import UserRepository from 'service/repository/restful/user.repository'
import CategoryRepository from 'service/repository/restful/category.repository'
import SaleRepository from 'service/repository/restful/sale.repository'

class RepositoryFactory {
  getRepository(serviceName) {
    switch (serviceName) {
      case 'user':
        return UserRepository
      case 'category':
        return CategoryRepository
      case 'sale':
        return SaleRepository
      default:
        throw Error('Invalid param')
    }
  }
}

export default new RepositoryFactory()
