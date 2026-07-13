from ..enums.payment_status import PaymentStatus
from ..model.ticket import Ticket
from ..strategy.payment.payment_strategy import PaymentStrategy


class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def pay(self, ticket: Ticket, amount: float) -> bool:
        success = self._strategy.process_payment(ticket, amount)
        if success:
            ticket.payment_status = PaymentStatus.SUCCESS
        else:
            ticket.payment_status = PaymentStatus.FAILED
            print(f"Payment failed for ticket: {ticket.ticket_id}")
        return success
