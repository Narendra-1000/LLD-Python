from ...model.ticket import Ticket
from .payment_strategy import PaymentStrategy


class UpiPayment(PaymentStrategy):
    def process_payment(self, ticket: Ticket, amount: float) -> bool:
        print(f"Paid ₹{amount} for ticket {ticket.ticket_id} via UPI.")
        return True
