import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
// import { useAuthStore } from 'stores/auth-store'
import ToastUtil from 'utility/toast'
// import { MESSAGE } from 'utility/message'

class KindService extends BaseService {
  /**
   * Handle get list kind
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
   * Handle add kind
   *
   * @returns object|null
   */
  async add(dataRequest) {
    const res = await this.dao.add(dataRequest)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    ToastUtil.error(res.message)
    return null
  }

  /**
   * Handle get kind
   *
   * @param kindId: id of the kind
   * @returns object|null
   */
  async getByKindId(kindId) {
    const res = await this.dao.getByKindId(kindId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    return null
  }

  /**
   * Handle delete kind
   *
   * @param kindId: id of the kind
   * @returns object|null
   */
  async delete(kindId) {
    const res = await this.dao.delete(kindId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle active kind
   *
   * @param kindId: id of the kind
   * @returns object|null
   */
  async active(kindId) {
    const res = await this.dao.active(kindId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle update kind
   *
   * @param kindId: id of the kind
   * @param dataRequest: data request
   * @returns object|null
   */
  async update(kindId, dataRequest) {
    const res = await this.dao.update(kindId, dataRequest)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    ToastUtil.error(res.message)
    return null
  }
}

export default new KindService('kind')
