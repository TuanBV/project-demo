import BaseRepository from './base.repository';

class MeetingRoomRepository extends BaseRepository {
  constructor() {
    super('/meeting-rooms');
  }

  getList() {
    return this.client.get('');
  }
}

export default new MeetingRoomRepository();
