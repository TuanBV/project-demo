import BaseRepository from './base.repository'

class ProductRepository extends BaseRepository {
  constructor() {
    super('/product')
  }

  /**
   * Handle get list product
   *
   * @returns list[object]|null
   */
  getList() {
    return this.client.get('')
  }

  /**
   * Handle add product
   *
   * @params dataRequest: data of product
   * @returns object|null
   */
  add(dataRequest) {
    return this.client.post('', dataRequest)
  }

  /**
   * Handle get product by id
   *
   * @params productId: id of product
   * @returns object|null
   */
  getByProductId(productId) {
    return this.client.get(`/${productId}`)
  }

  /**
   * Handle delete product
   *
   * @params productId: id of product
   * @returns object|null
   */
  delete(productId) {
    return this.client.delete(`/${productId}`)
  }

  /**
   * Handle active product
   *
   * @params productId: id of product
   * @returns object|null
   */
  active(productId) {
    return this.client.put(`/${productId}/active`)
  }

  /**
   * Handle update product
   *
   * @params productId: id of the product
   * @params dataRequest: data request
   * @returns object|null
   */
  update(productId, dataRequest) {
    return this.client.put(`/${productId}`, dataRequest)
  }
}

export default new ProductRepository()
