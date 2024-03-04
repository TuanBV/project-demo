import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';

class CandidatePassListService extends BaseService {
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
  async addMail(listIdCandidate) {
    const res = await this.dao.add_mail(listIdCandidate);
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
  async editMail(mailTemplate) {
    const res = await this.dao.edit_mail(mailTemplate);
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
  async sendMail(listIdCandidate) {
    const res = await this.dao.send_mail(listIdCandidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return false;
  }
}

export default new CandidatePassListService('candidate_pass_list');
