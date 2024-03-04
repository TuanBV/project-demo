import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import { useAuthStore } from 'stores/auth-store';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class UserService extends BaseService {
  /**
   * Handle login user
   *
   * @param object data
   * @returns object|false
   */
  async login(data) {
    const res = await this.dao.login(data);
    if (STATUS_CODE.SUCCESS === res.code) {
      const auth = useAuthStore();
      auth.signIn(res.payload);
      return res.payload;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle get current user
   *
   * @returns object|null
   */
  async getMe() {
    const res = await this.dao.getMe();
    if (STATUS_CODE.SUCCESS === res.code) {
      const auth = useAuthStore();
      auth.signIn(res.payload);
      return res.payload;
    }
    return null;
  }

  /**
   * Handle get list user
   *
   * @returns object|null
   */
  async getList(flagLoading = true) {
    const res = await this.dao.getList(flagLoading);
    if (STATUS_CODE.SUCCESS === res.code) {
      res.payload.list_user.forEach((item) => {
        if (item.gender === 0) {
          item.gender_text = 'Nam';
        } else if (item.gender === 1) {
          item.gender_text = 'Nữ';
        } else {
          item.gender_text = '';
        }
      });
      return res.payload;
    }
    return null;
  }

  /**
   * Handle count record of page
   *
   * @returns object|null
   */
  async countRecord() {
    const res = await this.dao.countRecord();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return null;
  }

  /**
   * Handle get information of user
   *
   * @returns object|null
   */
  async get(employeeCode) {
    const res = await this.dao.get(employeeCode);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return null;
  }

  /**
   * Handle get information of user
   *
   * @returns object|null
   */
  async add(dataUser) {
    const res = await this.dao.add(dataUser);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }

  /**
   * Handle edit information of user
   *
   * @returns object|null
   */
  async edit(dataUser) {
    const res = await this.dao.edit(dataUser);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }

  /**
   * Handle delete user
   *
   * @returns object|null
   */
  async delete(employeeCode) {
    const res = await this.dao.delete(employeeCode);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }

  /**
   * Handle logout user
   *
   * @returns boolean
   */
  async logout() {
    const res = await this.dao.logout();
    if (STATUS_CODE.SUCCESS === res.code) {
      const auth = useAuthStore();
      auth.signOut();
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle change password
   *
   * @param {object} data
   * @returns {boolean}
   */
  async changePassword(data) {
    const res = await this.dao.changePassword(data);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.USER.CHANGE_PASSWORD.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle send mail forgot password
   *
   * @param {string} email
   * @return {boolean}
   */
  async forgotPassword(email) {
    const res = await this.dao.forgotPassword(email);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.FORGOT_PASSWORD.SENT_MAIL);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle check access reset password with token
   *
   * @param {string} token
   * @return {boolean}
   */
  async checkTokenForgotPassword(token) {
    const res = await this.dao.checkTokenForgotPassword(token);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle reset password
   *
   * @param {object} data
   * @return {boolean}
   */
  async resetPassword(token, data) {
    const res = await this.dao.resetPassword(token, data);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle get list user
   *
   * @returns object|null
   */
  async getListInterviewer() {
    const res = await this.dao.getListInterviewer();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return null;
  }
}

export default new UserService('user');
