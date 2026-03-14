# # Пример 1
# def outer(x):
#     def inner():
#         print(x)
#     return inner

# f = outer(10)

# f()  # 10


# Пример 2
def multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = multiplier(2)
triple = multiplier(3)

print(double(5)) # 10, double запомнил n = 2
print(triple(5)) # 15, triple запомнил n = 3