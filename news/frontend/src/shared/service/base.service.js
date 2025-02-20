import RepositoryFactory from './repository/repository.factory'

export default class BaseService {
  serviceName

  dao

  constructor(serviceName) {
    this.serviceName = serviceName
    this.dao = RepositoryFactory.getRepository(serviceName)
  }

  async version() {
    return '1.0'
  }
}
