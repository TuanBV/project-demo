import { defineStore } from 'pinia';

export const candidateStore = defineStore('candidateStore', {
  state: () => ({
    candidate: {},
  }),
  actions: {
    setCandidate(data) {
      this.candidate = data;
    },
  },
});
