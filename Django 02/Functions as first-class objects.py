# 1. Присваивание функций переменным

def msg(name):
    return f"Hello, {name}!"

# Присваивание функции переменной
f = msg

# Вызов функции с использованием переменной
print(f("Emma")) # Hello, Emma!

# 2. Передача функций в качестве аргументо
def msg(name):
    return f"Hello, {name}!"

def fun1(fun2, name):
    return fun2(name)

print(fun1(msg, "Alex")) # Hello, Alex!


# 3. Возврат функций из других функций
def fun1(msg):
    def fun2():
        return f"Message: {msg}"
    return fun2

# Получение функции fun2 из fun1
func = fun1("Hello, World!")
print(func()) # Message: Hello, World!


# 4. Хранение функций в структурах данных
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

# Хранение функций в словаре
d = {
    "add": add,
    "subtract": subtract
}

# Вызов функций из словаря
print(d["add"](5, 3)) # 8
print(d["subtract"](5, 3)) # 2