from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class User:
    id: str
    name: str

    def __str__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
