import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE, SUCCESS } from 'utilities/message';

class CandidateService extends BaseService {
  /**
   * Handle get inverviewed candidates
   * @returns {array<object>} Candidates
   */
  async getInterviewedCandidates(listOffer = false) {
    const res = await this.dao.getInterviewedCandidates(listOffer);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload.candidates;
    }

    if (res.message && STATUS_CODE.NOT_FOUND !== res.code) {
      ToastUtil.error(res.message);
    }

    return [];
  }

  /**
   * Handle get list candidate
   *
   * @returns {object|false}
   */
  async getListConfirmCandidates() {
    const res = await this.dao.get_list_confirm_candidates();
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
    const res = await this.dao.get_confirm_candidate(idCandidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }

  /**
   * Handle send results by mail
   *
   * @param {array} candidatesId
   * @returns {boolean} Send mail status
   */
  async sendMails(candidatesId) {
    const res = await this.dao.sendMails(candidatesId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.SEND_RESULT.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle update status of candidate from "SEND_FORM" to "UPDATED_FORM"
   * @returns object|false
   */
  async edit_confirm_candidate(idCandidate) {
    const res = await this.dao.edit_confirm_candidate(idCandidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }

  /**
   * Handle edit status
   *
   * @returns {boolean}
   */
  async editStatus(status, message) {
    const res = await this.dao.editStatus(status);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(message);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle create result mails
   *
   * @param {array} candidatesId
   * @returns {array|false} Mails
   */
  async createResultMails(candidatesId) {
    const res = await this.dao.createResultMails(candidatesId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.RESULT.CREATE_MAIL.SUCCESS);
      return res.payload.mails;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle get offer candidates
   *
   * @param {array} candidatesId
   * @returns {array|false} Mails
   */
  async getOfferCandidates(flagLoading = true) {
    const res = await this.dao.getOfferCandidates(flagLoading);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload.candidates;
    }

    if (res.message && STATUS_CODE.NOT_FOUND !== res.code) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle get accept offer candidates
   *
   * @returns {array<object>|false} Candidates
   */
  async getAcceptOfferCandidates(flagLoading = true) {
    const res = await this.dao.getAcceptOfferCandidates(flagLoading);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload.candidates;
    }

    if (res.message && STATUS_CODE.NOT_FOUND !== res.code) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle edit start join candidate
   *
   * @param {id} candidateId
   * @returns {string} startJoinDate
   */
  async editStartJoin(candidateId, startJoinDate) {
    const res = await this.dao.editStartJoin(candidateId, startJoinDate);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CANDIDATE.UPDATE_START_JOIN.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle send candidates form
   *
   * @param {array<int>} candidatesId
   * @return {bool}
   */
  async sendCandidatesForm(candidatesId) {
    const res = await this.dao.sendCandidatesForm(candidatesId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.LINK_FORM.SEND.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle get form candidate data
   *
   * @param {string} token
   * @return {object|false}
   */
  async getFormCandidate(token) {
    const res = await this.dao.getFormCandidate(token);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }

  /**
   * Handle edit candidate
   *
   * @param {int} candidateId
   * @param {object} candidate
   * @return {bool}
   */
  async edit(candidateId, candidate) {
    const res = await this.dao.edit(candidateId, candidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CANDIDATE.UPDATE.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle edit form candidate
   *
   * @param {string} token
   * @param {object} candidate
   * @return {bool}
   */
  async editForm(token, candidate) {
    const res = await this.dao.editForm(token, candidate);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CANDIDATE.UPDATE_FORM.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle create result mails
   *
   * @param {array} candidatesId
   * @returns {array|false} Mails
   */
  async createFormMails(candidatesId) {
    const res = await this.dao.createFormMails(candidatesId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(SUCCESS.CREATE_FORM);
      return res.payload.mails;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }
}

export default new CandidateService('candidate');
