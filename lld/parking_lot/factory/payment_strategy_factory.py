from ..enums.payment_mode import PaymentMode
from ..strategy.payment.card_payment import CardPayment
from ..strategy.payment.cash_payment import CashPayment
from ..strategy.payment.payment_strategy import PaymentStrategy
from ..strategy.payment.upi_payment import UpiPayment


class PaymentStrategyFactory:
    @staticmethod
    def get(mode: PaymentMode) -> PaymentStrategy:
        if mode == PaymentMode.CASH:
            return CashPayment()
        if mode == PaymentMode.UPI:
            return UpiPayment()
        if mode == PaymentMode.CARD:
            return CardPayment()
        raise ValueError(f"Unsupported payment mode: {mode}")
