from datetime import datetime

from ..enums.gate_type import GateType
from ..service.parking_lot import ParkingLot
from .gate import Gate
from .ticket import Ticket
from .vehicle import Vehicle


class EntryGate(Gate):
    def __init__(self, gate_id: str) -> None:
        super().__init__(id=gate_id)

    def get_type(self) -> GateType:
        return GateType.ENTRY

    def park_vehicle(self, vehicle: Vehicle, entry_time: datetime) -> Ticket | None:
        return ParkingLot.get_instance().park_vehicle(vehicle, entry_time)
