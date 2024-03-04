import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';

class CandidateListService extends BaseService {
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

  /**
   * Handle get info candidate
   *
   * @returns {object|false}
   */
  async editCandidate(candidate) {
    const res = await this.dao.edit_candidate(candidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return false;
  }

  /**
   * Handle move candidate black list
   *
   * @returns object|null
   */
  async moveBlackList(candidate) {
    const res = await this.dao.moveBlackList(candidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }
}

export default new CandidateListService('candidate_list');
