import BaseRepository from './base.repository'

class KindRepository extends BaseRepository {
  constructor() {
    super('/kind')
  }

  /**
   * Handle get list kind
   *
   * @returns list[object]|null
   */
  getList() {
    return this.client.get('')
  }

  /**
   * Handle add kind
   *
   * @params dataRequest: data of kind
   * @returns object|null
   */
  add(dataRequest) {
    return this.client.post('', dataRequest)
  }

  /**
   * Handle get kind by id
   *
   * @params kindId: id of kind
   * @returns object|null
   */
  getByKindId(kindId) {
    return this.client.get(`/${kindId}`)
  }

  /**
   * Handle delete kind
   *
   * @params kindId: id of kind
   * @returns object|null
   */
  delete(kindId) {
    return this.client.delete(`/${kindId}`)
  }

  /**
   * Handle active kind
   *
   * @params kindId: id of kind
   * @returns object|null
   */
  active(kindId) {
    return this.client.put(`/${kindId}/active`)
  }

  /**
   * Handle update kind
   *
   * @params kindId: id of the kind
   * @params dataRequest: data request
   * @returns object|null
   */
  update(kindId, dataRequest) {
    return this.client.put(`/${kindId}`, dataRequest)
  }
}

export default new KindRepository()
