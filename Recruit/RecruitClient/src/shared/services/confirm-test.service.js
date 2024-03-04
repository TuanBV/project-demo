import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class ConfirmTestService extends BaseService {
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
   * Handle save point
   *
   * @returns {boolean}
   */
  async saveScore(candidateScores) {
    const res = await this.dao.saveScore(candidateScores);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CONFIRM.SAVE_SCORE.SUCCESS);
      return true;
    }
    ToastUtil.error(res.message);
    return false;
  }

  /**
   * Handle eliminate candidate
   *
   * @returns {boolean}
   */
  async eliminate(idCandidate, flagNotTest) {
    const res = await this.dao.eliminate(idCandidate, flagNotTest);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CONFIRM.DELETE.SUCCESS);
      return true;
    }
    ToastUtil.error(res.message);
    return false;
  }

  /**
   * Handle eliminate candidate
   *
   * @returns {boolean}
   */
  async eliminateAll(listCandidateId) {
    const res = await this.dao.eliminateAll(listCandidateId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CONFIRM.DELETE.SUCCESS);
      return true;
    }
    ToastUtil.error(res.message);
    return false;
  }

  /**
   * Handle confirm candidate test
   *
   * @returns {boolean}
   */
  async confirmTest(listCandidateId) {
    const res = await this.dao.confirmTest(listCandidateId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CONFIRM.EDIT_STATUS.SUCCESS);
      return true;
    }
    ToastUtil.error(res.message);
    return false;
  }
}

export default new ConfirmTestService('confirm_test');
