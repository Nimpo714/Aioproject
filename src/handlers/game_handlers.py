# -- Modules
from aiogram import types
from aiogram.dispatcher import FSMContext
# -- Local Modules
from src.sql import select_from_quest
from src.sql import (
    select_from_quest, 
    start_user_timer, 
    add_correct_answer, 
    finish_user_game, 
    is_game_open,
    played_the_game
    
)
from src.state_machine import Game


async def play_quiz(message: types.Message, state: FSMContext):
    does_user_played_the_game = played_the_game(message.chat.id)
    print(does_user_played_the_game)
    if not does_user_played_the_game:
        pass
    else:
        await message.answer("Простите, но вы уже играли в игру")
        return

    if not is_game_open(): 
        await message.answer("Простите, но игра не активна. Дождитесь запуска администратором.")
        return # Нужно прервать выполнение

    chat_id = message.chat.id
    data = await state.get_data()
    current_q_id = data.get('current_q_id', 1) 

    # 2. Таймер запускаем только при самом первом входе
    if current_q_id == 1 and message.text == '/game':
        start_user_timer(chat_id)

    # 3. Проверка ответа на ПРЕДЫДУЩИЙ вопрос
    if current_q_id > 1:
        # Получаем данные вопроса, на который пользователь только что ответил
        prev_q_id = current_q_id - 1
        prev_quest = select_from_quest(prev_q_id)
        
        if prev_quest:
            correct_answer = str(prev_quest[6]) # cor_ans
            if message.text == correct_answer:
                add_correct_answer(chat_id)

    # 4. Лимит вопросов (здесь 5)
    # Если текущий id стал 6, значит ответили на 5 вопросов — финишируем
    if current_q_id > 5:
        final_rate = finish_user_game(chat_id) 
        await message.answer(
            f"🏁 Квиз окончен!\nВаш результат сохранен в таблице лидеров.", 
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.finish()
        return

    # 5. Выдача ТЕКУЩЕГО вопроса
    quest_data = select_from_quest(current_q_id)

    if quest_data:
        # Распаковка: id, quest, ans1, ans2, ans3, ans4, cor_ans
        q_id, q_text, a1, a2, a3, a4, cor = quest_data
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(a1, a2).add(a3, a4)

        await message.answer(
            f"<b>Вопрос №{current_q_id}</b>\n\n{q_text}", 
            reply_markup=markup, 
            parse_mode="HTML"
        )
        
        # Увеличиваем счетчик для следующего шага
        await state.update_data(current_q_id=current_q_id + 1)
        # Убедитесь, что Game.question — это состояние, в котором находится этот хендлер
        await Game.question.set() 
    else:
        # Если вопросов меньше 5 в базе, корректно завершаем
        finish_user_game(chat_id)
        await message.answer("📭 Вопросы в базе закончились.", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()