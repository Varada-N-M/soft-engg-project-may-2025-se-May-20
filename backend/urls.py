from flask_restful import Api
from api.auth.routes import SignupChild, Login, RefreshToken, SignupParent, SignupOrganization, SignupTeacher
<<<<<<< HEAD
from api.student.routes import GratitudeEntry, Habits, CompleteHabit, ToDoListResource
from api.parent.routes import LinkChildToParent
from api.teacher.routes import AddStudent, RemoveStudent
from api.organization.routes import OrganizationStats
=======
from api.student.routes import GratitudeEntry, Habits, CompleteHabit, StudentLessonUpdates
from api.parent.routes import LinkChildToParent
from api.teacher.routes import AddStudent
from api.teacher.routes import TeacherLessonUpdates
>>>>>>> lessonupdates_backend_frontend


api = Api()

# Login
api.add_resource(Login, '/api/login')
api.add_resource(RefreshToken, '/api/refresh-token')
api.add_resource(SignupChild, '/api/child/register')
api.add_resource(SignupParent, '/api/parent/register')
api.add_resource(SignupOrganization, '/api/organization/register')
api.add_resource(SignupTeacher, '/api/teacher/register')

# Student
api.add_resource(GratitudeEntry, '/api/child/gratitude', '/api/child/gratitude/<int:entry_id>')
api.add_resource(Habits, '/api/child/habit', '/api/child/habit/<int:habit_id>')
api.add_resource(CompleteHabit, '/api/child/habit/<int:habit_id>/complete')
<<<<<<< HEAD
api.add_resource(ToDoListResource, '/api/todos', '/api/todos/<int:todo_id>')
=======
api.add_resource(StudentLessonUpdates, '/api/child/lesson-updates')

>>>>>>> lessonupdates_backend_frontend

# Parent
api.add_resource(LinkChildToParent, '/api/parent/link-child', '/api/parent/unlink-child/<int:child_id>')

# Teacher
api.add_resource(AddStudent, '/api/teacher/add-student')
<<<<<<< HEAD
api.add_resource(RemoveStudent, '/api/teacher/remove-student/<int:student_id>')

# Organization
api.add_resource(OrganizationStats, '/api/organization/stats')
=======
api.add_resource(TeacherLessonUpdates, '/api/teacher/lesson-updates')
>>>>>>> lessonupdates_backend_frontend
