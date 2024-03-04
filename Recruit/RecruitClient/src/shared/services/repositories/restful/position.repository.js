import BaseRepository from './base.repository';

class PositionRepository extends BaseRepository {
  constructor() {
    super('/positions');
  }

  getList() {
    return this.client.get('');
  }
}

export default new PositionRepository();
