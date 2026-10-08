"""Student Grade Management System.

Create students, add grades (0-100), compute averages, letter grades,
pass/fail status, honor roll detection and printable summary reports.
"""

import math

MIN_GRADE = 0.0
MAX_GRADE = 100.0
PASSING_AVERAGE = 60.0
HONOR_ROLL_AVERAGE = 90.0
FAILING_LETTER = "F"
# (minimum average, letter) from the highest to the lowest boundary.
LETTER_BOUNDARIES = ((90.0, "A"), (80.0, "B"), (70.0, "C"), (60.0, "D"))
NOT_AVAILABLE = "N/A"


class Student:
    """A student with an ID, a name and a list of numeric grades."""

    def __init__(self, student_id, name):
        """Create a student.

        Raises:
            ValueError: if the ID or the name is empty or not a string.
        """
        self.student_id = self._validate_text(student_id, "Student ID")
        self.name = self._validate_text(name, "Student name")
        self.grades = []

    @staticmethod
    def _validate_text(value, field_name):
        """Return the stripped text or raise ValueError if it is empty."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        return value.strip()

    @staticmethod
    def _validate_grade(grade):
        """Return the grade as float or raise ValueError if it is invalid."""
        is_number = isinstance(grade, (int, float)) and not isinstance(grade, bool)
        if not is_number or math.isnan(grade):
            raise ValueError(f"Grade {grade!r} is not a valid number.")
        if not MIN_GRADE <= grade <= MAX_GRADE:
            raise ValueError(
                f"Grade {grade} is out of range ({MIN_GRADE:g}-{MAX_GRADE:g})."
            )
        return float(grade)

    def add_grade(self, grade):
        """Add a grade between 0 and 100.

        Raises:
            ValueError: if the grade is not numeric or out of range.
        """
        self.grades.append(self._validate_grade(grade))

    def remove_grade_by_value(self, grade):
        """Remove the first grade equal to the given value.

        Raises:
            ValueError: if the value is invalid or not in the grade list.
        """
        value = self._validate_grade(grade)
        if value not in self.grades:
            raise ValueError(f"Grade {value} was not found for {self.name}.")
        self.grades.remove(value)

    def remove_grade_by_index(self, index):
        """Remove the grade at the given zero-based index.

        Raises:
            ValueError: if the index is not an integer or out of bounds.
        """
        if not isinstance(index, int) or isinstance(index, bool):
            raise ValueError(f"Index {index!r} must be an integer.")
        if not 0 <= index < len(self.grades):
            raise ValueError(
                f"Index {index} is out of bounds (0-{len(self.grades) - 1})."
                if self.grades
                else "There are no grades to remove."
            )
        del self.grades[index]

    def average(self):
        """Return the average of all grades.

        Raises:
            ValueError: if the student has no grades yet.
        """
        if not self.grades:
            raise ValueError(f"{self.name} has no grades yet.")
        return sum(self.grades) / len(self.grades)

    def letter_grade(self):
        """Return the letter grade (A-F) for the current average."""
        average = self.average()
        for minimum, letter in LETTER_BOUNDARIES:
            if average >= minimum:
                return letter
        return FAILING_LETTER

    def has_passed(self):
        """Return True if the average is 60 or higher."""
        return self.average() >= PASSING_AVERAGE

    def pass_status(self):
        """Return 'Passed' or 'Failed'."""
        return "Passed" if self.has_passed() else "Failed"

    def is_honor_roll(self):
        """Return True (boolean flag) if the average is 90 or higher."""
        return bool(self.grades) and self.average() >= HONOR_ROLL_AVERAGE

    def summary_report(self):
        """Return a formatted summary report of the student."""
        has_grades = bool(self.grades)
        average = f"{self.average():.2f}" if has_grades else NOT_AVAILABLE
        letter = self.letter_grade() if has_grades else NOT_AVAILABLE
        status = self.pass_status() if has_grades else NOT_AVAILABLE
        lines = (
            "=" * 34,
            f"Student ID    : {self.student_id}",
            f"Student Name  : {self.name}",
            f"Grades Count  : {len(self.grades)}",
            f"Average Grade : {average}",
            f"Letter Grade  : {letter}",
            f"Status        : {status}",
            f"Honor Roll    : {self.is_honor_roll()}",
            "=" * 34,
        )
        return "\n".join(lines)


def attempt(description, action, *args):
    """Run an action and print a clear error message instead of crashing."""
    try:
        result = action(*args)
    except ValueError as error:
        print(f"[ERROR] {description}: {error}")
        return None
    print(f"[OK] {description}")
    return result


def main():
    """Demonstrate every requirement of the grade management system."""
    print("--- 1. Add students (valid and invalid) ---")
    ana = attempt("Create Ana", Student, "S001", "Ana Torres")
    attempt("Create student with empty name", Student, "S002", "   ")
    attempt("Create student with empty ID", Student, "", "No Id")
    ben = attempt("Create Ben", Student, "S003", "Ben Ruiz")

    print("\n--- 2. Add grades (valid and invalid) ---")
    for grade in (95.0, 72.5, 100, 88):
        attempt(f"Add grade {grade} to Ana", ana.add_grade, grade)
    attempt("Add text grade 'Fifty' to Ana", ana.add_grade, "Fifty")
    attempt("Add grade 150 to Ana", ana.add_grade, 150)
    attempt("Add grade -5 to Ana", ana.add_grade, -5)
    for grade in (55, 40.5, 62):
        attempt(f"Add grade {grade} to Ben", ben.add_grade, grade)

    print("\n--- 3. Average, letter grade, pass/fail and honor roll ---")
    print(ana.summary_report())
    print(ben.summary_report())

    print("\n--- 4. Remove grades by value and by index ---")
    attempt("Remove grade 72.5 from Ana", ana.remove_grade_by_value, 72.5)
    attempt("Remove grade 10 (does not exist)", ana.remove_grade_by_value, 10)
    attempt("Remove grade at index 0 from Ana", ana.remove_grade_by_index, 0)
    attempt("Remove grade at index 9 (out of bounds)", ana.remove_grade_by_index, 9)
    print(ana.summary_report())

    print("\n--- 5. Student without grades ---")
    attempt("Average of student without grades",
            Student("S004", "Carla Vera").average)
    print(Student("S004", "Carla Vera").summary_report())


if __name__ == "__main__":
    main()
