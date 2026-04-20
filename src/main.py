
import argparse
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from models import Teacher, Group, Student, Subject, Grade
from db import SessionLocal


MODEL_MAP = {
    "1": ("Teacher", Teacher),
    "2": ("Group", Group),
    "3": ("Student", Student),
    "4": ("Subject", Subject),
    "5": ("Grade", Grade),
}


ACTION_MAP = {
    "1": "create",
    "2": "list",
    "3": "update",
    "4": "remove",
    "0": "exit",
}


def print_main_menu():
    print("""
=============================
   University Database CLI
=============================

Choose an action:
1. Create record   - add a new record
2. List records    - show all records
3. Update record   - edit an existing record
4. Remove record   - delete a record
0. Exit            - close the program
""")


def print_model_menu():
    print("""
Choose a model:
1. Teacher   - teacher
2. Group     - student group
3. Student   - student
4. Subject   - subject
5. Grade     - grade
""")


def list_entities(session, model):
    records = session.query(model).all()
    if not records:
        print("No records found.")
        return

    for record in records:
        print(record)


def create_entity(session, model_name):
    if model_name == "Teacher":
        name = input("Enter teacher name: ")
        entity = Teacher(name=name)

    elif model_name == "Group":
        name = input("Enter group name: ")
        entity = Group(name=name)

    elif model_name == "Student":
        name = input("Enter student name: ")
        group_id = int(input("Enter group id: "))
        entity = Student(name=name, group_id=group_id)

    elif model_name == "Subject":
        name = input("Enter subject name: ")
        teacher_id = int(input("Enter teacher id: "))
        entity = Subject(name=name, teacher_id=teacher_id)

    elif model_name == "Grade":
        student_id = int(input("Enter student id: "))
        subject_id = int(input("Enter subject id: "))
        grade = int(input("Enter grade: "))
        grade_date_input = input("Enter grade date (YYYY-MM-DD) or leave empty: ").strip()
        grade_date = (
            datetime.strptime(grade_date_input, "%Y-%m-%d").date()
            if grade_date_input
            else datetime.today().date()
        )
        entity = Grade(
            student_id=student_id,
            subject_id=subject_id,
            grade=grade,
            grade_date=grade_date,
        )
    else:
        print("Unknown model.")
        return

    try:
        session.add(entity)
        session.commit()
        print(f"{model_name} created successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"Database error: {e.orig}")


def update_entity(session, model_name, model):
    entity_id = int(input("Enter record id: "))
    entity = session.query(model).filter(model.id == entity_id).first()

    if not entity:
        print(f"{model_name} with id={entity_id} not found.")
        return

    try:
        if model_name == "Teacher":
            name = input(f"Enter new name [{entity.name}]: ").strip()
            if name:
                entity.name = name

        elif model_name == "Group":
            name = input(f"Enter new group name [{entity.name}]: ").strip()
            if name:
                entity.name = name

        elif model_name == "Student":
            name = input(f"Enter new name [{entity.name}]: ").strip()
            group_id = input(f"Enter new group id [{entity.group_id}]: ").strip()

            if name:
                entity.name = name
            if group_id:
                entity.group_id = int(group_id)

        elif model_name == "Subject":
            name = input(f"Enter new subject name [{entity.name}]: ").strip()
            teacher_id = input(f"Enter new teacher id [{entity.teacher_id}]: ").strip()

            if name:
                entity.name = name
            if teacher_id:
                entity.teacher_id = int(teacher_id)

        elif model_name == "Grade":
            student_id = input(f"Enter new student id [{entity.student_id}]: ").strip()
            subject_id = input(f"Enter new subject id [{entity.subject_id}]: ").strip()
            grade = input(f"Enter new grade [{entity.grade}]: ").strip()
            grade_date = input(f"Enter new grade date [{entity.grade_date}] (YYYY-MM-DD): ").strip()

            if student_id:
                entity.student_id = int(student_id)
            if subject_id:
                entity.subject_id = int(subject_id)
            if grade:
                entity.grade = int(grade)
            if grade_date:
                entity.grade_date = datetime.strptime(grade_date, "%Y-%m-%d").date()

        session.commit()
        print(f"{model_name} updated successfully.")

    except IntegrityError as e:
        session.rollback()
        print(f"Database error: {e.orig}")


def remove_entity(session, model_name, model):
    entity_id = int(input("Enter record id to remove: "))
    entity = session.query(model).filter(model.id == entity_id).first()

    if not entity:
        print(f"{model_name} with id={entity_id} not found.")
        return

    try:
        if model_name == "Group":
            students_count = session.query(Student).filter(Student.group_id == entity_id).count()
            if students_count > 0:
                print(f"Cannot remove Group. It contains {students_count} students.")
                return

        if model_name == "Teacher":
            subjects_count = session.query(Subject).filter(Subject.teacher_id == entity_id).count()
            if subjects_count > 0:
                print(f"Cannot remove Teacher. They have {subjects_count} subjects.")
                return

        if model_name == "Student":
            grades_count = session.query(Grade).filter(Grade.student_id == entity_id).count()
            if grades_count > 0:
                print(f"Cannot remove Student. They have {grades_count} grades.")
                return

        if model_name == "Subject":
            grades_count = session.query(Grade).filter(Grade.subject_id == entity_id).count()
            if grades_count > 0:
                print(f"Cannot remove Subject. It has {grades_count} grades.")
                return

        session.delete(entity)
        session.commit()
        print(f"{model_name} removed successfully.")

    except IntegrityError as e:
        session.rollback()
        print(f"Database error: {e.orig}")


def interactive_menu():
    with SessionLocal() as session:
        while True:
            print_main_menu()
            action_choice = input("Select action: ").strip()

            action = ACTION_MAP.get(action_choice)
            if not action:
                print("Invalid action.\n")
                continue

            if action == "exit":
                print("Goodbye!")
                break

            print_model_menu()
            model_choice = input("Select model: ").strip()

            model_data = MODEL_MAP.get(model_choice)
            if not model_data:
                print("Invalid model.\n")
                continue

            model_name, model = model_data

            if action == "create":
                create_entity(session, model_name)
            elif action == "list":
                list_entities(session, model)
            elif action == "update":
                update_entity(session, model_name, model)
            elif action == "remove":
                remove_entity(session, model_name, model)

            input("\nPress Enter to continue...")


def cli_mode():
    parser = argparse.ArgumentParser(description="University database CLI")
    parser.add_argument(
        "--menu",
        action="store_true",
        help="Run interactive menu mode"
    )
    args = parser.parse_args()

    if args.menu:
        interactive_menu()
    else:
        print("Run with: python main.py --menu")


if __name__ == "__main__":
    cli_mode()