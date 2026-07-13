from ...model.booking import Booking
from .payment_strategy import PaymentStrategy


class WalletPaymentStrategy(PaymentStrategy):
    def process_payment(self, booking: Booking) -> bool:
        print(f"Processing wallet payment for booking: {booking.booking_id}")
        return True
