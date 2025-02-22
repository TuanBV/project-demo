import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
import ToastUtil from 'utility/toast'

class ImageService extends BaseService {
  /**
   * Handle get list image
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
   * Handle add image
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
   * Handle delete image
   *
   * @param imageId: id of the image
   * @returns object|null
   */
  async delete(imageId) {
    const res = await this.dao.delete(imageId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }
}

export default new ImageService('image')
