import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class MailService extends BaseService {
  /**
   * Handle update mail
   *
   * @param int mailId
   * @param object mail
   *
   * @returns {object|false}
   */
  async update(mailId, mail) {
    const res = await this.dao.update(mailId, mail);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.MAIL.UPDATE.SUCCESS);
      return res.payload;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }
}

export default new MailService('mail');
