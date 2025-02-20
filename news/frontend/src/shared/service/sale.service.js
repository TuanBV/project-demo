import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
// import { useAuthStore } from 'stores/auth-store'
import ToastUtil from 'utility/toast'
// import { MESSAGE } from 'utility/message'

class SaleService extends BaseService {
  /**
   * Handle get list sale
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
   * Handle add sale
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
   * Handle get sale
   *
   * @param saleId: id of the sale
   * @returns object|null
   */
  async getBySaleId(saleId) {
    const res = await this.dao.getBySaleId(saleId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    return null
  }

  /**
   * Handle delete sale
   *
   * @param saleId: id of the sale
   * @returns object|null
   */
  async delete(saleId) {
    const res = await this.dao.delete(saleId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle active sale
   *
   * @param saleId: id of the sale
   * @returns object|null
   */
  async active(saleId) {
    const res = await this.dao.active(saleId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle update sale
   *
   * @param saleId: id of the sale
   * @param dataRequest: data request
   * @returns object|null
   */
  async update(saleId, dataRequest) {
    const res = await this.dao.update(saleId, dataRequest)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    ToastUtil.error(res.message)
    return null
  }
}

export default new SaleService('sale')
