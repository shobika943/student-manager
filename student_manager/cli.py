"""Menu-driven command line interface."""
from typing import List

from .models import Student
from .repository import StorageError
from .service import StudentNotFoundError, StudentService
from .validators import ValidationError

MENU = """
==============================
   STUDENT MANAGEMENT SYSTEM
==============================
 1. Add student
 2. View all students
 3. View student by ID
 4. Update student
 5. Delete student
 6. Search students
 0. Exit
------------------------------"""


def print_table(students: List[Student]) -> None:
    if not students:
        print("\nNo records found.")
        return
    print(f"\n{'ID':<5}{'Name':<22}{'Email':<30}{'Age':<6}{'Course':<20}")
    print("-" * 83)
    for s in students:
        print(f"{s.id:<5}{s.name:<22}{s.email:<30}{s.age:<6}{s.course:<20}")
    print(f"\nTotal: {len(students)}")


def ask_id(prompt: str = "Enter student ID: ") -> int:
    raw = input(prompt).strip()
    if not raw.isdigit():
        raise ValidationError("ID must be a positive number.")
    return int(raw)


class CLI:
    def __init__(self, service: StudentService):
        self.service = service
        self.actions = {
            "1": self.add, "2": self.view_all, "3": self.view_one,
            "4": self.update, "5": self.delete, "6": self.search,
        }

    def run(self) -> None:
        while True:
            print(MENU)
            try:
                choice = input("Choose an option: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                return
            if choice == "0":
                print("Goodbye!")
                return
            action = self.actions.get(choice)
            if not action:
                print("Invalid option. Please choose 0-6.")
                continue
            try:
                action()
            except (ValidationError, StudentNotFoundError, StorageError) as exc:
                print(f"\n[Error] {exc}")
            except (KeyboardInterrupt, EOFError):
                print("\nCancelled.")

    def add(self):
        print("\n-- Add Student --")
        s = self.service.add(input("Name: "), input("Email: "),
                             input("Age: "), input("Course: "))
        print(f"\n[OK] Student added with ID {s.id}.")

    def view_all(self):
        print_table(self.service.list_all())

    def view_one(self):
        print_table([self.service.get(ask_id())])

    def update(self):
        sid = ask_id()
        current = self.service.get(sid)
        print_table([current])
        print("Press Enter to keep the current value.")
        self.service.update(
            sid,
            name=input(f"Name [{current.name}]: "),
            email=input(f"Email [{current.email}]: "),
            age=input(f"Age [{current.age}]: "),
            course=input(f"Course [{current.course}]: "),
        )
        print("\n[OK] Student updated.")

    def delete(self):
        sid = ask_id()
        student = self.service.get(sid)
        if input(f"Delete '{student.name}'? (y/N): ").strip().lower() == "y":
            self.service.delete(sid)
            print("\n[OK] Student deleted.")
        else:
            print("Deletion cancelled.")

    def search(self):
        results = self.service.search(input("Search (name/email/course/ID): "))
        print_table(results)
