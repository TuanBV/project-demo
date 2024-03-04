import BaseRepository from './base.repository';

class AddCvRepository extends BaseRepository {
  constructor() {
    super('/candidates/add-cv');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  add(candidate) {
    return this.client.post('', candidate);
  }
}

export default new AddCvRepository();
