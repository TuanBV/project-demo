import BaseRepository from './base.repository';

class BlackListRepository extends BaseRepository {
  constructor() {
    super('/black_list');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  get_candidate(idCandidate) {
    return this.client.get(`/${idCandidate}`);
  }
}

export default new BlackListRepository();
