from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Organization(db.Model):
    __tablename__ = 'organization'
    
    org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    # Who created this organization
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    # Creator relationship
    creator = db.relationship('Users', foreign_keys=[created_by], backref='organizations_created')
    # Users belonging to this organization
    users = db.relationship('Users', backref='organization', foreign_keys='Users.org_id')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Teacher(db.Model):
    __tablename__ = 'teacher'
    
    teacher_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    subject = db.Column(db.String(255))
    lessons = db.relationship('LessonUpdates', backref='teacher', lazy=True)
    teacher_children = db.relationship('TeacherChild', backref='teacher', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LessonUpdates(db.Model):
    __tablename__ = 'lesson_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(UUID(as_uuid=True), db.ForeignKey('teacher.teacher_id'))
    lesson = db.Column(db.String(255))
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Child(db.Model):
    __tablename__ = 'child'
    
    child_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    dob = db.Column(db.Integer)
    class_ = db.Column('class', db.Integer)
    school = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    unique = db.Column(db.String(255))
    habits = db.relationship('Habit', backref='child', lazy=True)
    badges = db.relationship('Badge', backref='child', lazy=True)
    skills = db.relationship('Skill', backref='child', lazy=True)
    todos = db.relationship('ToDoList', backref='child', lazy=True)
    gratitudes = db.relationship('GratitudeEntries', backref='child', lazy=True)
    teacher_links = db.relationship('TeacherChild', backref='child', lazy=True)
    parent_links = db.relationship('ParentChild', backref='child', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Habit(db.Model):
    __tablename__ = 'habit'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(UUID(as_uuid=True), db.ForeignKey('child.child_id'))
    habit = db.Column(db.String(255))
    is_daily = db.Column(db.String(10))
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date when the habit was recorded


class Badge(db.Model):
    __tablename__ = 'badge'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(UUID(as_uuid=True), db.ForeignKey('child.child_id'))
    badge = db.Column(db.String(255))
    level = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Date when the badge was awarded


class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(UUID(as_uuid=True), db.ForeignKey('child.child_id'))
    skill_name = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    is_learned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date when the skill was added
    # Date when the skill was completed
    completion_date = db.Column(db.DateTime, nullable=True)


class ToDoList(db.Model):
    __tablename__ = 'to_do_list'

    list_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    child_id = db.Column(UUID(as_uuid=True), db.ForeignKey('child.child_id'))
    to_do = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_done = db.Column(db.Boolean, default=False)
    is_daily = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)  # Date when the task was completed
    
class GratitudeEntries(db.Model):
    __tablename__ = 'gratitude_entries'

    entry_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    child_id = db.Column(UUID(as_uuid=True), db.ForeignKey('child.child_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gratitude_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=True)  # Date when the task was completed



class TeacherChild(db.Model):
    __tablename__ = 'teacher_child'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(UUID(as_uuid=True), db.ForeignKey('teacher.teacher_id'))
    child_id = db.Column(UUID(as_uuid=True), db.ForeignKey('child.child_id'))
    linked_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Parent(db.Model):
    __tablename__ = 'parent'

    parent_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    phone_number = db.Column(db.String(20))
    parent_links = db.relationship('ParentChild', backref='parent', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ParentChild(db.Model):
    __tablename__ = 'parent_child'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey('parent.parent_id'))
    child_id = db.Column(UUID(as_uuid=True), db.ForeignKey('child.child_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    role_type = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    # Organization this user belongs to
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.org_id'))
    # One-to-one relationships for roles
    teacher = db.relationship('Teacher', backref='user', uselist=False)
    child = db.relationship('Child', backref='user', uselist=False)
    parent = db.relationship('Parent', backref='user', uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)