from profile_decorator import profile_decorator

profile_decorator.init()


@profile_decorator.profile_memory
def my_func():
    print("hello, world")


if __name__ == "__main__":
    my_func()
