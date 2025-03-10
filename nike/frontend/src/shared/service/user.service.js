import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
import { useAuthStore } from 'stores/auth-store'
import ToastUtil from 'utility/toast'
// import { MESSAGE } from 'utility/message'

class UserService extends BaseService {
  /**
   * Handle login user
   *
   * @param object data
   * @returns object|false
   */
  async login(data) {
    const res = await this.dao.login(data)
    if (STATUS_CODE.SUCCESS === res.code) {
      const auth = useAuthStore()
      auth.signIn(res.payload)
      ToastUtil.success('Login successful !!!')
      return res.payload
    }
    ToastUtil.error(res.message)
    return false
  }

  /**
   * Handle get current user
   *
   * @returns object|null
   */
  async getMe() {
    const res = await this.dao.getMe()
    if (STATUS_CODE.SUCCESS === res.code) {
      const auth = useAuthStore()
      auth.signIn(res.payload)
      return res.payload
    }
    return null
  }

  /**
   * Handle get list user
   *
   * @returns object|null
   */
  async getList(flagLoading = true) {
    const res = await this.dao.getList(flagLoading)
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    return null
  }

  /**
   * Handle get information of user
   *
   * @returns object|null
   */
  async get(userId) {
    const res = await this.dao.get(userId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    return null
  }

  /**
   * Handle get information of user
   *
   * @returns object|null
   */
  async add(dataUser) {
    const res = await this.dao.add(dataUser)
    if (res) {
      // ToastUtil.success('Tạo tài khoản thành công !!!')
      return true
    }
    ToastUtil.error('Lỗi tạo tài khoản !!!')
    return null
  }

  /**
   * Handle edit information of user
   *
   * @returns object|null
   */
  async edit(dataUser) {
    const res = await this.dao.edit(dataUser)
    console.log(res)
    // if (STATUS_CODE.SUCCESS === res.code) {
    //   ToastUtil.success(MESSAGE.USER.UPDATE.SUCCESS)
    //   return true
    // }
    // ToastUtil.error(res.message)
    return null
  }

  /**
   * Handle delete user
   *
   * @returns object|null
   */
  async statusUser(userId, status) {
    const res = await this.dao.statusUser(userId, status)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle logout user
   *
   * @returns boolean
   */
  async logout() {
    const res = await this.dao.logout()
    if (STATUS_CODE.SUCCESS === res.code) {
      const auth = useAuthStore()
      auth.signOut()
      return true
    }

    // if (res.message) {
    //   ToastUtil.error(res.message)
    // }
    return false
  }

  /**
   * Handle change password
   *
   * @param {object} data
   * @returns {boolean}
   */
  async changePassword(data) {
    const res = await this.dao.changePassword(data)
    console.log(res)
    // if (STATUS_CODE.SUCCESS === res.code) {
    //   ToastUtil.success(MESSAGE.USER.CHANGE_PASSWORD.SUCCESS)
    //   return true
    // }

    // if (res.message) {
    //   ToastUtil.error(res.message)
    // }
    return false
  }

  /**
   * Handle send mail forgot password
   *
   * @param {string} email
   * @return {boolean}
   */
  async forgotPassword(email) {
    const res = await this.dao.forgotPassword(email)
    console.log(res)
    // if (STATUS_CODE.SUCCESS === res.code) {
    //   ToastUtil.success(MESSAGE.FORGOT_PASSWORD.SENT_MAIL)
    //   return true
    // }

    // if (res.message) {
    //   ToastUtil.error(res.message)
    // }
    return false
  }

  /**
   * Handle check access reset password with token
   *
   * @param {string} token
   * @return {boolean}
   */
  async checkTokenForgotPassword(token) {
    const res = await this.dao.checkTokenForgotPassword(token)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }

    // if (res.message) {
    //   ToastUtil.error(res.message)
    // }
    return false
  }

  /**
   * Handle reset password
   *
   * @param {object} data
   * @return {boolean}
   */
  async resetPassword(token, data) {
    const res = await this.dao.resetPassword(token, data)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }

    // if (res.message) {
    //   ToastUtil.error(res.message)
    // }
    return false
  }
}

export default new UserService('user')
