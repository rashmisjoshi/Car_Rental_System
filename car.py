# car_rental_system/car.py

class Car:
    def __init__(self, car_id, make, model, year, available=True):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.available = available

    def rent(self):
        if self.available:
            self.available = False
            return True
        else:
            return False

    def return_car(self):
        self.available = True
