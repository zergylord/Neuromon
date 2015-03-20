class First(object):
    @classmethod
    def foo(cls):
        print cls.__name__
class Second(First):
    def __init__(self):
        Second.foo()

q = Second()

