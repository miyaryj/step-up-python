class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


user = User("Alice")
print(user.name)

user.name = "Bob"
print(user.name)
