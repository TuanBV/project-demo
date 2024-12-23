import UserRepository from 'service/repository/restful/user.repository'

class RepositoryFactory {
  getRepository(serviceName) {
    switch (serviceName) {
      case 'user':
        return UserRepository
      default:
        throw Error('Invalid param')
    }
  }
}

export default new RepositoryFactory()
