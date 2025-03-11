import BaseRepository from './base.repository'

class PostRepository extends BaseRepository {
  constructor() {
    super('/post')
  }

  /**
   * Handle get list post
   *
   * @returns list[object]|null
   */
  getList() {
    return this.client.get('')
  }

  /**
   * Handle add post
   *
   * @params dataRequest: data of post
   * @returns object|null
   */
  add(dataRequest) {
    return this.client.post('', dataRequest)
  }

  /**
   * Handle get post by id
   *
   * @params postId: id of post
   * @returns object|null
   */
  getByPostId(postId) {
    return this.client.get(`/${postId}`)
  }

  /**
   * Handle delete post
   *
   * @params postId: id of post
   * @returns object|null
   */
  delete(postId) {
    return this.client.delete(`/${postId}`)
  }

  /**
   * Handle active post
   *
   * @params postId: id of post
   * @returns object|null
   */
  active(postId) {
    return this.client.put(`/${postId}/active`)
  }

  /**
   * Handle update post
   *
   * @params postId: id of the post
   * @params dataRequest: data request
   * @returns object|null
   */
  update(postId, dataRequest) {
    return this.client.put(`/${postId}`, dataRequest)
  }
}

export default new PostRepository()
