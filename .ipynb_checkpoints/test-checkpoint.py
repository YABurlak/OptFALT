def foo():
    d = 10
    exec("d = 0")
    print(d)