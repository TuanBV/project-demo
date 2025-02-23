import BaseRepository from './base.repository'

class SettingRepository extends BaseRepository {
  constructor() {
    super('/setting')
  }

  /**
   * Handle get setting list
   *
   * @returns list[object]|null
   */
  getList() {
    return this.client.get('/all')
  }

  /**
   * Handle get new setting
   *
   * @returns object|null
   */
  getNewSetting() {
    return this.client.get('')
  }

  /**
   * Handle save setting
   *
   * @params dataRequest: data of setting
   * @returns object|null
   */
  save(dataRequest) {
    return this.client.post('', dataRequest)
  }
}

export default new SettingRepository()
