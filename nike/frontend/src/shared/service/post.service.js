import { STATUS_CODE } from 'utility/const'
import BaseService from 'service/base.service'
// import { useAuthStore } from 'stores/auth-store'
import ToastUtil from 'utility/toast'
// import { MESSAGE } from 'utility/message'

class PostService extends BaseService {
  /**
   * Handle get list post
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
   * Handle add post
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
   * Handle get post
   *
   * @param postId: id of the post
   * @returns object|null
   */
  async getByPostId(postId) {
    const res = await this.dao.getByPostId(postId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload
    }
    return null
  }

  /**
   * Handle delete post
   *
   * @param postId: id of the post
   * @returns object|null
   */
  async delete(postId) {
    const res = await this.dao.delete(postId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }

  /**
   * Handle active post
   *
   * @param postId: id of the post
   * @returns object|null
   */
  async active(postId) {
    const res = await this.dao.active(postId)
    if (STATUS_CODE.SUCCESS === res.code) {
      return true
    }
    return null
  }
}

export default new PostService('post')
