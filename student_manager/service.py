"""Business logic: CRUD + search. Independent of the UI."""
from typing import List, Optional

from .models import Student
from .repository import JsonRepository
from .validators import (
    ValidationError, validate_age, validate_course, validate_email, validate_name,
)


class StudentNotFoundError(Exception):
    pass


class StudentService:
    def __init__(self, repository: JsonRepository):
        self.repo = repository

    # ---------- Create ----------
    def add(self, name, email, age, course) -> Student:
        students = self.repo.load_all()
        email = validate_email(email)
        self._ensure_unique_email(students, email)
        new_id = max((s.id for s in students), default=0) + 1
        student = Student(new_id, validate_name(name), email,
                          validate_age(age), validate_course(course))
        students.append(student)
        self.repo.save_all(students)
        return student

    # ---------- Read ----------
    def list_all(self) -> List[Student]:
        return sorted(self.repo.load_all(), key=lambda s: s.id)

    def get(self, student_id: int) -> Student:
        for s in self.repo.load_all():
            if s.id == student_id:
                return s
        raise StudentNotFoundError(f"No student with ID {student_id}.")

    # ---------- Update ----------
    def update(self, student_id: int, name: Optional[str] = None,
               email: Optional[str] = None, age=None,
               course: Optional[str] = None) -> Student:
        students = self.repo.load_all()
        target = next((s for s in students if s.id == student_id), None)
        if target is None:
            raise StudentNotFoundError(f"No student with ID {student_id}.")
        if name:
            target.name = validate_name(name)
        if email:
            email = validate_email(email)
            self._ensure_unique_email(students, email, ignore_id=student_id)
            target.email = email
        if age not in (None, ""):
            target.age = validate_age(age)
        if course:
            target.course = validate_course(course)
        self.repo.save_all(students)
        return target

    # ---------- Delete ----------
    def delete(self, student_id: int) -> Student:
        students = self.repo.load_all()
        target = next((s for s in students if s.id == student_id), None)
        if target is None:
            raise StudentNotFoundError(f"No student with ID {student_id}.")
        students.remove(target)
        self.repo.save_all(students)
        return target

    # ---------- Search ----------
    def search(self, keyword: str) -> List[Student]:
        kw = keyword.strip().lower()
        if not kw:
            raise ValidationError("Search keyword cannot be empty.")
        return [s for s in self.list_all()
                if kw in s.name.lower() or kw in s.email.lower()
                or kw in s.course.lower() or kw == str(s.id)]

    @staticmethod
    def _ensure_unique_email(students, email, ignore_id=None):
        for s in students:
            if s.email == email and s.id != ignore_id:
                raise ValidationError(f"Email '{email}' is already registered.")
