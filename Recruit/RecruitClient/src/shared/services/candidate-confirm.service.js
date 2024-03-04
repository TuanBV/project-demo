import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';

class CandidateConfirmService extends BaseService {
  /**
   * Handle get list candidate
   *
   * @returns object|false
   */
  async getList(flagLoading = true) {
    const res = await this.dao.get_list(flagLoading);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }

  /**
   * Handle get info confirm candidate
   *
   * @returns object|false
   */
  async getConfirmCandidate(idCandidate) {
    const res = await this.dao.get_candidate_confirm(idCandidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }

  /**
   * Handle update status of candidate from "SEND_FORM" to "UPDATED_FORM"
   *
   * @returns object|false
   */
  async edit(idCandidate) {
    const res = await this.dao.edit(idCandidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }
}

export default new CandidateConfirmService('candidate_confirm');
