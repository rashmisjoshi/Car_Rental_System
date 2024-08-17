import mysql.connector

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rashmi@0507",
        database="car_rental_system"
    )

# Function to rent a car
def rent_car(customer_id, car_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Check if the car is available
    cursor.execute("SELECT available FROM cars WHERE car_id = %s", (car_id,))
    car = cursor.fetchone()

    if car and car['available']:
        # Update car availability
        cursor.execute("UPDATE cars SET available = FALSE WHERE car_id = %s", (car_id,))
        
        # Insert rental record
        rental_id = f"R{car_id[1:]}"  # Simple rental ID generation
        cursor.execute("INSERT INTO rentals (rental_id, customer_id, car_id, rental_fee) VALUES (%s, %s, %s, %s)",
                       (rental_id, customer_id, car_id, 500.0))  # Assume a fixed rental fee for simplicity
        
        # Commit changes
        conn.commit()
        
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False

# Function to return a car
def return_car(customer_id, car_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Check if the car is rented by the customer
    cursor.execute("SELECT * FROM rentals WHERE car_id = %s AND customer_id = %s", (car_id, customer_id))
    rental = cursor.fetchone()

    if rental:
        # Update car availability
        cursor.execute("UPDATE cars SET available = TRUE WHERE car_id = %s", (car_id,))
        
        # Delete rental record
        cursor.execute("DELETE FROM rentals WHERE car_id = %s AND customer_id = %s", (car_id, customer_id))
        
        # Commit changes
        conn.commit()
        
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False

# Function to fetch customer rented cars
def get_rented_cars(customer_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT cars.make
        FROM cars
        JOIN rentals ON cars.car_id = rentals.car_id
        WHERE rentals.customer_id = %s
    """, (customer_id,))
    rented_cars = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return [car['make'] for car in rented_cars]

# Main script
def main():
    # Rent cars
    rent_car("CU001", "C001")
    rent_car("CU002", "C002")

    # Display rented cars for customers
    print(f"Vrusabh Gawande's Rented Cars: {get_rented_cars('CU001')}")
    print(f"Ashutosh Banasure's Rented Cars: {get_rented_cars('CU002')}")

    # Return cars
    return_car("CU001", "C001")

    # Display updated rented cars for customers
    print(f"Vrusabh Gawande's Updated Rented Cars: {get_rented_cars('CU001')}")
    print(f"Ashutosh Banasure's Updated Rented Cars: {get_rented_cars('CU002')}")

    # Display rental information
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT rentals.rental_id, customers.name, cars.make, rentals.rental_fee
        FROM rentals
        JOIN customers ON rentals.customer_id = customers.customer_id
        JOIN cars ON rentals.car_id = cars.car_id
    """)
    rentals = cursor.fetchall()
    for rental in rentals:
        print(f"Rental ID: {rental['rental_id']}, Customer: {rental['name']}, Car: {rental['make']}, Rental Fee: INR {rental['rental_fee']}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
