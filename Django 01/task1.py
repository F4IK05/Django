import random

# минимальный, положительный элемент
def min_positive(list):
    list_pos = []

    for num in list:
        if num > 0:
            list_pos.append(num)

    min_value = list_pos[0]

    for num in list_pos:
        if num < min_value:
            min_value = num
            
    return min_value

# максимальный, отрицательный элемент
def max_negative(list):
    list_neg = []

    for num in list:
        if num < 0:
            list_neg.append(num)

    max_value = list_neg[0]

    for num in list_neg:
        if num < max_value:
            max_value = num

    return max_value

# количество отрицательных элементов
def count_negative(list):
    count = 0

    for num in list:
        if num < 0:
            count += 1
    
    return count

# количество положительных элементов
def count_positive(list):
    count = 0

    for num in list:
        if num > 0:
            count += 1
    
    return count

# количество нулей
def count_zero(list):
    count = 0

    for num in list:
        if num == 0:
            count += 1
    
    return count

list = []

for i in range(10):
    list.append(random.randint(-10, 10))


print("List:", list)
print("Min positive:", min_positive(list))
print("Max negative:", max_negative(list))
print("Count negative:", count_negative(list))
print("Count positive:", count_positive(list))
print("Count zero:", count_zero(list))