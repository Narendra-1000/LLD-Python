from ...model.booking import Booking
from .payment_strategy import PaymentStrategy


class CreditCardPaymentStrategy(PaymentStrategy):
    def process_payment(self, booking: Booking) -> bool:
        print(f"Processing credit card payment for booking: {booking.booking_id}")
        return True
