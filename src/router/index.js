// this file creates the router instance that is used by our application

// we start by importing the createRouter and createWebHistory functions, as well as the components describing each of our views
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterView from "../views/RegisterView.vue";
import CourseView from "../views/CourseView.vue";
import CourseEdit from "../views/CourseEdit.vue";
import UserManageView from "../views/UserManageView.vue";
import UserSearchView from "../views/UserSearchView.vue";
import StudentSchedule from "../views/StudentSchedule.vue";
import ProfessorSchedule from "../views/ProfessorSchedule.vue";
import StudentUnenroll from "../views/StudentUnenroll.vue";
import CreationView from "../views/CreationView.vue";
import AdminStudentSchedule from "../views/AdminStudentSchedule.vue";
import AdminRegister from "../views/AdminRegisterView.vue";

const router = createRouter({
  // the history mode determines how vue router interacts with the url.
  // createWebHistory() simulates the default browser behavior of changing
  // the path of the url based on the current document.
  // import.meta.env.BASE_URL is a vite feature that you don't need to worry about
  // and can safely use. it refers to the current path to the directory being
  // served by vite, which in this project is always the same directory
  // (and therefore import.meta.env.BASE_URL is '/')
  history: createWebHistory(import.meta.env.BASE_URL),

  // each entry to this routes array has a path (what goes in the URL to access
  // this page), a name (check out components/AppHeader.vue for how this is used)
  // and, most importantly, the component that should be rendered for the view
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/course",
      name: "course",
      component: CourseView,
    },
    {
      path: "/StudentUnenroll",
      name: "StudentUnenroll",
      component: StudentUnenroll,
    },
    {
      path: "/edit",
      name: "edit",
      component: CourseEdit,
    },
    {
      path: "/usermanage",
      name: "usermanage",
      component: UserManageView,
    },
    {
      path: "/usersearch",
      name: "usersearch",
      component: UserSearchView,
    },
    {
      path: "/StudentSchedule",
      name: "StudentSchedule",
      component: StudentSchedule
    },
    {
      path: "/AdminSchedule",
      name: "AdminStudentSchedule",
      component: AdminStudentSchedule
    },
    {
      path: "/ProfessorSchedule",
      name: "ProfessorSchedule",
      component: ProfessorSchedule
    },
    {
      path: "/course_creation",
      name: "course_creation",
      component: CreationView,
    },
    {
      path: "/AdminRegister",
      name: "AdminRegister",
      component: AdminRegister
    }
  ],
});

export default router;
