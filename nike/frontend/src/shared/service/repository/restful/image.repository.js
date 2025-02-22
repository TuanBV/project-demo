import BaseRepository from './base.repository'

class ImageRepository extends BaseRepository {
  constructor() {
    super('/image')
  }

  /**
   * Handle get list image
   *
   * @returns list[object]|null
   */
  getList() {
    return this.client.get('')
  }

  /**
   * Handle add image
   *
   * @params dataRequest: data of image
   * @returns object|null
   */
  add(dataRequest) {
    return this.client.post('', dataRequest)
  }

  /**
   * Handle delete image
   *
   * @params imageId: id of image
   * @returns object|null
   */
  delete(imageId) {
    return this.client.delete(`/${imageId}`)
  }
}

export default new ImageRepository()
