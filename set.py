class A:
    def __init__(self, a):
        self.a = a

stack = [A(1), A(2),A(3),A(4),A(5)]
a = stack[0]
del stack[0]
for i in stack:
    print(i.a)
print(a.a)