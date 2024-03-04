import BaseRepository from './base.repository';

class TeamRepository extends BaseRepository {
  constructor() {
    super('/teams');
  }

  getList() {
    return this.client.get('');
  }
}

export default new TeamRepository();
