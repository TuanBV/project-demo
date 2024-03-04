import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class InviteInterviewService extends BaseService {
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
   * Handle create result mails
   *
   * @param {array} candidatesId
   * @returns {object|false} Mails
   */
  async createInviteMails(candidatesId) {
    const res = await this.dao.createInviteMails(candidatesId);
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
   * Handle send results by mail
   *
   * @param {array} candidatesId
   * @returns {boolean} Send mail status
   */
  async sendMailsInvite(candidatesId) {
    const res = await this.dao.sendMailsInvite(candidatesId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.INVITE.SEND_MAIL.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }
}

export default new InviteInterviewService('invite_interview');
