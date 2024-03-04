import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';

class BlackListService extends BaseService {
  /**
   * Handle get black list candidate
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
   * Handle get info candidate
   *
   * @returns {object|false}
   */
  async getCandidate(idCandidate) {
    const res = await this.dao.get_candidate(idCandidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }
}

export default new BlackListService('black_list');
