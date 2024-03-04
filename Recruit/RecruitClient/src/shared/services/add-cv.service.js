import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class AddCvService extends BaseService {
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
   * Handle add cv
   *
   * @returns object|false
   */
  async add(cv) {
    const res = await this.dao.add(cv);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.ADD_CV.ADD.SUCCESS);
      return res.payload;
    }

    ToastUtil.error(res.message);
    return null;
  }
}

export default new AddCvService('add_cv');
