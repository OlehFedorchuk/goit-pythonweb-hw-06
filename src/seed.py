from random import randint, choice, sample
from datetime import date, timedelta
from faker import Faker
from db import engine, SessionLocal
from models import Base, Group, Student, Teacher, Subject, Grade

fake = Faker()


def random_date_within_last_year() -> date:
    return date.today() - timedelta(days=randint(1, 365))


def seed_database():
    session = SessionLocal()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        Base.metadata.create_all(bind=engine)

        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()

        groups = [
            Group(name="Group A"),
            Group(name="Group B"),
            Group(name="Group C"),
        ]
        session.add_all(groups)
        session.commit()

        teachers = [Teacher(name=fake.name()) for _ in range(randint(3, 5))]
        session.add_all(teachers)
        session.commit()

        subject_names = [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "English",
            "Programming",
            "Databases",
        ]
        selected_subjects = sample(subject_names, randint(5, 8))

        subjects = [
            Subject(name=name, teacher_id=choice(teachers).id)
            for name in selected_subjects
        ]
        session.add_all(subjects)
        session.commit()

        students = [
            Student(name=fake.name(), group_id=choice(groups).id)
            for _ in range(randint(30, 50))
        ]
        session.add_all(students)
        session.commit()

        grades = []
        for student in students:
            for _ in range(randint(10, 20)):
                grades.append(
                    Grade(
                        student_id=student.id,
                        subject_id=choice(subjects).id,
                        grade=randint(60, 100),
                        grade_date=random_date_within_last_year(),
                    )
                )

        session.add_all(grades)
        session.commit()

        print("Database seeded successfully!")

    except Exception as e:
        session.rollback()
        print(f"Seeding error: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    seed_database()