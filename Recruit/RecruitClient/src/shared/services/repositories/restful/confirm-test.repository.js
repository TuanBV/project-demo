import BaseRepository from './base.repository';

class ConfirmTestRepository extends BaseRepository {
  constructor() {
    super('/candidates/test');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  saveScore(candidateScores) {
    return this.client.put('/score', { list_candidate: candidateScores });
  }

  eliminate(candidateId, flagNotTest) {
    return this.client.put(`/${candidateId}`, { flag_not_test: flagNotTest });
  }

  eliminateAll(listCandidateId, idsNotTest) {
    return this.client.put('/eliminate-all', { list_id: listCandidateId, list_not_test: idsNotTest });
  }

  confirmTest(listCandidateId) {
    return this.client.put('/confirm', { list_id: listCandidateId });
  }
}

export default new ConfirmTestRepository();
