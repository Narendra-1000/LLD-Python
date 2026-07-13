import threading

from .enums.vehicle_type import VehicleType
from .factory.vehicle_factory import VehicleFactory
from .model.branch import Branch
from .model.user import User
from .repository.booking_repository import BookingRepository
from .repository.branch_repository import BranchRepository
from .service.booking_service import BookingService
from .strategy.booking.least_booked_vehicle_strategy import LeastBookedVehicleStrategy
from .strategy.payment.credit_card_payment_strategy import CreditCardPaymentStrategy
from .strategy.payment.wallet_payment_strategy import WalletPaymentStrategy
from .strategy.pricing.hourly_pricing_strategy import HourlyPricingStrategy
from .utils.date_time_parser import DateTimeParser


def main() -> None:
    branch_repo = BranchRepository()
    booking_repo = BookingRepository()

    branch1 = Branch("B1", "New York")
    branch2 = Branch("B2", "Boston")
    branch_repo.add_branch(branch1)
    branch_repo.add_branch(branch2)

    branch1.add_vehicle(VehicleFactory.create(VehicleType.SEDAN, "NY1234", 25, 3.5))
    branch1.add_vehicle(VehicleFactory.create(VehicleType.SEDAN, "NY5678", 22, 3))
    branch1.add_vehicle(VehicleFactory.create(VehicleType.SUV, "NYB100", 30, 4))

    branch2.add_vehicle(VehicleFactory.create(VehicleType.SEDAN, "BO1234", 25, 4))

    user = User("U1", "John Doe", "john@example.com")

    start = DateTimeParser.parse("21 May 7:30 AM 2025")
    end = DateTimeParser.parse("21 May 12:30 PM 2025")

    booking_service = BookingService.get_instance(
        branch_repo,
        booking_repo,
        LeastBookedVehicleStrategy(),
        HourlyPricingStrategy(),
    )

    print("--------------")

    def book_with_credit_card() -> None:
        print(f"{threading.current_thread().name} started!")
        booking_service.book_vehicle(
            "B1",
            VehicleType.SUV,
            start,
            end,
            user,
            CreditCardPaymentStrategy(),
            branch1,
            branch2,
            100.0,
        )
        print(f"{threading.current_thread().name} ended!")

    def book_with_wallet() -> None:
        print(f"{threading.current_thread().name} started!")
        booking_service.book_vehicle(
            "B1",
            VehicleType.SUV,
            start,
            end,
            user,
            WalletPaymentStrategy(),
            branch1,
            branch2,
            100.0,
        )
        print(f"{threading.current_thread().name} ended!")

    t1 = threading.Thread(target=book_with_credit_card)
    t2 = threading.Thread(target=book_with_wallet)

    t1.start()
    t2.start()

    print("--------------")


if __name__ == "__main__":
    main()
