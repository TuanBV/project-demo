import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
// import { useAuthStore } from 'stores/auth-store'
import ToastUtil from 'utility/toast'
// import { MESSAGE } from 'utility/message'

class ProductService extends BaseService {
  /**
   * Handle get list product
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
   * Handle add product
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
   * Handle get product
   *
   * @param productId: id of the product
   * @returns object|null
   */
  async getByProductId(productId) {
    const res = await this.dao.getByProductId(productId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    return null
  }

  /**
   * Handle delete product
   *
   * @param productId: id of the product
   * @returns object|null
   */
  async delete(productId) {
    const res = await this.dao.delete(productId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle active product
   *
   * @param productId: id of the product
   * @returns object|null
   */
  async active(productId) {
    const res = await this.dao.active(productId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle update product
   *
   * @param productId: id of the product
   * @param dataRequest: data request
   * @returns object|null
   */
  async update(productId, dataRequest) {
    const res = await this.dao.update(productId, dataRequest)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    ToastUtil.error(res.message)
    return null
  }
}

export default new ProductService('product')
