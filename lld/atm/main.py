from .model.account import Account
from .model.atm import ATM
from .model.card import Card
from .repository.atm_repository import ATMRepository
from .service.atm_machine import ATMMachine


def main() -> None:
    card = Card(
        "CARD123",
        "1234",
        Account("ACC123", 5000),
    )

    atm1 = ATM("ATM1", 5, 5, 20)
    atm2 = ATM("ATM2", 0, 2, 5)

    atm_repository = ATMRepository()
    atm_repository.save(atm1)
    atm_repository.save(atm2)

    atm_machine2 = ATMMachine("ATM2", atm_repository)

    atm_machine2.insert_card(card)
    atm_machine2.enter_pin("1234")
    atm_machine2.select_option("WITHDRAW")
    atm_machine2.dispense_cash(1410)


if __name__ == "__main__":
    main()
