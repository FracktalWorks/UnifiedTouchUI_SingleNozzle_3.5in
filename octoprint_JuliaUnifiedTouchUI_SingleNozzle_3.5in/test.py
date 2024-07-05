class Parent1:
    def __init__(self, arg1):
        self.arg1 = arg1
        print(f"Parent1 initialized with arg1: {arg1}")

class Parent2:
    def __init__(self):
        print("Parent2 initialized")

class Parent3:
    def __init__(self):
        print("Parent3 initialized")

class Child(Parent1, Parent2, Parent3):
    def __init__(self, arg1):
        Parent1.__init__(self, arg1)  # Initialize Parent1 with arg1
        print("extra")
        Parent2.__init__(self)  # Initialize Parent2 without arguments
        Parent3.__init__(self)  # Initialize Parent3 without arguments
        print("Child initialized")

# Example of creating an instance of Child
child_instance = Child(10)
