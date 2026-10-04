"""Data model."""
from dataclasses import dataclass, asdict


@dataclass
class Student:
    id: int
    name: str
    email: str
    age: int
    course: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            id=int(data["id"]),
            name=data["name"],
            email=data["email"],
            age=int(data["age"]),
            course=data["course"],
        )
