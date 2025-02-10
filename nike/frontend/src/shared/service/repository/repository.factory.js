import UserRepository from 'service/repository/restful/user.repository'
import CategoryRepository from 'service/repository/restful/category.repository'

class RepositoryFactory {
  getRepository(serviceName) {
    switch (serviceName) {
      case 'user':
        return UserRepository
      case 'category':
        return CategoryRepository
      default:
        throw Error('Invalid param')
    }
  }
}

export default new RepositoryFactory()
