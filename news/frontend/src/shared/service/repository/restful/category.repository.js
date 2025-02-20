import BaseRepository from './base.repository'

class CategoryRepository extends BaseRepository {
  constructor() {
    super('/category')
  }

  /**
   * Handle get list category
   *
   * @returns list[object]|null
   */
  getList() {
    return this.client.get('')
  }

  /**
   * Handle add category
   *
   * @params dataRequest: data of category
   * @returns object|null
   */
  add(dataRequest) {
    return this.client.post('', dataRequest)
  }

  /**
   * Handle get category by id
   *
   * @params categoryId: id of category
   * @returns object|null
   */
  getByCategoryId(categoryId) {
    return this.client.get(`/${categoryId}`)
  }

  /**
   * Handle delete category
   *
   * @params categoryId: id of category
   * @returns object|null
   */
  delete(categoryId) {
    return this.client.delete(`/${categoryId}`)
  }

  /**
   * Handle active category
   *
   * @params categoryId: id of category
   * @returns object|null
   */
  active(categoryId) {
    return this.client.put(`/${categoryId}/active`)
  }

  /**
   * Handle update category
   *
   * @params categoryId: id of the category
   * @params dataRequest: data request
   * @returns object|null
   */
  update(categoryId, dataRequest) {
    return this.client.put(`/${categoryId}`, dataRequest)
  }
}

export default new CategoryRepository()
