<template>
  <main class="story-detail">
    <div v-if="story">
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
    </div>
    <p v-if="loading">Loading...</p>
    <p v-if="error === 'not_found'">
      Couldn't find that story. Perhaps one of
      <router-link to="/">these</router-link>
      will suite you?
    </p>
    <p v-else-if="error">
      Uh oh. Something went wrong.
    </p>
  </main>
</template>

<script>
export default {
  data() {
    return {
      story: null,
      loading: true,
      error: null,
    };
  },
  mounted() {
    fetch(`/api/story/${this.$route.params.story_id}`)
      .then(resp => resp.ok ? resp.json() : Promise.reject(resp))
      .then((data) => { this.story = data; })
      .catch((resp) => {
        this.error = resp.status === 404 ? 'not_found' : 'other';
      })
      .finally(() => { this.loading = false; });
  },
}
</script>
