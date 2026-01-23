# Modules
import string
import random
# Local Modules
from src.sql import clear_promo_code, add_promo_code

def spliter(text: str, split_symb=' '):
    return text.split(split_symb)

def questions_parser(questions):
    # [(1, 'Hello', '1', '2', '3', '4', '2'), ...]
    parsed_list = []
    for item in questions:
        text = f'''Вопрос номер N{item[0]}
Вопрос: {item[1]}
Варианты:
N1: {item[2]}
N2: {item[3]}
N3: {item[4]}
N4: {item[5]}'''
        parsed_list.append(text)
    return parsed_list

def auto_promocodes(return_promocodes_list: bool = False):
    """ Автоматически создает 10 промокодов """
    clear_promo_code()
    code_list = []
    for i in range(10):
        chars = string.ascii_letters + string.digits # + string.punctuation
        promo = "".join(random.choice(chars) for _ in range(15))
        add_promo_code(promo)
        if return_promocodes_list:
            code_list.append(promo)
    return code_list