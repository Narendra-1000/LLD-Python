import threading
from datetime import datetime

from .enums.pricing_strategy_type import PricingStrategyType
from .enums.vehicle_type import VehicleType
from .factory.pricing_strategy_factory import PricingStrategyFactory
from .factory.vehicle_factory import VehicleFactory
from .model.entry_gate import EntryGate
from .model.exit_gate import ExitGate
from .model.parking_floor import ParkingFloor
from .model.parking_spot import ParkingSpot
from .service.parking_lot import ParkingLot
from .utils.date_time_parser import DateTimeParser


def main() -> None:
    lot = ParkingLot.get_instance()
    entry_gate = EntryGate("EG1")
    ExitGate("XG1")

    lot.pricing_strategy = PricingStrategyFactory.get(
        PricingStrategyType["EVENT_BASED"]
    )

    floor1 = ParkingFloor("Floor1")
    floor1.add_spot(ParkingSpot("F1S1", VehicleType.BIKE))
    floor1.add_spot(ParkingSpot("F1S2", VehicleType.CAR))
    floor1.add_spot(ParkingSpot("F1S3", VehicleType.TRUCK))
    floor1.add_spot(ParkingSpot("F1S4", VehicleType.CAR))
    lot.add_floor(floor1)

    print("--------------------------")

    bike1 = VehicleFactory.create("KA01AB1234", VehicleType.BIKE)
    bike2 = VehicleFactory.create("KA01AB5678", VehicleType.BIKE)
    entry_time = DateTimeParser.parse("21 May 7:30 AM 2025")
    print(entry_time.replace(minute=0, second=0, microsecond=0))

    t1 = threading.Thread(
        target=entry_gate.park_vehicle,
        args=(bike1, entry_time),
    )
    t2 = threading.Thread(
        target=entry_gate.park_vehicle,
        args=(bike2, entry_time),
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
