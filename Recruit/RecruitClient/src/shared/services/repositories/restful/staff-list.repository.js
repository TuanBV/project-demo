import BaseRepository from './base.repository';

class StaffListRepository extends BaseRepository {
  constructor() {
    super('/staff');
  }

  get_list(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  delete(idStaff) {
    return this.client.delete(`/${idStaff}`);
  }
}

export default new StaffListRepository();
