# def count_up_to(n):
#     i = 1
#     while i <= n:
#         yield i
#         i += 1

# num = count_up_to(5)
# print(next(num))  # 1
# print(next(num))  # 2
# print(next(num))  # 3
# print(next(num))  # 4
# print(next(num))  # 5
# print(next(num))  # StopIteration

# Тип генераторной функции и генератора
from inspect import isgeneratorfunction, isgenerator

def gen_function():
    yield 10

gen = gen_function()

print('type gen_function is', type(gen_function)) # <class 'function'>
print('type gen is', type(gen)) # <class 'generator'>

print('gen_function is generatorfunction: ', isgeneratorfunction(gen_function)) # True
print('gen_function is generator: ', isgenerator(gen_function)) # False, gen_function функция, а не генератор

print('gen is generatorfunction: ', isgeneratorfunction(gen)) # False
print('gen is generator: ', isgenerator(gen)) # True