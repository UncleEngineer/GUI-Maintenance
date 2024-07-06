class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def drive(self):
        print('The Car is moving.')

class ElectricCar(Car):
    def __init__(self, brand, model, year):
        super().__init__(brand, model, year)

    def charge(self):
        print('My electric car is fully charged.')

elecCar01 = ElectricCar('Tesla', 'Model S', 2020)
print(elecCar01.brand)
print(elecCar01.model)
print(elecCar01.year)
elecCar01.charge()
elecCar01.drive()
print('===========================================')
elecCar02 = ElectricCar('MG', 'Maxus 9', 2022)
print(elecCar02.brand)
print(elecCar02.model)
print(elecCar02.year)
elecCar02.charge()
elecCar02.drive()