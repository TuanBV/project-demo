import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class ContactCandidateService extends BaseService {
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
   * Handle add contact
   *
   * @returns true|false
   */
  async add(contact) {
    const res = await this.dao.add(contact);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.CONTACT.ADD.SUCCESS);
      return true;
    }

    ToastUtil.error(res.message);
    return false;
  }
}

export default new ContactCandidateService('contact_candidate');
