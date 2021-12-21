class A():

    def b(self):
        pass


class B(A):

    def b(self):
        print(1)


b = B()

b.b()
