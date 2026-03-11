# удалить из списка все элементы, которые меньше заданного числа
def remove_less_than(list, number):
    list_copy = list[:]

    for num in list_copy:
        if num < number:
            list.remove(num)

    return list



list = []
list_size = int(input("Enter the size of the list: "))

for i in range(list_size):
    num = int(input("Enter a number: "))

    list.append(num)

print("List:", list)
number = int(input("Enter a number to remove elements less than it: "))

print("List after removing elements less than", number, ":", remove_less_than(list, number))