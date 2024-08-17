# car_rental_system/rental.py

class Rental:
    def __init__(self, rental_id, customer, car, rental_fee):
        self.rental_id = rental_id
        self.customer = customer
        self.car = car
        self.rental_fee = rental_fee
