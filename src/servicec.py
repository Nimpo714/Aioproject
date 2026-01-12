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