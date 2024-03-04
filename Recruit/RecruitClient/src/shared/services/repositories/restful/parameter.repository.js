import BaseRepository from './base.repository';

class TemplateRepository extends BaseRepository {
  constructor() {
    super('/parameters');
  }

  get(idParameters) {
    return this.client.get(`/${idParameters}`);
  }

  edit(param) {
    return this.client.put(`/${param.id}`, param);
  }

  delete(idParameters) {
    return this.client.delete(`/${idParameters}`);
  }

  add(param) {
    return this.client.post('', param);
  }

  getList(params) {
    return this.client.get('', params);
  }
}

export default new TemplateRepository();
