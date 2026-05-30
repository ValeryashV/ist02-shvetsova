class Facade:
    pass
facade_1 = Facade()
facade_1_type = type(facade_1)

class Grade:
    minimum_passing = 65

class Rules:
    def washing_brushes(self):
        print('Point bristles towards the basin while washing your brushes.')

class Circle:
    pi = 3.14

    def __init__(self, diameter):
        print(f"New circle with diameter: {diameter}")
        self.radius = diameter / 2

    def area(self, radius):
        return self.pi * radius**2

    def circumference(self):
        return 2 * self.pi * self.radius

    def __repr__(self):
        return f"Circle with radius {self.radius}"

teaching_table = Circle(36)
medium_pizza = Circle(12)
round_room = Circle(11460)

print(medium_pizza.circumference())
print(teaching_table.circumference())
print(round_room.circumference())

print(medium_pizza)
print(teaching_table)
print(round_room)

print(dir(5))
def this_function_is_an_object():
    return "I am a function"
print(dir(this_function_is_an_object))