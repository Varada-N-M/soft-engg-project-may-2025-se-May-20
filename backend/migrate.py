from models import db, Users, Teacher, Child, Parent, School, LessonUpdates, TeacherChild, ParentChild, UserRole, CommonSkill, SkillCompleted, Habit, HabitCompletion, Badge, ToDoList, GratitudeEntries, Organization
from config import Config
from flask import Flask
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timezone, timedelta
import os
import random

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

        # Teachers
        {"email": "principal@school.edu", "password": "teacher123", "first_name": "Mariah", "last_name": "Jace", "role": UserRole.PRINCIPAL},
        {"email": "teacher1@school.edu", "password": "teacher123", "first_name": "Sarah", "last_name": "Johnson", "role": UserRole.TEACHER},
        {"email": "teacher2@school.edu", "password": "teacher123", "first_name": "Mike", "last_name": "Davis", "role": UserRole.TEACHER},
        {"email": "teacher3@school.edu", "password": "teacher123", "first_name": "Lisa", "last_name": "Wang", "role": UserRole.TEACHER},
        
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
        {"user_idx": 0, "subject": "Administration", "school_idx": 0},  # Principal Mariah Jace
        {"user_idx": 1, "subject": "Mathematics", "school_idx": 0},  # Sarah Johnson
        {"user_idx": 2, "subject": "English Literature", "school_idx": 0},  # Mike Davis  
        {"user_idx": 3, "subject": "Science", "school_idx": 0},  # Lisa Wang
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
        {"user_idx": 7, "dob": date(2012, 1, 30), "class_": 7, "school": "Springfield Elementary", "gender": "Male"},    # Liam Martinez
        {"user_idx": 8, "dob": date(2010, 9, 12), "class_": 9, "school": "Springfield Elementary", "gender": "Female"}, # Olivia Lee
        {"user_idx": 9, "dob": date(2008, 5, 18), "class_": 8, "school": "Springfield Elementary", "gender": "Male"},  # Ethan Taylor
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
        {"user_idx": 10, "phone_number": "5550201"},  # Jennifer Brown
        {"user_idx": 11, "phone_number": "5550202"},  # Robert Wilson
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
        {"teacher_idx": 1, "student_idx": 0},  # Emma (Class 1)
        {"teacher_idx": 1, "student_idx": 1},  # Noah (Class 3)  
        {"teacher_idx": 1, "student_idx": 2},  # Sophia (Class 5)
        
        # Mike Davis (English) - High school students
        {"teacher_idx": 2, "student_idx": 3},  # Liam (Class 7)
        {"teacher_idx": 2, "student_idx": 4},  # Olivia (Class 9)
        {"teacher_idx": 2, "student_idx": 5},  # Ethan (Class 11)
        
        # Lisa Wang (Science) - Mixed levels
        {"teacher_idx": 3, "student_idx": 2},  # Sophia (Class 5)
        {"teacher_idx": 3, "student_idx": 3},  # Liam (Class 7)
        {"teacher_idx": 3, "student_idx": 4},  # Olivia (Class 9)
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
        # Math lessons by Sarah Johnson (now index 1)
        {"teacher_idx": 1, "class_": 1, "day": "Monday", "subject": "Math", "lesson": "Addition Basics", "activity": "Practice adding single-digit numbers with colorful blocks and worksheets."},
        {"teacher_idx": 1, "class_": 1, "day": "Wednesday", "subject": "Math", "lesson": "Counting to 100", "activity": "Count objects in groups and practice writing numbers 1-100."},
        {"teacher_idx": 1, "class_": 3, "day": "Tuesday", "subject": "Math", "lesson": "Multiplication Tables", "activity": "Learn times tables 2, 5, and 10 through songs and games."},
        {"teacher_idx": 1, "class_": 3, "day": "Friday", "subject": "Math", "lesson": "Word Problems", "activity": "Solve simple addition and subtraction word problems using real-world examples."},
        {"teacher_idx": 1, "class_": 5, "day": "Monday", "subject": "Math", "lesson": "Fractions Introduction", "activity": "Understand halves, quarters, and thirds using pizza and pie models."},
        {"teacher_idx": 1, "class_": 5, "day": "Thursday", "subject": "Math", "lesson": "Decimal Numbers", "activity": "Learn about tenths and hundredths using money examples and place value charts."},
        
        # English lessons by Mike Davis (now index 2)
        {"teacher_idx": 2, "class_": 7, "day": "Monday", "subject": "English", "lesson": "Shakespeare Introduction", "activity": "Read Romeo and Juliet Act 1, Scene 1 and discuss Elizabethan language."},
        {"teacher_idx": 2, "class_": 7, "day": "Wednesday", "subject": "English", "lesson": "Creative Writing", "activity": "Write a short story using descriptive language and dialogue techniques."},
        {"teacher_idx": 2, "class_": 9, "day": "Tuesday", "subject": "English", "lesson": "Poetry Analysis", "activity": "Analyze themes and literary devices in Robert Frost's 'The Road Not Taken'."},
        {"teacher_idx": 2, "class_": 9, "day": "Friday", "subject": "English", "lesson": "Debate Skills", "activity": "Practice persuasive speaking through structured debates on current topics."},
        {"teacher_idx": 2, "class_": 11, "day": "Monday", "subject": "English", "lesson": "College Essay Writing", "activity": "Draft personal statements and practice college application essay techniques."},
        {"teacher_idx": 2, "class_": 11, "day": "Thursday", "subject": "English", "lesson": "Advanced Grammar", "activity": "Master complex sentence structures and advanced punctuation rules."},
        
        # Science lessons by Lisa Wang (now index 3)
        {"teacher_idx": 3, "class_": 5, "day": "Tuesday", "subject": "Science", "lesson": "Plant Life Cycles", "activity": "Observe bean seeds germination and document plant growth stages."},
        {"teacher_idx": 3, "class_": 5, "day": "Friday", "subject": "Science", "lesson": "Weather Patterns", "activity": "Create a weather station and track daily temperature, humidity, and precipitation."},
        {"teacher_idx": 3, "class_": 7, "day": "Wednesday", "subject": "Science", "lesson": "Cell Structure", "activity": "Use microscopes to observe plant and animal cells, draw and label parts."},
        {"teacher_idx": 3, "class_": 7, "day": "Thursday", "subject": "Science", "lesson": "Ecosystems", "activity": "Build a terrarium ecosystem and study predator-prey relationships."},
        {"teacher_idx": 3, "class_": 9, "day": "Monday", "subject": "Science", "lesson": "Chemical Reactions", "activity": "Conduct safe experiments to observe acids, bases, and chemical changes."},
        {"teacher_idx": 3, "class_": 9, "day": "Wednesday", "subject": "Science", "lesson": "Physics Laws", "activity": "Explore Newton's laws through hands-on experiments with motion and force."},
        
        # Additional cross-curricular lessons
        {"teacher_idx": 1, "class_": 2, "day": "Tuesday", "subject": "Math", "lesson": "Shapes and Geometry", "activity": "Identify 2D and 3D shapes in the classroom and create shape art projects."},
        {"teacher_idx": 2, "class_": 8, "day": "Friday", "subject": "English", "lesson": "Research Skills", "activity": "Learn to evaluate sources and cite information for research projects."},
        {"teacher_idx": 3, "class_": 6, "day": "Monday", "subject": "Science", "lesson": "Solar System", "activity": "Create a scale model of the solar system and learn planet characteristics."},
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

    db.session.flush()  # Get skill IDs for further operations
    
    # Create Organizations
    print("🏢 Creating organizations...")
    organizations_data = [
        {"name": "Springfield Educational District", "phone_number": "9876543210", "address": "789 Education Blvd, Springfield"},
        {"name": "Riverside Learning Institute", "phone_number": "9876543220", "address": "321 Academy St, Riverside"}
    ]
    
    organizations = []
    for org_data in organizations_data:
        org = Organization(
            name=org_data["name"],
            phone_number=org_data["phone_number"],
            address=org_data["address"],
            created_by=admin_user.user_id
        )
        organizations.append(org)
        db.session.add(org)
    
    # Create Student Habits
    print("🔄 Creating student habits...")
    habits_data = [
        # Emma Brown's habits (child_id = 1)
        {"child_idx": 0, "name": "Read for 20 minutes", "description": "Daily reading habit to improve literacy skills", "category": "Education", "habit_xp": 15},
        {"child_idx": 0, "name": "Brush teeth twice daily", "description": "Morning and evening tooth brushing", "category": "Health", "habit_xp": 10},
        {"child_idx": 0, "name": "Complete homework", "description": "Finish all assigned homework before play time", "category": "Education", "habit_xp": 20},
        
        # Noah Wilson's habits (child_id = 2)
        {"child_idx": 1, "name": "Practice math facts", "description": "10 minutes of multiplication table practice", "category": "Education", "habit_xp": 15},
        {"child_idx": 1, "name": "Exercise for 30 minutes", "description": "Physical activity like running, sports, or cycling", "category": "Health", "habit_xp": 20},
        {"child_idx": 1, "name": "Help with chores", "description": "Assist family with household responsibilities", "category": "Life Skills", "habit_xp": 12},
        
        # Sophia Garcia's habits (child_id = 3)
        {"child_idx": 2, "name": "Write in journal", "description": "Daily reflection and creative writing", "category": "Personal Growth", "habit_xp": 18},
        {"child_idx": 2, "name": "Practice piano", "description": "30 minutes of piano practice daily", "category": "Arts", "habit_xp": 25},
        {"child_idx": 2, "name": "Study science", "description": "Review science concepts and experiments", "category": "Education", "habit_xp": 20},
        
        # Liam Martinez's habits (child_id = 4)
        {"child_idx": 3, "name": "Read news articles", "description": "Stay informed with age-appropriate current events", "category": "Education", "habit_xp": 22},
        {"child_idx": 3, "name": "Code for 30 minutes", "description": "Practice programming skills", "category": "Technology", "habit_xp": 30},
        
        # Olivia Lee's habits (child_id = 5)
        {"child_idx": 4, "name": "Meditation practice", "description": "10 minutes of mindfulness meditation", "category": "Wellness", "habit_xp": 20},
        {"child_idx": 4, "name": "Volunteer work", "description": "Community service activities", "category": "Community", "habit_xp": 35},
        
        # Ethan Taylor's habits (child_id = 6)
        {"child_idx": 5, "name": "College prep study", "description": "SAT/ACT preparation and college research", "category": "Education", "habit_xp": 40},
        {"child_idx": 5, "name": "Leadership activities", "description": "Student government and leadership roles", "category": "Leadership", "habit_xp": 30},
    ]
    
    habits = []
    for habit_data in habits_data:
        habit = Habit(
            child_id=students[habit_data["child_idx"]].child_id,
            name=habit_data["name"],
            description=habit_data["description"],
            category=habit_data["category"],
            habit_xp=habit_data["habit_xp"]
        )
        habits.append(habit)
        db.session.add(habit)
    
    db.session.flush()
    
    # Create Habit Completions (last 30 days with realistic patterns)
    print("✅ Creating habit completion history...")
    today = date.today()
    habit_completions = []
    
    for habit in habits:
        # Create 30 days of completion history with varying success rates
        success_rate = random.uniform(0.4, 0.9)  # 40-90% completion rate
        for day_offset in range(30):
            completion_date = today - timedelta(days=day_offset)
            if random.random() < success_rate:
                completion = HabitCompletion(
                    child_id=habit.child_id,
                    habit_id=habit.id,
                    is_done=True,
                    completion_date=completion_date
                )
                habit_completions.append(completion)
                db.session.add(completion)
    
    # Create Student Badges
    print("🏆 Creating student badges...")
    badges_data = [
        # Emma Brown badges (child_id = 1)
        {"child_idx": 0, "badge": "Reading Star", "level": "Bronze", "is_earned": True, "badge_xp": 100},
        {"child_idx": 0, "badge": "Math Whiz", "level": "Silver", "is_earned": True, "badge_xp": 150},
        {"child_idx": 0, "badge": "Homework Hero", "level": "Bronze", "is_earned": True, "badge_xp": 100},
        {"child_idx": 0, "badge": "Creative Writer", "level": "Bronze", "is_earned": False, "badge_xp": 100},
        
        # Noah Wilson badges (child_id = 2)
        {"child_idx": 1, "badge": "Fitness Champion", "level": "Gold", "is_earned": True, "badge_xp": 200},
        {"child_idx": 1, "badge": "Helper Badge", "level": "Silver", "is_earned": True, "badge_xp": 150},
        {"child_idx": 1, "badge": "Math Master", "level": "Bronze", "is_earned": True, "badge_xp": 100},
        {"child_idx": 1, "badge": "Science Explorer", "level": "Bronze", "is_earned": False, "badge_xp": 100},
        
        # Sophia Garcia badges (child_id = 3)
        {"child_idx": 2, "badge": "Artist Extraordinaire", "level": "Gold", "is_earned": True, "badge_xp": 200},
        {"child_idx": 2, "badge": "Science Genius", "level": "Silver", "is_earned": True, "badge_xp": 150},
        {"child_idx": 2, "badge": "Journal Keeper", "level": "Bronze", "is_earned": True, "badge_xp": 100},
        {"child_idx": 2, "badge": "Leadership Star", "level": "Silver", "is_earned": False, "badge_xp": 150},
        
        # Liam Martinez badges (child_id = 4)
        {"child_idx": 3, "badge": "Tech Pioneer", "level": "Gold", "is_earned": True, "badge_xp": 200},
        {"child_idx": 3, "badge": "News Hound", "level": "Silver", "is_earned": True, "badge_xp": 150},
        {"child_idx": 3, "badge": "Critical Thinker", "level": "Bronze", "is_earned": True, "badge_xp": 100},
        
        # Olivia Lee badges (child_id = 5)
        {"child_idx": 4, "badge": "Community Champion", "level": "Gold", "is_earned": True, "badge_xp": 200},
        {"child_idx": 4, "badge": "Mindfulness Master", "level": "Silver", "is_earned": True, "badge_xp": 150},
        {"child_idx": 4, "badge": "Compassion Award", "level": "Bronze", "is_earned": True, "badge_xp": 100},
        
        # Ethan Taylor badges (child_id = 6)
        {"child_idx": 5, "badge": "Future Leader", "level": "Gold", "is_earned": True, "badge_xp": 200},
        {"child_idx": 5, "badge": "College Bound", "level": "Silver", "is_earned": True, "badge_xp": 150},
        {"child_idx": 5, "badge": "Academic Excellence", "level": "Gold", "is_earned": True, "badge_xp": 200},
    ]
    
    badges = []
    for badge_data in badges_data:
        earned_at = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90)) if badge_data["is_earned"] else None
        badge = Badge(
            child_id=students[badge_data["child_idx"]].child_id,
            badge=badge_data["badge"],
            level=badge_data["level"],
            is_earned=badge_data["is_earned"],
            badge_xp=badge_data["badge_xp"],
            earned_at=earned_at
        )
        badges.append(badge)
        db.session.add(badge)
    
    # Create Student To-Do Lists
    print("📝 Creating student to-do lists...")
    todos_data = [
        # Emma Brown todos (child_id = 1)
        {"child_idx": 0, "to_do": "Math homework - Addition practice", "description": "Complete pages 23-25 in math workbook", "is_done": True, "is_daily": False},
        {"child_idx": 0, "to_do": "Read chapter 3 of Charlotte's Web", "description": "Reading assignment for English class", "is_done": True, "is_daily": False},
        {"child_idx": 0, "to_do": "Make bed", "description": "Daily morning routine", "is_done": True, "is_daily": True},
        {"child_idx": 0, "to_do": "Pack school bag", "description": "Get ready for tomorrow", "is_done": False, "is_daily": True},
        
        # Noah Wilson todos (child_id = 2)
        {"child_idx": 1, "to_do": "Science project research", "description": "Find information about plant growth for project", "is_done": False, "is_daily": False},
        {"child_idx": 1, "to_do": "Practice multiplication tables 6-10", "description": "Math skills improvement", "is_done": True, "is_daily": False},
        {"child_idx": 1, "to_do": "Feed pet hamster", "description": "Daily pet care responsibility", "is_done": True, "is_daily": True},
        {"child_idx": 1, "to_do": "Clean room", "description": "Weekly room maintenance", "is_done": False, "is_daily": False},
        
        # Sophia Garcia todos (child_id = 3)
        {"child_idx": 2, "to_do": "Piano practice - Scales", "description": "30 minutes of scale practice", "is_done": True, "is_daily": True},
        {"child_idx": 2, "to_do": "Write in gratitude journal", "description": "Daily reflection practice", "is_done": True, "is_daily": True},
        {"child_idx": 2, "to_do": "Study for science test", "description": "Review chapters 4-6 for Friday test", "is_done": False, "is_daily": False},
        {"child_idx": 2, "to_do": "Art project sketches", "description": "Create preliminary drawings for art class", "is_done": False, "is_daily": False},
        
        # Liam Martinez todos (child_id = 4)
        {"child_idx": 3, "to_do": "Code practice - Python loops", "description": "Complete coding exercises on loops", "is_done": True, "is_daily": False},
        {"child_idx": 3, "to_do": "Read current events", "description": "Stay updated with news", "is_done": True, "is_daily": True},
        {"child_idx": 3, "to_do": "English essay draft", "description": "First draft of persuasive essay", "is_done": False, "is_daily": False},
        {"child_idx": 3, "to_do": "History presentation prep", "description": "Prepare slides for Civil Rights presentation", "is_done": False, "is_daily": False},
        
        # Olivia Lee todos (child_id = 5)
        {"child_idx": 4, "to_do": "Volunteer at food bank", "description": "Community service commitment", "is_done": True, "is_daily": False},
        {"child_idx": 4, "to_do": "Morning meditation", "description": "10 minutes of mindfulness", "is_done": True, "is_daily": True},
        {"child_idx": 4, "to_do": "Chemistry lab report", "description": "Complete analysis of yesterday's experiment", "is_done": False, "is_daily": False},
        {"child_idx": 4, "to_do": "Plan student council meeting", "description": "Prepare agenda for Friday meeting", "is_done": False, "is_daily": False},
        
        # Ethan Taylor todos (child_id = 6)
        {"child_idx": 5, "to_do": "SAT practice test", "description": "Complete full practice exam", "is_done": True, "is_daily": False},
        {"child_idx": 5, "to_do": "College application essays", "description": "Review and edit personal statements", "is_done": False, "is_daily": False},
        {"child_idx": 5, "to_do": "Leadership workshop notes", "description": "Organize notes from yesterday's workshop", "is_done": True, "is_daily": False},
        {"child_idx": 5, "to_do": "Review tomorrow's schedule", "description": "Daily planning routine", "is_done": True, "is_daily": True},
    ]
    
    todos = []
    for todo_data in todos_data:
        completion_date = datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48)) if todo_data["is_done"] else None
        todo = ToDoList(
            child_id=students[todo_data["child_idx"]].child_id,
            to_do=todo_data["to_do"],
            description=todo_data["description"],
            is_done=todo_data["is_done"],
            is_daily=todo_data["is_daily"],
            completion_date=completion_date,
            created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 7))
        )
        todos.append(todo)
        db.session.add(todo)
    
    # Create Gratitude Entries
    print("🙏 Creating gratitude entries...")
    gratitude_entries = []
    gratitude_texts = [
        "I'm grateful for my family's support in my studies",
        "Today I appreciated having good friends at school",
        "I'm thankful for my teacher's patience and help",
        "Grateful for the opportunity to learn new things every day",
        "I appreciate having access to books and learning resources",
        "Thankful for my health and ability to play sports",
        "I'm grateful for delicious meals and a warm home",
        "Appreciating the beauty of nature on my walk today",
        "Grateful for technology that helps me connect with others",
        "Thankful for challenges that help me grow stronger",
        "I appreciate having time to pursue my hobbies",
        "Grateful for the chance to help others in my community"
    ]
    
    # Create 30 days of gratitude entries for each student
    for student in students:
        for day_offset in range(30):
            if random.random() < 0.7:  # 70% chance of writing gratitude each day
                entry_date = datetime.now(timezone.utc) - timedelta(days=day_offset)
                gratitude_text = random.choice(gratitude_texts)
                entry = GratitudeEntries(
                    child_id=student.child_id,
                    gratitude_text=gratitude_text,
                    created_at=entry_date,
                    updated_at=entry_date
                )
                gratitude_entries.append(entry)
                db.session.add(entry)
    
    # Update Student XP Points and Streaks based on activities
    print("🌟 Updating student progress metrics...")
    for i, student in enumerate(students):
        # Calculate XP from habits, badges, and skills
        student_habits = [h for h in habits if h.child_id == student.child_id]
        student_badges = [b for b in badges if b.child_id == student.child_id and b.is_earned]
        
        total_habit_xp = sum(h.habit_xp for h in student_habits) * random.randint(5, 15)  # Multiple completions
        total_badge_xp = sum(b.badge_xp for b in student_badges)
        skill_xp = 200 if student.child_id in [2] else random.randint(0, 100)  # Some students completed skills
        
        total_xp = total_habit_xp + total_badge_xp + skill_xp + random.randint(50, 200)
        streak = random.randint(1, 15)  # Current active streak
        
        student.xp_points = total_xp
        student.streak = streak

    # Commit all data
    db.session.commit()
    print("✅ Database seeding completed successfully!")
    print(f"📊 Created:")
    print(f"   • {len(schools)} schools")
    print(f"   • {len(organizations)} organizations")
    print(f"   • {len(users)} users with authentication")
    print(f"   • {len(teachers)} teachers") 
    print(f"   • {len(students)} students")
    print(f"   • {len(parents)} parents")
    print(f"   • {len(lessons_data)} lesson updates")
    print(f"   • {len(habits)} student habits")
    print(f"   • {len(habit_completions)} habit completion records")
    print(f"   • {len(badges)} student badges")
    print(f"   • {len(todos)} todo items")
    print(f"   • {len(gratitude_entries)} gratitude journal entries")
    print(f"   • Teacher-student and parent-child relationships")
    print(f"   • Realistic progress tracking with XP points and streaks")

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
        print("Principal: principal@school.edu / teacher123")
        print("Teacher 1: teacher1@school.edu / teacher123")
        print("Teacher 2: teacher2@school.edu / teacher123") 
        print("Teacher 3: teacher3@school.edu / teacher123")
        print("Student: emma.brown@student.edu / student123")
        print("Parent: parent1@example.com / parent123")
