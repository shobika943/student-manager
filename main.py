"""Entry point: python main.py"""
from student_manager.cli import CLI
from student_manager.repository import JsonRepository
from student_manager.service import StudentService


def main() -> None:
    CLI(StudentService(JsonRepository("data/students.json"))).run()


if __name__ == "__main__":
    main()
