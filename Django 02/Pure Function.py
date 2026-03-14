# Пример
old_digit = 5

def add_number(new_value):
    global old_digit
    old_digit += new_value
    return old_digit

print(add_number(10)) # 15

# Зависимость от глобальной переменной делает функцию не чистой, 
# так как она изменяет состояние программы и может привести к непредсказуемым результатам при повторных вызовах.