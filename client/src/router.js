import Vue from "vue";
import Router from "vue-router";
import RecentStories from "./views/RecentStories.vue";
import YourStories from "./views/YourStories.vue";
import Write from "./views/Write.vue";
import StoryDetail from "./views/StoryDetail.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "recent_stories",
      component: RecentStories,
    },
    {
      path: "/yours",
      name: "your_stories",
      component: YourStories
    },
    {
      path: "/write",
      name: "write",
      component: Write
    },
    {
      path: "/story/:story_id",
      name: "story_detail",
      component: StoryDetail,
    },
  ]
});
