import BaseRepository from './base.repository';

class CandidateConfirmRepository extends BaseRepository {
  constructor() {
    super('/candidates_confirm');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  get_candidate_confirm(idCandidate) {
    return this.client.get(`/${idCandidate}`);
  }

  edit(idCandidate) {
    return this.client.put(`/${idCandidate}`);
  }
}

export default new CandidateConfirmRepository();
