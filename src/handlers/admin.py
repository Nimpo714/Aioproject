# -- Modules
from aiogram import types
from aiogram.dispatcher import FSMContext
from prettytable import PrettyTable

# -- Local Modules
from src.sql import add_admin, user_in_table, set_quest, clear_questions_table, select_from_quest, set_game_status
from src.credits import admin_password
from src.keyboards import check_questions
from src.servicec import spliter, questions_parser
from src.state_machine import QuizCreator, QuestionsCheck


async def admin_add(message: types.Message):
    split = spliter(message.text)
    try:
        if split[1] == admin_password:
            add_admin(message.chat.id)
            await message.answer("Админ был добавлен")
    except IndexError:
        await message.answer("Вы забыли пароль /admin <pass>")


async def start_quiz_creation(message: types.Message, state: FSMContext):
    if not user_in_table(message.chat.id, 'admins'):
        return await message.answer("❌ Опросы может создавать только администратор.")

    await state.update_data(questions_list=[], current_count=1)
    await message.answer(f"📝 Вопрос 1 из 5. Введите текст вопроса:")
    await QuizCreator.waiting_for_question.set()


async def process_question(message: types.Message, state: FSMContext):
    await state.update_data(temp_question=message.text)
    await message.answer(
        "Теперь введите 4 варианта ответа <b>ЧЕРЕЗ ЗАПЯТУЮ</b>\n"
        "(например: Марс, Юпитер, Земля, Сатурн)",
        parse_mode="HTML"
    )
    await QuizCreator.waiting_for_options.set()


async def process_options(message: types.Message, state: FSMContext):
    # Разделяем по запятой и убираем лишние пробелы
    options = [opt.strip() for opt in message.text.split(',')]

    if len(options) != 4:
        return await message.answer("⚠️ Ошибка! Нужно ввести ровно 4 варианта через запятую.")

    await state.update_data(temp_options=options)

    # --- ПРЕДПОКАЗ ТАБЛИЦЕЙ ---
    table = PrettyTable()
    table.field_names = ["№", "Вариант ответа"]
    for i, opt in enumerate(options, 1):
        table.add_row([i, opt])

    output_text = (
        f"<b>Проверьте варианты:</b>\n"
        f"<pre>{table}</pre>\n"
        f"Введите <b>НОМЕР</b> правильного ответа (1, 2, 3 или 4):"
    )

    await message.answer(output_text, parse_mode="HTML", protect_content=True)
    await QuizCreator.waiting_for_correct.set()


async def process_correct_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    options = data['temp_options']
    question_text = data['temp_question']
    questions_list = data.get('questions_list', [])
    current_count = data.get('current_count', 1)

    # Проверка ввода номера
    if not message.text.isdigit() or not (1 <= int(message.text) <= 4):
        return await message.answer("⚠️ Ошибка! Введите только цифру: 1, 2, 3 или 4")

    correct_index = int(message.text) - 1
    correct_text = options[correct_index]

    # Сохраняем текущий вопрос в список
    questions_list.append({
        "question": question_text,
        "options": options,
        "correct": correct_text
    })

    if current_count < 5:
        # Обновляем данные и просим следующий вопрос
        new_count = current_count + 1
        await state.update_data(questions_list=questions_list, current_count=new_count)
        await message.answer(f"✅ Вопрос {current_count} сохранен.")
        await message.answer(f"📝 Введите текст вопроса <b>№{new_count}</b>:", parse_mode="HTML")
        await QuizCreator.waiting_for_question.set()
    else:
        # Финал: запись 5 вопросов в БД
        await message.answer("💾 Все 5 вопросов собраны! Сохраняю в базу...")

        clear_questions_table()
        for item in questions_list:
            # Если ваша БД принимает варианты как список, оставляем так.
            # Если как строку, используем: ", ".join(item['options'])
            set_quest(
                quest_text=item['question'],
                quest_ans=item['options'],
                cor_ans=item['correct']
            )

        await message.answer("🚀 Квиз успешно создан и доступен в БД!")
        await state.finish()


async def start_game(message: types.Message):
    # Если пользователь является админом (находится в таблице admins)
    if user_in_table(message.chat.id, 'admins'):
        quests = []
        # Вопросы с 1 - 5
        for i in range(1, 5+1):
            quest_data = select_from_quest(i, select='*')
            if quest_data:  # Проверка, что данные получены
                quests.append(quest_data)

        questions_parsed_list = questions_parser(quests)
        await message.answer('Сверка вопросов:')

        if not questions_parsed_list:
            await message.answer('Список вопросов пуст \n/questions для того чтоб начать заполнение')
            return

        # - Вывод
        for q in questions_parsed_list:
            await message.answer(q)
        await message.answer('Начать игру?', reply_markup=check_questions())
        await QuestionsCheck.are_you_sure.set()

    else:
        await message.answer('У вас нет прав администратора (вы не в списке)')

async def game_sure(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        set_game_status(True)
        await message.answer('Игра начата')
        await state.finish()

    elif message.text == 'Нет':
        # await message.answer('Игра не будет начата\nХотите изменить вопросы?', reply_markup=check_questions())
        await message.answer('Отмена')
        await state.finish()