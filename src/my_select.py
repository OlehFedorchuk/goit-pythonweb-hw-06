from sqlalchemy import func, desc, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Group, Student, Teacher, Subject, Grade

from tabulate import tabulate

DATABASE_URL = "postgresql+psycopg://Admin:Password@localhost:5432/university_db"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    with Session() as session:
        result = (
            session.query(
                Student.id,
                Student.name,
                func.round(func.avg(Grade.grade), 2).label("average_grade"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .group_by(Student.id, Student.name)
            .order_by(desc("average_grade"))
            .limit(5)
            .all()
        )
        return result


def select_2(subject_id: int):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    """
    with Session() as session:
        result = (
            session.query(
                Student.id,
                Student.name,
                Subject.name.label("subject"),
                func.round(func.avg(Grade.grade), 2).label("average_grade"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Student.id, Student.name, Subject.name)
            .order_by(desc("average_grade"))
            .first()
        )
        return result


def select_3(subject_id: int):
    """
    Знайти середній бал у групах з певного предмета.
    """
    with Session() as session:
        result = (
            session.query(
                Group.id,
                Group.name,
                Subject.name.label("subject"),
                func.round(func.avg(Grade.grade), 2).label("average_grade"),
            )
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id, Group.name, Subject.name)
            .order_by(Group.name)
            .all()
        )
        return result


def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    with Session() as session:
        result = (
            session.query(
                func.round(func.avg(Grade.grade), 2).label("average_grade")
            )
            .select_from(Grade)
            .scalar()
        )
        return result


def select_5(teacher_id: int):
    """
    Знайти які курси читає певний викладач.
    """
    with Session() as session:
        result = (
            session.query(
                Teacher.name.label("teacher"),
                Subject.id,
                Subject.name.label("subject"),
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .filter(Teacher.id == teacher_id)
            .order_by(Subject.name)
            .all()
        )
        return result


def select_6(group_id: int):
    """
    Знайти список студентів у певній групі.
    """
    with Session() as session:
        result = (
            session.query(
                Student.id,
                Student.name,
                Group.name.label("group_name"),
            )
            .join(Group, Group.id == Student.group_id)
            .filter(Group.id == group_id)
            .order_by(Student.name)
            .all()
        )
        return result


def select_7(group_id: int, subject_id: int):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    with Session() as session:
        result = (
            session.query(
                Student.name.label("student"),
                Group.name.label("group_name"),
                Subject.name.label("subject"),
                Grade.grade,
                Grade.grade_date,
            )
            .join(Group, Group.id == Student.group_id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(
                and_(
                    Group.id == group_id,
                    Subject.id == subject_id,
                )
            )
            .order_by(Student.name, Grade.grade_date)
            .all()
        )
        return result


def select_8(teacher_id: int):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    with Session() as session:
        result = (
            session.query(
                Teacher.name.label("teacher"),
                func.round(func.avg(Grade.grade), 2).label("average_grade"),
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(Teacher.id == teacher_id)
            .group_by(Teacher.name)
            .first()
        )
        return result


def select_9(student_id: int):
    """
    Знайти список курсів, які відвідує певний студент.
    """
    with Session() as session:
        result = (
            session.query(
                Student.name.label("student"),
                Subject.id,
                Subject.name.label("subject"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Student.id == student_id)
            .distinct()
            .order_by(Subject.name)
            .all()
        )
        return result


def select_10(student_id: int, teacher_id: int):
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    with Session() as session:
        result = (
            session.query(
                Student.name.label("student"),
                Teacher.name.label("teacher"),
                Subject.id,
                Subject.name.label("subject"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .join(Teacher, Teacher.id == Subject.teacher_id)
            .filter(
                and_(
                    Student.id == student_id,
                    Teacher.id == teacher_id,
                )
            )
            .distinct()
            .order_by(Subject.name)
            .all()
        )
        return result
def print_table(title, data, headers):
    print(f"\n{title}")
    if not data:
        print("No data found")
        return

    rows = []
    for row in data:
        if hasattr(row, "_mapping"):
            rows.append(list(row._mapping.values()))
        else:
            rows.append(list(row))

    print(tabulate(rows, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    print_table(
        "Top 5 students by average grade",
        select_1(),
        ["ID", "Student", "Average grade"],
    )

    result_2 = select_2(1)
    print_table(
        "Best student in subject",
        [result_2] if result_2 else [],
        ["ID", "Student", "Subject", "Average grade"],
    )

    print_table(
        "Average grade by groups for subject",
        select_3(1),
        ["Group ID", "Group", "Subject", "Average grade"],
    )

    result_4 = select_4()
    print(f"\nAverage grade for all grades: {result_4}")

    print_table(
        "Courses taught by teacher",
        select_5(1),
        ["Teacher", "Subject ID", "Subject"],
    )

    print_table(
        "Students in group",
        select_6(1),
        ["Student ID", "Student", "Group"],
    )

    print_table(
        "Grades of students in group by subject",
        select_7(1, 1),
        ["Student", "Group", "Subject", "Grade", "Date"],
    )

    result_8 = select_8(1)
    print_table(
        "Average grade given by teacher",
        [result_8] if result_8 else [],
        ["Teacher", "Average grade"],
    )

    print_table(
        "Courses attended by student",
        select_9(1),
        ["Student", "Subject ID", "Subject"],
    )

    print_table(
        "Courses taught to student by teacher",
        select_10(1, 1),
        ["Student", "Teacher", "Subject ID", "Subject"],
    )