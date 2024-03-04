import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';

class MeetingRoomService extends BaseService {
  /**
   * Handle get list position
   *
   * @returns object|false
   */
  async getList() {
    const res = await this.dao.getList();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }
}

export default new MeetingRoomService('meeting_room');
