import { defineStore } from 'pinia';

export const countStore = defineStore('countStore', {
  state: () => ({
    count: {},
  }),
  actions: {
    setCountRecord(countRecord) {
      this.count = countRecord;
    },
  },
});
