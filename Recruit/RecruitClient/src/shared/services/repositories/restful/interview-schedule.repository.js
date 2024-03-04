import BaseRepository from './base.repository';

class InterviewScheduleRepository extends BaseRepository {
  constructor() {
    super('/candidates/interview-schedule');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  add(candidateId, candidate) {
    return this.client.post(`/${candidateId}`, candidate);
  }

  edit(candidateId, candidate) {
    return this.client.put(`/${candidateId}`, candidate);
  }
}

export default new InterviewScheduleRepository();
