import threading

from ..enums.vehicle_type import VehicleType


class ParkingSpot:
    def __init__(self, spot_id: str, allowed_type: VehicleType) -> None:
        self.id = spot_id
        self.allowed_type = allowed_type
        self._occupied = False
        self._lock = threading.Lock()

    def try_occupy(self) -> bool:
        with self._lock:
            if not self._occupied:
                self._occupied = True
                return True
            return False

    def vacate(self) -> None:
        with self._lock:
            self._occupied = False

    def is_occupied(self) -> bool:
        with self._lock:
            return self._occupied
