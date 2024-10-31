import sqlite3
from tabulate import tabulate

# Connect to the database
def connect():
    return sqlite3.connect('tilavaraus.db')

# Add a facility
def add_tila():
    tilan_nimi = input("Enter the name of the facility: ")
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tilat (tilan_nimi) VALUES (?)", (tilan_nimi,))
    connection.commit()
    connection.close()
    print(f"Added facility '{tilan_nimi}' successfully.")

# Add a reserver
def add_varaaja():
    nimi = input("Enter the name of the reserver: ")
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO varaajat (nimi) VALUES (?)", (nimi,))
    connection.commit()
    connection.close()
    print(f"Added reserver '{nimi}' successfully.")

# Add a reservation
def add_varaus():
    tila_id = int(input("Enter the facility ID for the reservation: "))
    varaaja_id = int(input("Enter the reserver ID for the reservation: "))
    varauspaiva = input("Enter the reservation date (YYYY-MM-DD): ")
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO varaukset (tila, varaaja, varauspaiva) VALUES (?, ?, ?)", (tila_id, varaaja_id, varauspaiva))
    connection.commit()
    connection.close()
    print(f"Added reservation for facility ID {tila_id} and reserver ID {varaaja_id} on {varauspaiva} successfully.")

# View all facilities
def view_tilat():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tilat")
    data = cursor.fetchall()
    print(tabulate(data, headers=["ID", "Tilan Nimi"]))
    connection.close()

# View all reservers
def view_varaajat():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM varaajat")
    data = cursor.fetchall()
    print(tabulate(data, headers=["ID", "Nimi"]))
    connection.close()

# View all reservations
def view_varaukset():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT varaukset.id, tilat.tilan_nimi, varaajat.nimi, varaukset.varauspaiva
        FROM varaukset
        JOIN tilat ON varaukset.tila = tilat.id
        JOIN varaajat ON varaukset.varaaja = varaajat.id
    """)
    data = cursor.fetchall()
    print(tabulate(data, headers=["ID", "Tila", "Varaaja", "Varaus Päivä"]))
    connection.close()

# Menu to choose actions
def menu():
    while True:
        print("\nChoose an action:")
        print("1 - View Facilities")
        print("2 - View Reservers")
        print("3 - View Reservations")
        print("4 - Add a Facility")
        print("5 - Add a Reserver")
        print("6 - Add a Reservation")
        print("0 - Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_tilat()
        elif choice == "2":
            view_varaajat()
        elif choice == "3":
            view_varaukset()
        elif choice == "4":
            add_tila()
        elif choice == "5":
            add_varaaja()
        elif choice == "6":
            add_varaus()
        elif choice == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
