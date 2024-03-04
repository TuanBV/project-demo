import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';

class StaffListService extends BaseService {
  /**
   * Handle get list candidate
   *
   * @returns {object|false}
   */
  async getList(flagLoading = true) {
    const res = await this.dao.get_list(flagLoading);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }

  /**
  * Handle get list candidate
  *
  * @returns {object|false}
  */
  async delete(idStaff) {
    const res = await this.dao.delete(idStaff);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }
}

export default new StaffListService('staff_list');
