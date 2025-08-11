from flask_restful import Api

from api.auth.routes import (ChangePassword, ForgotPassword, Login,
                             RefreshToken, ResetPassword, SignupAdmin,
                             SignupChild, SignupOrganization, SignupParent,
                             SignupTeacher)
from api.organization.routes import OrganizationStats
from api.parent.routes import (GetLinkedChildren, LinkChildToParent,
                               ParentChildrenLessonUpdates, ParentProfile)
from api.student.routes import (AnalyzeWriting, BadgeCountAPI,
                                CompletedSkillsCountAPI, CompleteHabit,
                                CompleteSkill, GrammarCheck, GratitudeEntry,
                                Habits, ImproveSentence, Skills, StoryStarter,
                                StudentLessonUpdates, StudentProfile,
                                ToDoListDetailResource, ToDoListResource,
                                VocabularySuggestions,StudentEarnedBadgesAPI)
from api.teacher.routes import (AddStudent, CreateSchool, GetLinkedStudents,
                                LinkStudentToTeacher, RemoveStudent,
                                TeacherLessonUpdateDetail,
                                TeacherLessonUpdates, TeacherProfile,
                                UnlinkStudentFromTeacher,PrincipalTeacher,
                                PrincipalTeacherManagement, GetSchools)

api = Api()

# Login
api.add_resource(Login, '/api/login')
api.add_resource(RefreshToken, '/api/refresh-token')
api.add_resource(SignupChild, '/api/child/register')
api.add_resource(SignupParent, '/api/parent/register')
api.add_resource(SignupOrganization, '/api/organization/register')
api.add_resource(SignupTeacher, '/api/teacher/register')
api.add_resource(SignupAdmin, '/api/admin/register')

api.add_resource(CreateSchool, '/api/admin/add-school')
api.add_resource(GetSchools, '/api/schools')

api.add_resource(ForgotPassword, '/api/auth/forgot-password')
api.add_resource(ResetPassword, '/api/auth/reset-password')
api.add_resource(ChangePassword, '/api/auth/change-password')

# Student
api.add_resource(GratitudeEntry, '/api/child/gratitude', '/api/child/gratitude/<int:entry_id>')
api.add_resource(Habits, '/api/child/habit', '/api/child/habit/<int:habit_id>')
api.add_resource(CompleteHabit, '/api/child/habit/<int:habit_id>/complete')
api.add_resource(ToDoListResource, '/api/todos')
api.add_resource(ToDoListDetailResource, '/api/todos/<int:todo_id>')
api.add_resource(StudentLessonUpdates, '/api/child/lesson-updates')
api.add_resource(Skills, '/api/child/skills', '/api/child/skills/<int:skill_id>')
api.add_resource(CompleteSkill, '/api/child/skills/<int:skill_id>/complete')
api.add_resource(StudentProfile, '/api/child/profile')
api.add_resource(BadgeCountAPI, '/api/child/badge/count')
api.add_resource(CompletedSkillsCountAPI, '/api/child/skills/completed/count')
api.add_resource(StudentEarnedBadgesAPI, '/api/child/badges/earned')

#AI features
api.add_resource(ImproveSentence, '/api/child/improve-sentence')
api.add_resource(AnalyzeWriting, '/api/child/analyze-writing')
api.add_resource(GrammarCheck, '/api/child/grammar-check')
api.add_resource(VocabularySuggestions, '/api/child/vocabulary-suggestions')
api.add_resource(StoryStarter, '/api/child/story-starter')

# Parent
api.add_resource(LinkChildToParent, '/api/parent/link-child', '/api/parent/unlink-child/<int:child_id>')
api.add_resource(ParentProfile, '/api/parent/profile')
api.add_resource(GetLinkedChildren, '/api/parent/linked-children')
api.add_resource(ParentChildrenLessonUpdates, '/api/parent/children/lesson-updates')

# Teacher
api.add_resource(AddStudent, '/api/teacher/add-student')
api.add_resource(RemoveStudent, '/api/teacher/remove-student/<int:student_id>')
api.add_resource(TeacherLessonUpdates, '/api/teacher/lesson-updates')
api.add_resource(TeacherLessonUpdateDetail, '/api/teacher/lesson-updates/<int:lesson_id>')
api.add_resource(LinkStudentToTeacher, '/api/teacher/link-student')
api.add_resource(UnlinkStudentFromTeacher, '/api/teacher/unlink-student/<int:student_id>')
api.add_resource(TeacherProfile, '/api/teacher/profile')
api.add_resource(GetLinkedStudents, '/api/teacher/linked-students')
api.add_resource(PrincipalTeacher, "/principal/teachers")
api.add_resource(PrincipalTeacherManagement, "/principal/teachers/<int:teacher_id>")

# Organization
api.add_resource(OrganizationStats, '/api/organization/stats')
