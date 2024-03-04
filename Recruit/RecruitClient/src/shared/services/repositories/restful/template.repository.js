import BaseRepository from './base.repository';

class TemplateRepository extends BaseRepository {
  constructor() {
    super('/templates');
  }

  get(idTemplate) {
    return this.client.get(`/${idTemplate}`);
  }

  edit(template) {
    return this.client.put(`/${template.id}`, template);
  }

  getList() {
    return this.client.get('');
  }
}

export default new TemplateRepository();
