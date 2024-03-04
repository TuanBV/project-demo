import BaseRepository from './base.repository';

class CandidateRepository extends BaseRepository {
  constructor() {
    super('/candidates');
  }

  getInterviewedCandidates(optionValue = false) {
    return this.client.get(`/interviewed/${optionValue !== false ? optionValue : 0}`);
  }

  sendMails(candidatesId) {
    return this.client.post('/send-result-mails', {
      candidates_id: candidatesId,
    });
  }

  get_list() {
    return this.client.get('');
  }

  get_list_confirm_candidates() {
    return this.client.get('/confirm');
  }

  get_confirm_candidate(idCandidate) {
    return this.client.get(`/confirm/${idCandidate}`);
  }

  add(candidate) {
    return this.client.post('', candidate);
  }

  editStatus(dataStatus) {
    return this.client.put('/status', dataStatus);
  }

  createResultMails(candidatesId) {
    return this.client.post('/result-mails', { candidates_id: candidatesId });
  }

  getOfferCandidates(flagLoading = true) {
    return this.client.get('/offer', null, null, flagLoading);
  }

  edit_confirm_candidate(idCandidate) {
    return this.client.put(`/confirm/${idCandidate}`);
  }

  getAcceptOfferCandidates(flagLoading = true) {
    return this.client.get('/accept-offer', null, null, flagLoading);
  }

  editStartJoin(candidateId, startJoinDate) {
    return this.client.put(`/start-join/${candidateId}`, { start_join_date: startJoinDate });
  }

  sendCandidatesForm(candidatesId) {
    return this.client.post('/form/send', { candidates_id: candidatesId });
  }

  getFormCandidate(token) {
    return this.client.get(`/form/${token}`);
  }

  edit(candidateId, candidate) {
    return this.client.put(`/${candidateId}`, candidate);
  }

  editForm(token, candidate) {
    return this.client.put(`/form/${token}`, candidate);
  }

  createFormMails(candidatesId) {
    return this.client.post('/form-mails', { candidates_id: candidatesId });
  }
}

export default new CandidateRepository();
