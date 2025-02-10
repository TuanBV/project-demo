import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
// import { useAuthStore } from 'stores/auth-store'
import ToastUtil from 'utility/toast'
// import { MESSAGE } from 'utility/message'

class CategoryService extends BaseService {
  /**
   * Handle get list category
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
   * Handle add category
   *
   * @returns object|null
   */
  async add(dataRequest) {
    const res = await this.dao.add(dataRequest)
    console.log(res)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    ToastUtil.error(res.message)
    return null
  }

  /**
   * Handle get category
   *
   * @param categoryId: id of the category
   * @returns object|null
   */
  async getByCategoryId(categoryId) {
    const res = await this.dao.getByCategoryId(categoryId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    return null
  }

  /**
   * Handle delete category
   *
   * @param categoryId: id of the category
   * @returns object|null
   */
  async delete(categoryId) {
    const res = await this.dao.delete(categoryId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle active category
   *
   * @param categoryId: id of the category
   * @returns object|null
   */
  async active(categoryId) {
    const res = await this.dao.active(categoryId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle update category
   *
   * @param categoryId: id of the category
   * @param dataRequest: data request
   * @returns object|null
   */
  async update(categoryId, dataRequest) {
    const res = await this.dao.update(categoryId, dataRequest)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    ToastUtil.error(res.message)
    return null
  }
}

export default new CategoryService('category')
