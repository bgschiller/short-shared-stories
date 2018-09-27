<template>
  <main class="write">
    <div class="remaining-words">{{ remainingWordsPhrase }}</div>
    <div v-if="story">
      <span class="word"
        v-for="word in words"
        :key="word"
      >
        {{ word }}
      </span>
      <span
        v-if="!words.length"
        class="story-start-instructions"
      >
        How does this story start?
      </span>
      <input type="text" v-model="newWord" />
      <input type="submit" @click="submit" />
    </div>
    <p class="error" v-if="errorMsg">{{ errorMsg }}</p>
    <p v-if="initialLoading">Loading ...</p>
    <p v-if="success">Success!</p>
  </main>
</template>

<script>
export default {
  data() {
    return {
      error: null,
      initialLoading: true,
      resultLoading: false,
      story: null,
      newWord: null,
      success: null,
    };
  },
  computed: {
    remainingWordsPhrase() {
      if (!this.story) return;
      const remainingWords = this.story.num_words - this.story.words.length;
      return remainingWords > 1 ? `${remainingWords} words remain` : '1 word remains';
    },
    words() {
      if (!this.story) return [];
      return this.story.words;
    },
    errorMsg() {
      if (this.error === 'InvalidWord') {
        return 'Invalid choice of word';
      } else if (this.error === 'FragmentNotFound') {
        return 'Something went wrong writing that story. Perhaps your time had run out?';
      } else if (this.error) {
        return 'Something has gone wrong. Try again?';
      }
      return null;
    },
  },
  mounted() {
    fetch('/api/story')
      .then(resp => resp.ok ? resp.json() : Promise.reject(resp))
      .then((data) => {
        this.story = data;
      })
      .catch((resp) => {
        this.error = 'uh oh. something went wrong';
      })
      .finally(() => { this.initialLoading = false; });
  },
  methods: {
    submit() {
      this.resultLoading = true;
      this.error = null;

      fetch(`/api/story/${this.story.story_id}`, {
        method: 'POST',
        body: JSON.stringify({ word: this.newWord }),
        headers: {
          'content-type': 'application/json',
        },
      })
        .then(resp => resp.ok ? resp.json() : resp.json().then(data => Promise.reject(data, resp)))
        .then(() => {
          this.success = true;
          setTimeout(() => {
            this.$router.push('/');
          }, 2000);
        })
        .catch((data) => { this.error = data.error })
        .finally(() => { this.resultLoading = false; });
    },
  },
}
</script>
