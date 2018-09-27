<template>
  <div class="story-list">
    <h1>{{ header }}</h1>
    <p v-if="error" class="error">{{ error }}</p>
    <main>
      <p v-if="loading">Loading...</p>
      <ul v-else class="stories">
        <li class="story"
          v-for="story in stories"
          :key="story.story_id"
        >
          <router-link class="permalink" :to="`/story/${story.story_id}`">§</router-link>
          <span class="word"
            v-for="word in story.words"
            :key="word"
          >
            {{ word }}
          </span>
          <div class="incomplete-story"
            v-if="!story.is_complete"
          >
            (the story continues...)
          </div>
        </li>
        <p v-if="stories.length === 0">
          No stories yet... Care to <router-link to="/write">write one</router-link>?
        </p>
      </ul>
    </main>
  </div>
</template>

<script>
export default {
  props: {
    header: String,
  },
  data() {
    return {
      error: null,
      stories: [],
      loading: true,
    };
  },
  computed: {
    url() {
      if (this.header === 'Your Stories') {
        return '/api/your_stories';
      }
      return '/api/recent_stories';
    },
  },
  mounted() {
    fetch(this.url)
      .then(resp => resp.ok ? resp.json() : Promise.reject(resp))
      .then((data) => {
        this.stories = data;
      })
      .catch((resp) => {
        this.error = 'uh oh. something went wrong';
      })
      .finally(() => { this.loading = false; });
  },
}
</script>
