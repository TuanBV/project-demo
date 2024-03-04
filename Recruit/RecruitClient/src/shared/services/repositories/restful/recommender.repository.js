import BaseRepository from './base.repository';

class RecommenderRepository extends BaseRepository {
  constructor() {
    super('/recommenders');
  }

  getList() {
    return this.client.get('');
  }

  add(recommender) {
    return this.client.post('', recommender);
  }

  delete(recommenderId) {
    return this.client.delete(`/${recommenderId}`);
  }

  getDetail(recommenderId) {
    return this.client.get(`/${recommenderId}`);
  }

  edit(recommenderId, recommender) {
    return this.client.put(`/${recommenderId}`, recommender);
  }
}

export default new RecommenderRepository();
