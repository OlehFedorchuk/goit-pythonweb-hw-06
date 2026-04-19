from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject", cascade="all, delete-orphan")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade = Column(Integer, nullable=False)
    grade_date = Column(Date, default=date.today, nullable=False)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")