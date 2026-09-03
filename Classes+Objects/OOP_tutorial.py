class Dog(object):
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Hi I am ", self.name)

tim = Dog('Tim')
fred = Dog('Fred')

tim.speak()
fred.speak()