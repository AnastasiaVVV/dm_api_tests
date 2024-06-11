
def attempt(n=5):
    def decorator(
            func
    ):
        def wraps(*args, **kwargs):
            print("-------------")
            print(n)
            func(*args, **kwargs)
            print("-------------")
            return

        return wraps
    return decorator

@attempt(n=5)
def my_print(name):
    print(f"Hello {name}!")

@attempt(n=5)
def my_print1(name):
    print(f"Hello {name}1!")

@attempt(n=5)
def my_print2(name):
    print(f"Hello {name}2!")

@attempt(n=5)
def my_print3(asdasda):
    print(f"Hello {asdasda}3!")


my_print(name='Иван')
my_print1(name='Vasya')
my_print2(name='Petya')
my_print3(asdasda='Sasha')
