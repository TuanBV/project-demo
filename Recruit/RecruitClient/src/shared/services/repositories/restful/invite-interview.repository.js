import BaseRepository from './base.repository';

class InviteInterviewRepository extends BaseRepository {
  constructor() {
    super('/candidates/invite-interview');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  createInviteMails(candidatesId) {
    return this.client.post('/create-invite-mails', { candidates_id: candidatesId });
  }

  sendMailsInvite(candidatesId) {
    return this.client.post('/send-invite-mails', { candidates_id: candidatesId });
  }
}

export default new InviteInterviewRepository();
