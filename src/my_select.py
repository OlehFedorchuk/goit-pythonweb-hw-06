from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from config import DATABASE_URL
from models import Group, Student, Teacher, Subject, Grade
from db import engine

Session = sessionmaker(bind=engine)


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


def select_1():
    
    # Find the top 5 students with the highest average grade across all subjects.
    
    with Session() as session:
        return (
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


def select_2(subject_id: int):
    
    # Find the student with the highest average grade in a specific subject.
    
    with Session() as session:
        return (
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


def select_3(subject_id: int):
    
    # Find the average grade in each group for a specific subject.
    
    with Session() as session:
        return (
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


def select_4():
    
    # Find the average grade across the entire stream (all grades in the table).
    
    with Session() as session:
        return (
            session.query(
                func.round(func.avg(Grade.grade), 2).label("average_grade")
            )
            .select_from(Grade)
            .scalar()
        )


def select_5(teacher_id: int):
    
    # Find the courses taught by a specific teacher.
    
    with Session() as session:
        return (
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


def select_6(group_id: int):
    
    # Find the list of students in a specific group.
    
    with Session() as session:
        return (
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


def select_7(group_id: int, subject_id: int):
    
    # Find the grades of students in a specific group for a specific subject.
    
    with Session() as session:
        return (
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


def select_8(teacher_id: int):
    
    # Find the average grade given by a specific teacher across their subjects.
    
    with Session() as session:
        return (
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


def select_9(student_id: int):
    
    # Find the list of courses attended by a specific student.
    
    with Session() as session:
        return (
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


def select_10(student_id: int, teacher_id: int):
    
    # Find the list of courses taught by a specific teacher to a specific student.
    

    with Session() as session:
        return (
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


def select_11(student_id: int, teacher_id: int):
    
    # Find the average grade that a specific teacher gives to a specific student.
    
    with Session() as session:
        return (
            session.query(
                Student.name.label("student"),
                Teacher.name.label("teacher"),
                func.round(func.avg(Grade.grade), 2).label("average_grade"),
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
            .group_by(Student.name, Teacher.name)
            .first()
        )


def select_12(group_id: int, subject_id: int):
    
    # Find the grades of students in a specific group for a specific subject at the last lesson.
    
    with Session() as session:
        last_lesson_date = (
            session.query(func.max(Grade.grade_date))
            .select_from(Grade)
            .join(Student, Student.id == Grade.student_id)
            .filter(
                and_(
                    Student.group_id == group_id,
                    Grade.subject_id == subject_id,
                )
            )
            .scalar()
        )

        if not last_lesson_date:
            return []

        return (
            session.query(
                Group.name.label("group_name"),
                Subject.name.label("subject"),
                Student.name.label("student"),
                Grade.grade,
                Grade.grade_date,
            )
            .join(Student, Student.id == Grade.student_id)
            .join(Group, Group.id == Student.group_id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(
                and_(
                    Group.id == group_id,
                    Subject.id == subject_id,
                    Grade.grade_date == last_lesson_date,
                )
            )
            .order_by(Student.name)
            .all()
        )


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

    print(f"\nAverage grade for all grades: {select_4()}")

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

    result_11 = select_11(1, 1)
    print_table(
        "Average grade given by teacher to student",
        [result_11] if result_11 else [],
        ["Student", "Teacher", "Average grade"],
    )

    print_table(
        "Grades at the last lesson",
        select_12(1, 1),
        ["Group", "Subject", "Student", "Grade", "Date"],
    )