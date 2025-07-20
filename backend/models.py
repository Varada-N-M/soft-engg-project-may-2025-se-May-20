from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

# User roles
class UserRole(Enum):
    ADMIN = "admin"
    CHILD = "child"
    PARENT = "parent"
    PRINCIPAL = "principal"
    TEACHER = "teacher"
    ORGANIZATION = "organization"


# --- DB Models --- #

class Organization(db.Model):
    __tablename__ = 'organization'
    
    org_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    creator = db.relationship('Users', foreign_keys=[created_by], backref='organizations_created')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Organization {self.name}>'


class Teacher(db.Model):
    __tablename__ = 'teacher'
    
    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    subject = db.Column(db.String(255))
    school_id = db.Column(db.Integer, db.ForeignKey('school.school_id'), nullable=False)
    school = db.relationship('School', backref='teachers', lazy=True)
    lessons = db.relationship('LessonUpdates', backref='teacher', lazy=True)
    teacher_children = db.relationship('TeacherChild', backref='teacher', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Teacher {self.subject}>'


class LessonUpdates(db.Model):
    __tablename__ = 'lesson_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    lesson = db.Column(db.String(255))
    summary = db.Column(db.Text)

    def __repr__(self):
        return f'<LessonUpdate {self.lesson}>'


class Child(db.Model):
    __tablename__ = 'child'
    
    child_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    dob = db.Column(db.Date)
    class_ = db.Column('class', db.Integer)
    school_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    unique_key = db.Column(db.String(255))
    is_linked = db.Column(db.Boolean, default=False)  # Indicates if the child is linked to a parent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    streak = db.Column(db.Integer, default=0)
    xp_points = db.Column(db.Integer, default=0)

    habits = db.relationship('Habit', backref='child', lazy=True)
    badges = db.relationship('Badge', backref='child', lazy=True)
    skills = db.relationship('Skill', backref='child', lazy=True)
    todos = db.relationship('ToDoList', backref='child', lazy=True)
    gratitudes = db.relationship('GratitudeEntries', backref='child', lazy=True)
    teacher_links = db.relationship('TeacherChild', backref='child', lazy=True)
    parent_links = db.relationship('ParentChild', backref='child', lazy=True)

    def __repr__(self):
        return f'<Child {self.user_id}>'


class Habit(db.Model):
    __tablename__ = 'habit'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    habit_xp = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Habit {self.habit}>'


class HabitCompletion(db.Model):
    __tablename__ = 'habit_completion'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.Date, default=datetime.utcnow().date)

    def __repr__(self):
        return f'<HabitCompletion habit_id={self.habit_id} date={self.completion_date}>'


class Badge(db.Model):
    __tablename__ = 'badge'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    badge = db.Column(db.String(255))
    level = db.Column(db.String(255))
    is_earned = db.Column(db.Boolean, default=False)
    badge_xp = db.Column(db.Integer, default=0)
    earned_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Badge {self.badge}>'


class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    skill_name = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    is_learned = db.Column(db.Boolean, default=False)
    skill_xp = db.Column(db.Integer, default=0)
    completion_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Skill {self.skill_name}>'


class ToDoList(db.Model):
    __tablename__ = 'to_do_list'

    list_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    to_do = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_done = db.Column(db.Boolean, default=False)
    is_daily = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<ToDo {self.to_do}>'


class GratitudeEntries(db.Model):
    __tablename__ = 'gratitude_entries'

    entry_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gratitude_text = db.Column(db.Text)

    def __repr__(self):
        return f'<GratitudeEntry {self.entry_id}>'


class TeacherChild(db.Model):
    __tablename__ = 'teacher_child'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    linked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TeacherChild {self.teacher_id}-{self.child_id}>'


class Parent(db.Model):
    __tablename__ = 'parent'

    parent_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    phone_number = db.Column(db.String(20))
    parent_links = db.relationship('ParentChild', backref='parent', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Parent {self.user_id}>'


class ParentChild(db.Model):
    __tablename__ = 'parent_child'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.parent_id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    linked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ParentChild {self.parent_id}-{self.child_id}>'

class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role_type = db.Column(db.Enum(UserRole), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    teacher = db.relationship('Teacher', backref='user', uselist=False)
    child = db.relationship('Child', backref='user', uselist=False)
    parent = db.relationship('Parent', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.email}>'
    

class School(db.Model):
    __tablename__ = 'school'

    school_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    creator = db.relationship('Users', foreign_keys=[created_by], backref='schools_created')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<School {self.name}>'