import { api } from "@/plugins/axios";
import Vue from "vue";
import VueRouter, { NavigationGuardNext, RouteConfig } from "vue-router";

Vue.use(VueRouter);

const beforeEnter = async (
  _: unknown,
  __: unknown,
  next: NavigationGuardNext<Vue>
) => {
  const { data } = await api.get<{ allowed: boolean }>("/allowed");
  return next(data.allowed ? undefined : "/");
};

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Terms",
    component: () => import("@/views/Terms.vue"),
    beforeEnter: async (
      _: unknown,
      __: unknown,
      next: NavigationGuardNext<Vue>
    ) => {
      const { data } = await api.get<{ allowed: boolean }>("/allowed");
      return next(data.allowed ? "/buy" : undefined);
    },
  },
  {
    path: "/buy",
    name: "SwapForm",
    component: () => import("@/views/SwapForm.vue"),
    beforeEnter,
  },
  {
    path: "/payment",
    name: "PayForm",
    component: () => import("@/views/PayForm.vue"),
    beforeEnter,
  },
  {
    path: "*",
    name: "PageNotFound",
    component: () => import("@/views/PageNotFound.vue"),
  },
];

const router = new VueRouter({
  mode: "hash",
  base: process.env.BASE_URL,
  routes,
});

export default router;
