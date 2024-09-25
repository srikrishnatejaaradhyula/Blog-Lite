import { createRouter, createWebHistory } from "vue-router";
import Landing from "../components/Landing.vue";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import Nav from "../components/Nav.vue";
import Home from "../components/Home.vue";
import Post from "../components/Post.vue";
import CompleteProfile from "../components/CompleteProfile.vue";
import Follow from "../components/Follow.vue";
import Profile from "../components/Profile.vue";
import ErrorPage404 from "../components/ErrorPage404.vue";
import EditProfile from "../components/EditProfile.vue";
import EditPost from "../components/EditPost.vue";
import Unauthorized from "../components/Unauthorized.vue";
import OthersProfile from "../components/OthersProfile.vue"
import PostComment from "../components/PostComment.vue"
import Heatmap from "../components/Heatmap.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Landing",
      component: Landing,
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/register",
      name: "Register",
      component: Register,
    },
    {
      path: "/nav",
      name: "Nav",
      component: Nav,
      meta: { requiresAuth: true },
    },
    {
      path: "/home",
      name: "Home",
      component: Home,
      meta: { requiresAuth: true },
    },
    {
      path: "/post",
      name: "Post",
      component: Post,
      meta: { requiresAuth: true },
    },
    {
      path: "/complete-profile",
      name: "CompleteProfile",
      component: CompleteProfile,
      meta: { requiresAuth: true },
    },
    {
      path: "/follow",
      name: "Follow",
      component: Follow,
      meta: { requiresAuth: true },
    },
    {
      path: "/profile",
      name: "Profile",
      component: Profile,
      meta: { requiresAuth: true },
    },
    {
      path: "/edit-profile/:id",
      name: "EditProfile",
      component: EditProfile,
      meta: { requiresAuth: true },
    },
    {
      path: "/edit-post/:id",
      name: "EditPost",
      component: EditPost,
      meta: { requiresAuth: true },
    },
    {
      path: "/other-profile/:id",
      name: "OthersProfile",
      component: OthersProfile,
      meta: { requiresAuth: true },
    },
    {
      path: "/post-comment/:id",
      name: "PostComment",
      component: PostComment,
      meta: { requiresAuth: true },
    },
    {
      path: "/heatmap",
      name: "Heatmap",
      component: Heatmap,
    },
    {
      path: "/unauthorized",
      name: "Unauthorized",
      component: Unauthorized,
    },
    {
      path: "/:catchAll(.*)",
      name: "NotFound",
      component: ErrorPage404,
    }
  ],
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (to.meta.requiresAuth && !token) {
    // Redirect to the unauthorized page if the token is missing
    next('/unauthorized');
  } else {
    // Continue to the next page
    next();
  }
});

export default router;
