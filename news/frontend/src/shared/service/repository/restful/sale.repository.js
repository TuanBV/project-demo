import BaseRepository from './base.repository'

class SaleRepository extends BaseRepository {
  constructor() {
    super('/sale')
  }

  /**
   * Handle get list sale
   *
   * @returns list[object]|null
   */
  getList() {
    return this.client.get('')
  }

  /**
   * Handle add sale
   *
   * @params dataRequest: data of sale
   * @returns object|null
   */
  add(dataRequest) {
    return this.client.post('', dataRequest)
  }

  /**
   * Handle get sale by id
   *
   * @params saleId: id of sale
   * @returns object|null
   */
  getBySaleId(saleId) {
    return this.client.get(`/${saleId}`)
  }

  /**
   * Handle delete sale
   *
   * @params saleId: id of sale
   * @returns object|null
   */
  delete(saleId) {
    return this.client.delete(`/${saleId}`)
  }

  /**
   * Handle active sale
   *
   * @params saleId: id of sale
   * @returns object|null
   */
  active(saleId) {
    return this.client.put(`/${saleId}/active`)
  }

  /**
   * Handle update sale
   *
   * @params saleId: id of the sale
   * @params dataRequest: data request
   * @returns object|null
   */
  update(saleId, dataRequest) {
    return this.client.put(`/${saleId}`, dataRequest)
  }
}

export default new SaleRepository()
