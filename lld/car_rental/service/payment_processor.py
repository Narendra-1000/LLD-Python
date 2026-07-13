from ..enums.payment_status import PaymentStatus
from ..model.booking import Booking
from ..strategy.payment.payment_strategy import PaymentStrategy


class PaymentProcessor:
    def __init__(self, payment_strategy: PaymentStrategy) -> None:
        self._payment_strategy = payment_strategy

    def pay(self, booking: Booking) -> bool:
        success = self._payment_strategy.process_payment(booking)

        if success:
            booking.payment_status = PaymentStatus.SUCCESS
        else:
            booking.payment_status = PaymentStatus.FAILED
            print("Payment Failed!")

        return success
