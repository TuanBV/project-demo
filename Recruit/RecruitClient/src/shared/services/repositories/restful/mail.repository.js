import BaseRepository from './base.repository';

class MailRepository extends BaseRepository {
  constructor() {
    super('/mails');
  }

  update(mailId, mail) {
    return this.client.put(`/${mailId}`, mail);
  }
}

export default new MailRepository();
