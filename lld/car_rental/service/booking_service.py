import threading
import uuid
from datetime import datetime

from ..enums.booking_status import BookingStatus
from ..enums.vehicle_status import VehicleStatus
from ..enums.vehicle_type import VehicleType
from ..model.booking import Booking
from ..model.branch import Branch
from ..model.user import User
from ..repository.booking_repository import BookingRepository
from ..repository.branch_repository import BranchRepository
from ..strategy.booking.booking_strategy import BookingStrategy
from ..strategy.payment.payment_strategy import PaymentStrategy
from ..strategy.pricing.pricing_strategy import PricingStrategy
from .payment_processor import PaymentProcessor


class BookingService:
    _instance: "BookingService | None" = None
    _lock = threading.Lock()

    def __init__(
        self,
        branch_repo: BranchRepository,
        booking_repo: BookingRepository,
        booking_strategy: BookingStrategy,
        pricing_strategy: PricingStrategy,
    ) -> None:
        self._branch_repo = branch_repo
        self._booking_repo = booking_repo
        self.booking_strategy = booking_strategy
        self.pricing_strategy = pricing_strategy

    @classmethod
    def get_instance(
        cls,
        branch_repo: BranchRepository,
        booking_repo: BookingRepository,
        booking_strategy: BookingStrategy,
        pricing_strategy: PricingStrategy,
    ) -> "BookingService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(
                        branch_repo,
                        booking_repo,
                        booking_strategy,
                        pricing_strategy,
                    )
        return cls._instance

    def book_vehicle(
        self,
        branch_id: str,
        vehicle_type: VehicleType,
        start: datetime,
        end: datetime,
        user: User,
        payment_strategy: PaymentStrategy,
        pick_up_branch: Branch,
        drop_branch: Branch,
        distance_km: float,
    ) -> Booking | None:
        branch = self._branch_repo.get_branch(branch_id)
        if branch is None:
            print("Branch not found")
            return None

        active_vehicles = [
            vehicle
            for vehicle in branch.get_vehicles_by_type(vehicle_type)
            if vehicle.status == VehicleStatus.AVAILABLE
            and not vehicle.is_booked.get()
        ]

        if not active_vehicles:
            print(f"No active {vehicle_type.name} vehicles available.")
            return None

        vehicle = self.booking_strategy.book_vehicle(active_vehicles)

        if vehicle is None:
            print("No vehicle could be booked.")
            return None

        amount = self.pricing_strategy.calculate_price(vehicle, start, end, distance_km)

        booking = Booking(
            booking_id=str(uuid.uuid4()),
            user=user,
            vehicle=vehicle,
            pickup_branch=pick_up_branch,
            drop_branch=drop_branch,
            start_time=start,
            end_time=end,
            amount=amount,
        )

        processor = PaymentProcessor(payment_strategy)
        if not processor.pay(booking):
            print("Payment failed")
            vehicle.is_booked.set(False)
            return None

        booking.status = BookingStatus.CONFIRMED
        self._booking_repo.add_booking(booking)

        vehicle.increment_booking_count()
        vehicle.status = VehicleStatus.BOOKED

        print(booking)

        return booking

    def return_vehicle(self, booking_id: str) -> None:
        booking = self._booking_repo.get_booking_by_id(booking_id)
        if booking is None:
            raise RuntimeError("Booking not found")

        if booking.status != BookingStatus.CONFIRMED:
            raise RuntimeError("Vehicle is not currently booked")

        booking.status = BookingStatus.COMPLETED
        booking.vehicle.is_booked.set(False)

        drop_branch = booking.drop_branch
        drop_branch.add_vehicle(booking.vehicle)
        print(
            f"Vehicle returned to branch {drop_branch.city}: "
            f"{booking.vehicle.license_plate}"
        )
