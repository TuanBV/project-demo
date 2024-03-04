import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class CandidateAssessmentService extends BaseService {
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
   * Handle assessment
   *
   * @returns object|false
   */
  async assessment(candidateId, data) {
    const res = await this.dao.assessment(candidateId, data);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.ASSESSMENT.ADD.SUCCESS);
      return true;
    }

    ToastUtil.error(res.message);
    return false;
  }

  /**
   * Handle admin evaluate
   *
   * @returns {boolean}
   */
  async admin_evaluate(canidateId, status) {
    const res = await this.dao.admin_evaluate(canidateId, status);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.ASSESSMENT.EVALUATE.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }
}

export default new CandidateAssessmentService('candidate_assessment');
