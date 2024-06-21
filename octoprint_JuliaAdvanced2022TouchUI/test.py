class ParentA:
    def __init__(self):
        print('ParentA initialized')
        super().__init__()  # Call the next class in the MRO

class ParentB:
    def __init__(self):
        print('ParentB initialized')
        super().__init__()  # Call the next class in the MRO

class ParentC:
    def __init__(self):
        print('ParentC initialized')
        super().__init__()  # Call the next class in the MRO

class Child(ParentA, ParentB, ParentC):
    def __init__(self):
        print('Child initializing')
        super().__init__()  # Call the __init__ methods of the parents
        print('Child initialized')

# Create an instance of Child class
child_instance = Child()
