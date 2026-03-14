def decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper

def some_function():
    print("Inside some_function")

f = decorator(some_function)

f()