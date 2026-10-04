import os
import tempfile
import unittest

from student_manager.repository import JsonRepository, StorageError
from student_manager.service import StudentNotFoundError, StudentService
from student_manager.validators import ValidationError


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "s.json")
        self.svc = StudentService(JsonRepository(self.path))

    def tearDown(self):
        self.tmp.cleanup()

    def _add(self, email="a@b.com"):
        return self.svc.add("john doe", email, "20", "Python")

    def test_create_and_read(self):
        s = self._add()
        self.assertEqual(s.name, "John Doe")
        self.assertEqual(self.svc.get(s.id).email, "a@b.com")

    def test_persistence(self):
        self._add()
        again = StudentService(JsonRepository(self.path))
        self.assertEqual(len(again.list_all()), 1)

    def test_update(self):
        s = self._add()
        self.svc.update(s.id, course="Java", age="22")
        self.assertEqual(self.svc.get(s.id).course, "Java")
        self.assertEqual(self.svc.get(s.id).age, 22)

    def test_delete(self):
        s = self._add()
        self.svc.delete(s.id)
        with self.assertRaises(StudentNotFoundError):
            self.svc.get(s.id)

    def test_search(self):
        self._add()
        self.assertEqual(len(self.svc.search("python")), 1)
        self.assertEqual(len(self.svc.search("zzz")), 0)

    def test_validation(self):
        with self.assertRaises(ValidationError):
            self.svc.add("J", "bad-email", "20", "x")
        with self.assertRaises(ValidationError):
            self.svc.add("John", "j@x.com", "-3", "Python")

    def test_duplicate_email(self):
        self._add()
        with self.assertRaises(ValidationError):
            self._add()

    def test_corrupt_file(self):
        with open(self.path, "w") as f:
            f.write("{not json")
        with self.assertRaises(StorageError):
            self.svc.list_all()


if __name__ == "__main__":
    unittest.main()
