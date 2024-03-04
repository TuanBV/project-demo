import BaseRepository from './base.repository';

class CandidatePassListRepository extends BaseRepository {
  constructor() {
    super('/candidates_pass_list');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  add_mail(listIdCandidate) {
    return this.client.post('', listIdCandidate);
  }

  edit_mail(mailTemplate) {
    return this.client.put('', mailTemplate);
  }

  send_mail(listIdCandidate) {
    return this.client.put('/send-mail', listIdCandidate);
  }
}

export default new CandidatePassListRepository();
