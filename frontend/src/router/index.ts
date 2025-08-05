import {createWebHistory, createRouter} from 'vue-router'

import LandingPage from '../pages/LandingPage.vue'
import LoginStudent from '../pages/student/LoginStudent.vue';
import RegisterStudent from '../pages/student/RegisterStudent.vue';
import RegisterOrganisation from '../pages/organisation/RegisterOrganisation.vue';
import RegisterParent from '../pages/parent/RegisterParent.vue';
import LoginParent from "../pages/parent/LoginParent.vue";
import ParentHome from "../pages/parent/ParentHome.vue";
import LoginOrganisation from "../pages/organisation/LoginOrganisation.vue";
import HomeOrganisation from "../pages/organisation/HomeOrganisation.vue";
import HomeStudent from "../pages/student/HomeStudent.vue";
import Badges from "../pages/student/Badges.vue";
import Habit from '../pages/student/Habit.vue';
import LessonUpdates from "../pages/student/LessonUpdates.vue";
import SurveyPage from "../pages/student/SurveyPage.vue";
import WeeklyReport from "../pages/student/WeeklyReport.vue";
import SurveyReport from "../pages/teacher/SurveyReport.vue";
import TeacherLessonUpdates from "../pages/teacher/LessonUpdates.vue";
import StudentJournal from "../pages/student/StudentJournal.vue";
import LinkChild from '../pages/parent/LinkChild.vue';
import AddTeacher from "../pages/organisation/AddTeacher.vue";
import TeachersList from "../pages/organisation/TeachersList.vue";

const routes = [
    {path: '/', component: LandingPage},

    // BEGIN STUDENT SECTION
    {path: '/student/login', component: LoginStudent},
    {path: '/student/register', component: RegisterStudent},
    {path: '/student/home', component: HomeStudent},
    {path: '/student/badges', component: Badges},
    {path: '/student/habit', component: Habit},
    {path: '/student/lesson-updates', component: LessonUpdates},
    {path: '/student/survey', component: SurveyPage},
    {path: '/student/journal', component: StudentJournal},
    {path: '/student/weekly-report', component: WeeklyReport},
    // END STUDENT SECTION


    // BEGIN ORG SECTION
    {path: '/org/register', component: RegisterOrganisation},
    {path: '/org/login', component: LoginOrganisation},
    {path: '/org/home', component: HomeOrganisation},
    {path: '/org/survey-report', component: SurveyReport},
    {path: '/org/add-teacher', component: AddTeacher},
    {path: '/org/teachers', component: TeachersList},
    // END ORG SECTION


    // BEGIN PARENT SECTION
    {path: '/parent/register', component: RegisterParent},
    {path: '/parent/login', component: LoginParent},
    {path: '/parent/home', component: ParentHome},
    {path: '/parent/link-child', component: LinkChild},
    // END PARENT SECTION


    // BEGIN TEACHER SECTION
    {path: '/teacher/survey-report', component: SurveyReport},
    {path: '/teacher/lesson-updates', component: TeacherLessonUpdates},
    // END TEACHER SECTION

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;