import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';

class TeamService extends BaseService {
  /**
   * Handle get teams
   *
   * @returns array|null
   */
  async getList() {
    const res = await this.dao.getList();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload.item;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return null;
  }
}

export default new TeamService('team');
