# Student Management System (CLI)

A professional, menu-driven command-line application that performs full **CRUD** operations
on student records, with persistent JSON storage, search, input validation and error handling.

## Features
- **Create** – add a student (name, email, age, course)
- **Read** – list all students or view one by ID
- **Update** – edit any field (press Enter to keep the current value)
- **Delete** – remove a student with confirmation
- **Search** – by name, email, course or ID (case-insensitive, partial match)
- **Persistent storage** – data saved to `data/students.json` (atomic writes)
- **Input validation** – name, email format, age range (5–100), unique email
- **Exception handling** – missing/corrupt data file, bad input, Ctrl+C, unknown IDs
- **Zero dependencies** – Python standard library only

## Requirements
Python 3.8+

## Installation & Run
```bash
git clone https://github.com/shobika943/student-manager.git
cd student-manager
python main.py
```

## Sample Session
```
==============================
   STUDENT MANAGEMENT SYSTEM
==============================
 1. Add student
 2. View all students
 ...
Choose an option: 1
Name: Priya Kumar
Email: priya@example.com
Age: 21
Course: Python

[OK] Student added with ID 1.
```

## Project Structure
```
student-manager/
├── main.py                    # Entry point
├── student_manager/
│   ├── models.py              # Student dataclass
│   ├── validators.py          # Input validation rules
│   ├── repository.py          # JSON persistence layer
│   ├── service.py             # CRUD + search business logic
│   └── cli.py                 # Menu-driven user interface
├── tests/test_service.py      # Unit tests
├── data/                      # Runtime JSON storage (git-ignored)
└── README.md
```

## Architecture
Layered design with one-way dependencies: `CLI → Service → Repository → JSON file`.
The UI never touches storage directly, so the JSON repository can be swapped for
SQLite or CSV without changing the service or CLI.

## Running Tests
```bash
python -m unittest discover -s tests -v
```

## Validation Rules
| Field  | Rule                                         |
|--------|----------------------------------------------|
| Name   | ≥ 2 chars, letters/spaces/`.'-` only         |
| Email  | Valid format, must be unique                 |
| Age    | Integer between 5 and 100                    |
| Course | ≥ 2 characters                               |

## Release
Current version: **v1.0.0**

## License
MIT
