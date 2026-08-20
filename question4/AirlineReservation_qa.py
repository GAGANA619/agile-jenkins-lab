import unittest

from AirlineReservation import (
    Flight,
    Passenger,
    AirlineReservation
)


class AirlineReservationQA(unittest.TestCase):

    def setUp(self):
        self.system = AirlineReservation()

        self.flight = Flight(
            "AI101",
            "Chennai",
            "Delhi",
            "2026-12-20",
            5,
            3,
            2
        )

        self.system.add_flight(self.flight)

    def test_successful_booking(self):
        passenger = Passenger(
            "P001",
            "Rahul",
            25,
            "Adult"
        )

        fare = self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-20"
        )

        self.assertGreater(fare, 0)

        self.assertEqual(
            self.system.seat_availability("AI101", "Economy"),
            4
        )

    def test_double_booking(self):
        passenger = Passenger(
            "P002",
            "Anita",
            30,
            "Adult"
        )

        self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-20"
        )

        with self.assertRaises(ValueError):
            self.system.book_passenger(
                "AI101",
                passenger,
                "Economy",
                "2026-11-20"
            )

    def test_cancellation(self):
        passenger = Passenger(
            "P003",
            "Ravi",
            40,
            "Adult"
        )

        self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-20"
        )

        refund = self.system.cancel_booking(
            "AI101",
            "P003",
            "2026-11-20"
        )

        self.assertGreaterEqual(refund, 0)

        self.assertEqual(
            self.system.seat_availability("AI101", "Economy"),
            5
        )

    def test_refund_calculation(self):
        passenger = Passenger(
            "P004",
            "Suresh",
            35,
            "Adult"
        )

        fare = self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-01"
        )

        refund = self.system.cancel_booking(
            "AI101",
            "P004",
            "2026-11-01"
        )

        self.assertEqual(
            refund,
            round(fare * 0.90, 2)
        )

    def test_fully_booked_flight(self):

        for i in range(5):

            passenger = Passenger(
                "FULL" + str(i),
                "Passenger" + str(i),
                25,
                "Adult"
            )

            self.system.book_passenger(
                "AI101",
                passenger,
                "Economy",
                "2026-11-20"
            )

        passenger = Passenger(
            "P999",
            "NewPassenger",
            25,
            "Adult"
        )

        with self.assertRaises(ValueError):
            self.system.book_passenger(
                "AI101",
                passenger,
                "Economy",
                "2026-11-20"
            )

    def test_invalid_passenger(self):
        passenger = Passenger(
            "P005",
            "",
            25,
            "Adult"
        )

        with self.assertRaises(ValueError):
            self.system.book_passenger(
                "AI101",
                passenger,
                "Economy",
                "2026-11-20"
            )

    def test_excess_baggage(self):
        passenger = Passenger(
            "P006",
            "Kiran",
            25,
            "Adult"
        )

        self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-20"
        )

        charge = self.system.add_baggage(
            "AI101",
            "P006",
            30
        )

        self.assertEqual(charge, 5000)

    def test_normal_baggage(self):
        passenger = Passenger(
            "P007",
            "Arun",
            25,
            "Adult"
        )

        self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-20"
        )

        charge = self.system.add_baggage(
            "AI101",
            "P007",
            20
        )

        self.assertEqual(charge, 0)

    def test_dynamic_fare_calculation(self):

        fare = self.system.calculate_fare(
            self.flight,
            "Economy",
            "2026-12-18",
            "Adult"
        )

        self.assertGreater(fare, 5000)

    def test_senior_passenger(self):

        passenger = Passenger(
            "P009",
            "Ramesh",
            65,
            "Senior"
        )

        fare = self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-20"
        )

        self.assertGreater(fare, 0)

    def test_child_passenger(self):

        passenger = Passenger(
            "P010",
            "Child",
            10,
            "Child"
        )

        fare = self.system.book_passenger(
            "AI101",
            passenger,
            "Economy",
            "2026-11-20"
        )

        self.assertGreater(fare, 0)

    def test_flight_search(self):

        result = self.system.search_flight(
            "Chennai",
            "Delhi"
        )

        self.assertIn("AI101", result)


if __name__ == "__main__":
    unittest.main()
