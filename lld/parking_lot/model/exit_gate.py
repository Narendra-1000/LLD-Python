from datetime import datetime

from ..enums.gate_type import GateType
from ..enums.payment_mode import PaymentMode
from ..service.parking_lot import ParkingLot
from .gate import Gate


class ExitGate(Gate):
    def __init__(self, gate_id: str) -> None:
        super().__init__(id=gate_id)

    def get_type(self) -> GateType:
        return GateType.EXIT

    def unpark_vehicle(
        self,
        ticket_id: str,
        exit_time: datetime,
        payment_mode: PaymentMode,
    ) -> None:
        ParkingLot.get_instance().unpark_vehicle(ticket_id, exit_time, payment_mode)
