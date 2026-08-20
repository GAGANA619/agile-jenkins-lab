from datetime import datetime


class Flight:
    def __init__(self, flight_no, source, destination, travel_date,
                 economy_seats, business_seats, first_seats):

        self.flight_no = flight_no
        self.source = source
        self.destination = destination
        self.travel_date = datetime.strptime(travel_date, "%Y-%m-%d")
        self.seats = {
            "Economy": economy_seats,
            "Business": business_seats,
            "First": first_seats
        }

        self.base_fare = {
            "Economy": 5000,
            "Business": 10000,
            "First": 20000
        }

        self.bookings = {}


class Passenger:
    def __init__(self, passenger_id, name, age, passenger_type):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.passenger_type = passenger_type


class AirlineReservation:

    def __init__(self):
        self.flights = {}

    # Flight search
    def add_flight(self, flight):
        self.flights[flight.flight_no] = flight

    def search_flight(self, source, destination):
        result = []

        for flight in self.flights.values():
            if (flight.source.lower() == source.lower()
                    and flight.destination.lower() == destination.lower()):
                result.append(flight.flight_no)

        return result

    # Dynamic fare calculation
    def calculate_fare(self, flight, seat_class, booking_date,
                       passenger_type):

        if seat_class not in flight.base_fare:
            raise ValueError("Invalid class")

        if flight.seats[seat_class] <= 0:
            raise ValueError("Flight fully booked")

        fare = flight.base_fare[seat_class]

        available = flight.seats[seat_class]

        # Price based on seat availability
        if available <= 2:
            fare *= 1.50
        elif available <= 5:
            fare *= 1.25
        elif available <= 10:
            fare *= 1.10

        booking_date = datetime.strptime(
            booking_date, "%Y-%m-%d"
        )

        days_before_travel = (
            flight.travel_date - booking_date
        ).days

        # Price based on booking date
        if days_before_travel <= 3:
            fare *= 1.40
        elif days_before_travel <= 7:
            fare *= 1.20
        elif days_before_travel <= 30:
            fare *= 1.10

        # Passenger type
        if passenger_type.lower() == "child":
            fare *= 0.75
        elif passenger_type.lower() == "senior":
            fare *= 0.80
        elif passenger_type.lower() == "student":
            fare *= 0.90

        return round(fare, 2)

    # Passenger validation
    def validate_passenger(self, passenger):
        if not passenger.name.strip():
            return False

        if passenger.age <= 0 or passenger.age > 120:
            return False

        valid_types = [
            "adult",
            "child",
            "senior",
            "student"
        ]

        return passenger.passenger_type.lower() in valid_types

    # Seat availability
    def seat_availability(self, flight_no, seat_class):
        if flight_no not in self.flights:
            raise ValueError("Flight not found")

        flight = self.flights[flight_no]

        if seat_class not in flight.seats:
            raise ValueError("Invalid class")

        return flight.seats[seat_class]

    # Passenger booking
    def book_passenger(self, flight_no, passenger,
                       seat_class, booking_date):

        if flight_no not in self.flights:
            raise ValueError("Flight not found")

        if not self.validate_passenger(passenger):
            raise ValueError("Invalid passenger")

        flight = self.flights[flight_no]

        if seat_class not in flight.seats:
            raise ValueError("Invalid class")

        # Double booking check
        if passenger.passenger_id in flight.bookings:
            raise ValueError("Passenger already booked")

        # Seat availability
        if flight.seats[seat_class] <= 0:
            raise ValueError("Flight fully booked")

        fare = self.calculate_fare(
            flight,
            seat_class,
            booking_date,
            passenger.passenger_type
        )

        flight.seats[seat_class] -= 1

        flight.bookings[passenger.passenger_id] = {
            "passenger": passenger,
            "class": seat_class,
            "fare": fare,
            "booking_date": booking_date,
            "cancelled": False,
            "baggage_charge": 0
        }

        return fare

    # Baggage charges
    def calculate_baggage_charge(self, baggage_kg):

        free_baggage = 20
        charge_per_kg = 500

        if baggage_kg <= free_baggage:
            return 0

        excess = baggage_kg - free_baggage

        return excess * charge_per_kg

    # Add baggage to booking
    def add_baggage(self, flight_no, passenger_id, baggage_kg):

        if flight_no not in self.flights:
            raise ValueError("Flight not found")

        flight = self.flights[flight_no]

        if passenger_id not in flight.bookings:
            raise ValueError("Passenger not booked")

        if baggage_kg < 0:
            raise ValueError("Invalid baggage")

        charge = self.calculate_baggage_charge(
            baggage_kg
        )

        flight.bookings[
            passenger_id
        ]["baggage_charge"] = charge

        return charge

    # Cancellation
    def cancel_booking(self, flight_no, passenger_id,
                       cancellation_date):

        if flight_no not in self.flights:
            raise ValueError("Flight not found")

        flight = self.flights[flight_no]

        if passenger_id not in flight.bookings:
            raise ValueError("Booking not found")

        booking = flight.bookings[passenger_id]

        if booking["cancelled"]:
            raise ValueError("Booking already cancelled")

        cancellation_date = datetime.strptime(
            cancellation_date,
            "%Y-%m-%d"
        )

        days_before_travel = (
            flight.travel_date - cancellation_date
        ).days

        fare = booking["fare"]

        # Refund calculation
        if days_before_travel >= 15:
            refund_percentage = 0.90

        elif days_before_travel >= 7:
            refund_percentage = 0.75

        elif days_before_travel >= 3:
            refund_percentage = 0.50

        else:
            refund_percentage = 0.00

        refund = fare * refund_percentage

        booking["cancelled"] = True

        # Return seat
        flight.seats[
            booking["class"]
        ] += 1

        return round(refund, 2)

    # Get booking details
    def get_booking(self, flight_no, passenger_id):

        if flight_no not in self.flights:
            raise ValueError("Flight not found")

        flight = self.flights[flight_no]

        if passenger_id not in flight.bookings:
            raise ValueError("Booking not found")

        return flight.bookings[passenger_id]


if __name__ == "__main__":

    system = AirlineReservation()

    flight = Flight(
        "AI101",
        "Chennai",
        "Delhi",
        "2026-12-20",
        10,
        5,
        2
    )

    system.add_flight(flight)

    # Flight search
    print("Flights:")
    print(
        system.search_flight(
            "Chennai",
            "Delhi"
        )
    )

    passenger = Passenger(
        "P001",
        "Rahul",
        25,
        "Adult"
    )

    # Booking
    fare = system.book_passenger(
        "AI101",
        passenger,
        "Economy",
        "2026-11-20"
    )

    print("\nBooking Successful")
    print("Fare:", fare)

    # Seat availability
    print(
        "Available Economy Seats:",
        system.seat_availability(
            "AI101",
            "Economy"
        )
    )

    # Baggage
    baggage_charge = system.add_baggage(
        "AI101",
        "P001",
        25
    )

    print("Baggage Charge:", baggage_charge)

    # Cancellation
    refund = system.cancel_booking(
        "AI101",
        "P001",
        "2026-11-20"
    )

    print("Refund:", refund)
