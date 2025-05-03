class Foo2:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

foo2 = Foo2(some_random_variable=1, whatever_the_user_supplies=2)
print(foo2.some_random_variable)  # 1
print(foo2.whatever_the_user_supplies)  # 2
print(foo2.__dict__)  # {'some_random_variable': 1, 'whatever_the_user_supplies': 2}