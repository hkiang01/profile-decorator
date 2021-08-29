from profile_decorator import __version__, profile_decorator

profile_decorator.init()


@profile_decorator.profile_memory
def test_version():
    assert __version__ == "0.1.0"
