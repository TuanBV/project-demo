import { STATUS_CODE } from 'utilities/const';
import { MESSAGE } from 'utilities/message';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';

class OfficeService extends BaseService {
  /**
   * Handle get list position
   *
   * @returns object|false
   */
  async getList() {
    const res = await this.dao.getList();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle get mail offices
   *
   * @returns {array|false}
   */
  async getMails() {
    const res = await this.dao.getMails();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload.offices;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle update mail offices
   *
   * @returns {boolean}
   */
  async updateMails(mails) {
    const res = await this.dao.updateMails(mails);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.OFFICE.UPDATE_MAIL.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }
}

export default new OfficeService('office');
