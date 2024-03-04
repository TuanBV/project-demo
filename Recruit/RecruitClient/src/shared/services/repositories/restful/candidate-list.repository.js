import BaseRepository from './base.repository';

class CandidateListRepository extends BaseRepository {
  constructor() {
    super('/candidates');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  get_candidate(idCandidate) {
    return this.client.get(`/${idCandidate}`);
  }

  edit_candidate(candidate) {
    return this.client.put(`/${candidate.id}`, candidate);
  }

  /**
   * Handle move candidate black list
   *
   * @returns object|null
   */
  moveBlackList(candidate) {
    return this.client.delete(`/${candidate.id}`, candidate);
  }
}

export default new CandidateListRepository();
