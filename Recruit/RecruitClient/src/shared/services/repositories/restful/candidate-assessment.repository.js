import BaseRepository from './base.repository';

class CandidateAssessmentRepository extends BaseRepository {
  constructor() {
    super('/candidates/assessment');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  assessment(candidateId, data) {
    return this.client.put(`/${candidateId}`, data);
  }

  admin_evaluate(candidateId, status) {
    return this.client.put(`/evaluate/${candidateId}`, { evaluate: status });
  }
}

export default new CandidateAssessmentRepository();
