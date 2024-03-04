import BaseRepository from './base.repository';

class OfficeRepository extends BaseRepository {
  constructor() {
    super('/offices');
  }

  getList() {
    return this.client.get('');
  }

  getMails() {
    return this.client.get('/mail');
  }

  updateMails(mails) {
    return this.client.put('/mail', mails);
  }
}

export default new OfficeRepository();
