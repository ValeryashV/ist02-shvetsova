from abc import ABC, abstractmethod

class AbstractEmployee(ABC):
    new_id = 1

    def __init__(self):
        self.id = AbstractEmployee.new_id
        AbstractEmployee.new_id += 1

    @abstractmethod
    def say_id(self):
        pass


class Employee(AbstractEmployee):
    def __init__(self):
        super().__init__()
        self._name = None
        self._id = 999
        self.__id = 777

    def say_id(self):
        print(f"My id is {self.id}")

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    def del_name(self):
        del self._name
        print("_name deleted")


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def say_user_info(self):
        print(f"Username: {self.username}, Role: {self.role}")

class Admin(Employee, User):
    def __init__(self):
        Employee.__init__(self)
        User.__init__(self, self.id, "Admin")

    def say_id(self):
        super().say_id()
        print("I am an Admin")

class Manager(Admin):
    def say_id(self):
        print("I'm in charge!")
        super().say_id()

class Meeting:
    def __init__(self):
        self.attendees = []

    def __add__(self, employee):
        self.attendees.append(employee)
        return self

    def __len__(self):
        return len(self.attendees)


e1 = Employee()
e2 = Employee()
e1.say_id()
e2.say_id()

e3 = Admin()
e3.say_id()
e3.say_user_info()

e4 = Manager()
e4.say_id()

meeting = [Employee(), Admin(), Manager()]
print("\n--- Meeting Polymorphism ---")
for person in meeting:
    person.say_id()

print("\n--- Dunder Methods ---")
m1 = Meeting()
m1 = m1 + e1
m1 = m1 + e2
m1 = m1 + e3
print(f"Attendees count: {len(m1)}")

print("\n--- Encapsulation ---")
emp = Employee()
emp.set_name("Alex")
print(f"Name: {emp.get_name()}")
emp.del_name()

print("\n--- Dir check ---")
print([attr for attr in dir(emp) if 'id' in attr.lower() or 'name' in attr.lower()])
