from models import db, Users, Teacher, Child, Parent, School, LessonUpdates, TeacherChild, ParentChild, UserRole, CommonSkill, SkillCompleted
from config import Config
from flask import Flask
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timezone
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_seed_data():
    """Create comprehensive seed data for development and testing"""
    print("🌱 Starting database seeding...")
    
    # Create Schools
    print("📚 Creating schools...")
    schools_data = [
        {"name": "Springfield Elementary", "address": "123 Main St, Springfield", "phone_number": "+1-555-0101"},
        {"name": "Riverside High School", "address": "456 Oak Ave, Riverside", "phone_number": "+1-555-0102"}
    ]
    
    schools = []
    for school_data in schools_data:
        school = School(
            name=school_data["name"],
            address=school_data["address"],
            phone_number=school_data["phone_number"],
            created_by=1  # Will be set to admin user ID after creation
        )
        schools.append(school)
        db.session.add(school)
    
    # Create Users
    print("👥 Creating users with authentication...")
    users_data = [
        # Admin
        {"email": "admin@school.edu", "password": "admin123", "first_name": "Admin", "last_name": "User", "role": UserRole.ADMIN},
        
        # Teachers
        {"email": "mariah.jace@school.edu", "password": "teacher123", "first_name": "Mariah", "last_name": "Jace", "role": UserRole.PRINCIPAL},
        {"email": "sarah.johnson@school.edu", "password": "teacher123", "first_name": "Sarah", "last_name": "Johnson", "role": UserRole.TEACHER},
        {"email": "mike.davis@school.edu", "password": "teacher123", "first_name": "Mike", "last_name": "Davis", "role": UserRole.TEACHER},
        {"email": "lisa.wang@school.edu", "password": "teacher123", "first_name": "Lisa", "last_name": "Wang", "role": UserRole.TEACHER},
        
        # Students
        {"email": "emma.brown@student.edu", "password": "student123", "first_name": "Emma", "last_name": "Brown", "role": UserRole.CHILD},
        {"email": "noah.wilson@student.edu", "password": "student123", "first_name": "Noah", "last_name": "Wilson", "role": UserRole.CHILD},
        {"email": "sophia.garcia@student.edu", "password": "student123", "first_name": "Sophia", "last_name": "Garcia", "role": UserRole.CHILD},
        {"email": "liam.martinez@student.edu", "password": "student123", "first_name": "Liam", "last_name": "Martinez", "role": UserRole.CHILD},
        {"email": "olivia.lee@student.edu", "password": "student123", "first_name": "Olivia", "last_name": "Lee", "role": UserRole.CHILD},
        {"email": "ethan.taylor@student.edu", "password": "student123", "first_name": "Ethan", "last_name": "Taylor", "role": UserRole.CHILD},
        
        # Parents
        {"email": "parent1@example.com", "password": "parent123", "first_name": "Jennifer", "last_name": "Brown", "role": UserRole.PARENT},
        {"email": "parent2@example.com", "password": "parent123", "first_name": "Robert", "last_name": "Wilson", "role": UserRole.PARENT},
    ]
    
    users = []
    for user_data in users_data:
        user = Users(
            email=user_data["email"],
            password=generate_password_hash(user_data["password"]),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role_type=user_data["role"],
            is_active=True
        )
        users.append(user)
        db.session.add(user)
    
    db.session.flush()  # Get user IDs
    
    # Update school created_by to admin user
    admin_user = users[0]  # First user is admin
    for school in schools:
        school.created_by = admin_user.user_id
    
    # Create Teacher Profiles
    print("🎓 Creating teacher profiles...")
    teachers_data = [
        {"user_idx": 1, "subject": "Mathematics", "school_idx": 0},  # Sarah Johnson
        {"user_idx": 2, "subject": "English Literature", "school_idx": 0},  # Mike Davis  
        {"user_idx": 3, "subject": "Science", "school_idx": 1},  # Lisa Wang
    ]
    
    teachers = []
    for teacher_data in teachers_data:
        teacher = Teacher(
            user_id=users[teacher_data["user_idx"]].user_id,
            subject=teacher_data["subject"],
            school_id=schools[teacher_data["school_idx"]].school_id
        )
        teachers.append(teacher)
        db.session.add(teacher)
    
    # Create Student Profiles
    print("🎒 Creating student profiles...")
    students_data = [
        {"user_idx": 4, "dob": date(2018, 3, 15), "class_": 1, "school": "Springfield Elementary", "gender": "Female"},  # Emma Brown
        {"user_idx": 5, "dob": date(2016, 7, 22), "class_": 3, "school": "Springfield Elementary", "gender": "Male"},    # Noah Wilson
        {"user_idx": 6, "dob": date(2014, 11, 8), "class_": 5, "school": "Springfield Elementary", "gender": "Female"}, # Sophia Garcia
        {"user_idx": 7, "dob": date(2012, 1, 30), "class_": 7, "school": "Riverside High School", "gender": "Male"},    # Liam Martinez
        {"user_idx": 8, "dob": date(2010, 9, 12), "class_": 9, "school": "Riverside High School", "gender": "Female"}, # Olivia Lee
        {"user_idx": 9, "dob": date(2008, 5, 18), "class_": 11, "school": "Riverside High School", "gender": "Male"},  # Ethan Taylor
    ]
    
    students = []
    for student_data in students_data:
        student = Child(
            user_id=users[student_data["user_idx"]].user_id,
            dob=student_data["dob"],
            class_=student_data["class_"],
            school_name=student_data["school"],
            gender=student_data["gender"],
            unique_key=f"STU{student_data['user_idx']:03d}",
            is_linked=True,
            streak=0,
            xp_points=100
        )
        students.append(student)
        db.session.add(student)
    
    # Create Parent Profiles
    print("👨‍👩‍👧‍👦 Creating parent profiles...")
    parents_data = [
        {"user_idx": 10, "phone_number": "+1-555-0201"},  # Jennifer Brown
        {"user_idx": 11, "phone_number": "+1-555-0202"},  # Robert Wilson
    ]
    
    parents = []
    for parent_data in parents_data:
        parent = Parent(
            user_id=users[parent_data["user_idx"]].user_id,
            phone_number=parent_data["phone_number"]
        )
        parents.append(parent)
        db.session.add(parent)
    
    db.session.flush()  # Get all IDs
    
    # Create Teacher-Student Relationships
    print("🔗 Creating teacher-student relationships...")
    teacher_student_links = [
        # Sarah Johnson (Math) - Elementary students
        {"teacher_idx": 0, "student_idx": 0},  # Emma (Class 1)
        {"teacher_idx": 0, "student_idx": 1},  # Noah (Class 3)  
        {"teacher_idx": 0, "student_idx": 2},  # Sophia (Class 5)
        
        # Mike Davis (English) - High school students
        {"teacher_idx": 1, "student_idx": 3},  # Liam (Class 7)
        {"teacher_idx": 1, "student_idx": 4},  # Olivia (Class 9)
        {"teacher_idx": 1, "student_idx": 5},  # Ethan (Class 11)
        
        # Lisa Wang (Science) - Mixed levels
        {"teacher_idx": 2, "student_idx": 2},  # Sophia (Class 5)
        {"teacher_idx": 2, "student_idx": 3},  # Liam (Class 7)
        {"teacher_idx": 2, "student_idx": 4},  # Olivia (Class 9)
    ]
    
    for link_data in teacher_student_links:
        link = TeacherChild(
            teacher_id=teachers[link_data["teacher_idx"]].teacher_id,
            child_id=students[link_data["student_idx"]].child_id
        )
        db.session.add(link)
    
    # Create Parent-Child Relationships
    print("👪 Creating parent-child relationships...")
    parent_child_links = [
        {"parent_idx": 0, "child_idx": 0},  # Jennifer Brown -> Emma Brown
        {"parent_idx": 1, "child_idx": 1},  # Robert Wilson -> Noah Wilson
    ]
    
    for link_data in parent_child_links:
        link = ParentChild(
            parent_id=parents[link_data["parent_idx"]].parent_id,
            child_id=students[link_data["child_idx"]].child_id
        )
        db.session.add(link)
    
    # Create Lesson Updates
    print("📝 Creating lesson updates...")
    lessons_data = [
        # Math lessons by Sarah Johnson
        {"teacher_idx": 0, "class_": 1, "day": "Monday", "subject": "Math", "lesson": "Addition Basics", "activity": "Practice adding single-digit numbers with colorful blocks and worksheets."},
        {"teacher_idx": 0, "class_": 1, "day": "Wednesday", "subject": "Math", "lesson": "Counting to 100", "activity": "Count objects in groups and practice writing numbers 1-100."},
        {"teacher_idx": 0, "class_": 3, "day": "Tuesday", "subject": "Math", "lesson": "Multiplication Tables", "activity": "Learn times tables 2, 5, and 10 through songs and games."},
        {"teacher_idx": 0, "class_": 3, "day": "Friday", "subject": "Math", "lesson": "Word Problems", "activity": "Solve simple addition and subtraction word problems using real-world examples."},
        {"teacher_idx": 0, "class_": 5, "day": "Monday", "subject": "Math", "lesson": "Fractions Introduction", "activity": "Understand halves, quarters, and thirds using pizza and pie models."},
        {"teacher_idx": 0, "class_": 5, "day": "Thursday", "subject": "Math", "lesson": "Decimal Numbers", "activity": "Learn about tenths and hundredths using money examples and place value charts."},
        
        # English lessons by Mike Davis
        {"teacher_idx": 1, "class_": 7, "day": "Monday", "subject": "English", "lesson": "Shakespeare Introduction", "activity": "Read Romeo and Juliet Act 1, Scene 1 and discuss Elizabethan language."},
        {"teacher_idx": 1, "class_": 7, "day": "Wednesday", "subject": "English", "lesson": "Creative Writing", "activity": "Write a short story using descriptive language and dialogue techniques."},
        {"teacher_idx": 1, "class_": 9, "day": "Tuesday", "subject": "English", "lesson": "Poetry Analysis", "activity": "Analyze themes and literary devices in Robert Frost's 'The Road Not Taken'."},
        {"teacher_idx": 1, "class_": 9, "day": "Friday", "subject": "English", "lesson": "Debate Skills", "activity": "Practice persuasive speaking through structured debates on current topics."},
        {"teacher_idx": 1, "class_": 11, "day": "Monday", "subject": "English", "lesson": "College Essay Writing", "activity": "Draft personal statements and practice college application essay techniques."},
        {"teacher_idx": 1, "class_": 11, "day": "Thursday", "subject": "English", "lesson": "Advanced Grammar", "activity": "Master complex sentence structures and advanced punctuation rules."},
        
        # Science lessons by Lisa Wang
        {"teacher_idx": 2, "class_": 5, "day": "Tuesday", "subject": "Science", "lesson": "Plant Life Cycles", "activity": "Observe bean seeds germination and document plant growth stages."},
        {"teacher_idx": 2, "class_": 5, "day": "Friday", "subject": "Science", "lesson": "Weather Patterns", "activity": "Create a weather station and track daily temperature, humidity, and precipitation."},
        {"teacher_idx": 2, "class_": 7, "day": "Wednesday", "subject": "Science", "lesson": "Cell Structure", "activity": "Use microscopes to observe plant and animal cells, draw and label parts."},
        {"teacher_idx": 2, "class_": 7, "day": "Thursday", "subject": "Science", "lesson": "Ecosystems", "activity": "Build a terrarium ecosystem and study predator-prey relationships."},
        {"teacher_idx": 2, "class_": 9, "day": "Monday", "subject": "Science", "lesson": "Chemical Reactions", "activity": "Conduct safe experiments to observe acids, bases, and chemical changes."},
        {"teacher_idx": 2, "class_": 9, "day": "Wednesday", "subject": "Science", "lesson": "Physics Laws", "activity": "Explore Newton's laws through hands-on experiments with motion and force."},
        
        # Additional cross-curricular lessons
        {"teacher_idx": 0, "class_": 2, "day": "Tuesday", "subject": "Math", "lesson": "Shapes and Geometry", "activity": "Identify 2D and 3D shapes in the classroom and create shape art projects."},
        {"teacher_idx": 1, "class_": 8, "day": "Friday", "subject": "English", "lesson": "Research Skills", "activity": "Learn to evaluate sources and cite information for research projects."},
        {"teacher_idx": 2, "class_": 6, "day": "Monday", "subject": "Science", "lesson": "Solar System", "activity": "Create a scale model of the solar system and learn planet characteristics."},
    ]
    
    for lesson_data in lessons_data:
        lesson = LessonUpdates(
            teacher_id=teachers[lesson_data["teacher_idx"]].teacher_id,
            class_=lesson_data["class_"],
            day=lesson_data["day"],
            subject=lesson_data["subject"],
            lesson=lesson_data["lesson"],
            activity=lesson_data["activity"]
        )
        db.session.add(lesson)
    
    # seed common skill data
    common_skills = [
        {"skill_name": "Time Management", "skill_type": "regular", "video_url": "https://www.youtube.com/watch?v=DWvJk9bNDWo", "skill_xp": 50},
        {"skill_name": "Self Awareness", "skill_type": "regular", "video_url": "https://www.youtube.com/watch?v=OGVt0sgRXPM", "skill_xp": 50},
        {"skill_name": "Anger Management", "skill_type": "regular", "video_url": "https://www.youtube.com/watch?v=lxxpDF45TPA", "skill_xp": 50},
        {"skill_name": "Financial Literacy", "skill_type": "regular", "video_url": "https://www.youtube.com/watch?v=aRcXutXvfmM", "skill_xp": 50},

        {"skill_name": "Making a Simple Sandwich", "skill_type": "weekly", "video_url": "https://www.youtube.com/watch?v=byZlWHEZWSM", "skill_xp": 100},
        {"skill_name": "Cleaning Up After Cooking", "skill_type": "weekly", "video_url": "https://www.youtube.com/watch?v=_huP1lCMnlQ", "skill_xp": 100},
        {"skill_name": "Grow a Plant from Kitchen Scraps", "skill_type": "weekly", "video_url": "https://www.youtube.com/watch?v=dlp_MgVJCYc", "skill_xp": 100},
        {"skill_name": "Code Your First Simple Game with Scratch", "skill_type": "weekly", "video_url": "https://www.youtube.com/watch?v=1jHvXakt1qw", "skill_xp": 100},
    ]

    for skill_data in common_skills:
        skill = CommonSkill(
            skill_name=skill_data["skill_name"],
            skill_type=skill_data["skill_type"],
            video_url=skill_data["video_url"],
            skill_xp=skill_data["skill_xp"]
        )
        db.session.add(skill)
    
    # make two skill completed
    skill1 = SkillCompleted(
        child_id=2,
        skill_id=1,
        is_learned=True,
        completion_date=datetime.now(timezone.utc)
    )
    skill2 = SkillCompleted(
        child_id=2,
        skill_id=2,
        is_learned=True,
        completion_date=datetime.now(timezone.utc)
    )
    db.session.add(skill1)
    db.session.add(skill2)

    # Commit all data
    db.session.commit()
    print("✅ Database seeding completed successfully!")
    print(f"📊 Created:")
    print(f"   • {len(schools)} schools")
    print(f"   • {len(users)} users with authentication")
    print(f"   • {len(teachers)} teachers")
    print(f"   • {len(students)} students") 
    print(f"   • {len(parents)} parents")
    print(f"   • {len(lessons_data)} lesson updates")
    print(f"   • Teacher-student and parent-child relationships")

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if os.path.exists(db_path):
        confirm = input("WARNING: This will DELETE and RECREATE the database. Type 'yes' to continue: ")
        if confirm.lower() == 'yes':
            os.remove(db_path)
            print("Old database removed.")
        else:
            print("Migration cancelled.")
            exit(0)
    
    with app.app_context():
        print("🗄️  Dropping and creating database tables...")
        db.drop_all()
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create seed data
        try:
            create_seed_data()
        except Exception as e:
            print(f"❌ Error creating seed data: {e}")
            db.session.rollback()
            raise
        
        print("\n🎉 Database migration and seeding completed!")
        print("\n📋 Login Credentials:")
        print("Admin: admin@school.edu / admin123")
        print("Teacher: sarah.johnson@school.edu / teacher123")
        print("Student: emma.brown@student.edu / student123") 
        print("Parent: parent1@example.com / parent123")
