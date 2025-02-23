import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
// import { useAuthStore } from 'stores/auth-store'
import ToastUtil from 'utility/toast'
// import { MESSAGE } from 'utility/message'

class SettingService extends BaseService {
  /**
   * Handle get list setting
   *
   * @param
   * @returns list[object]|false
   */
  async getList() {
    const res = await this.dao.getList()
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    ToastUtil.error(res.message)
    return false
  }

  /**
   * Handle get new setting
   *
   * @param
   * @returns object|false
   */
  async getNewSetting() {
    const res = await this.dao.getNewSetting()
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    ToastUtil.error(res.message)
    return false
  }

  /**
   * Handle save setting
   *
   * @returns null
   */
  async save(dataRequest) {
    const res = await this.dao.save(dataRequest)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    ToastUtil.error(res.message)
    return null
  }
}

export default new SettingService('setting')
