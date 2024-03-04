import BaseRepository from './base.repository';

class ContactCandidateRepository extends BaseRepository {
  constructor() {
    super('/candidates/contact-candidate');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  add(candidate) {
    return this.client.post('', candidate);
  }
}

export default new ContactCandidateRepository();
