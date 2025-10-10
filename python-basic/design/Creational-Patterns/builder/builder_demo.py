class Person:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def __str__(self):
        return f'Person(name={self.name}, age={self.age}, sex={self.sex})'


class PersonBuilder:
    def __init__(self):
        self.name = None
        self.age = None
        self.sex = None

    def set_name(self, value):
        self.name = value
        return self
    
    def set_age(self, value):
        self.age = value
        return self
    
    def set_sex(self, value):
        self.sex = value
        return self
    
    def build(self):
        return Person(self.name, self.age, self.sex)


# Correct instantiation - outside of any class
person = PersonBuilder().set_name('James').set_age(18).set_sex('Male').build()
print(person)