import UserRepository from 'service/repository/restful/user.repository'
import CategoryRepository from 'service/repository/restful/category.repository'
import KindRepository from 'service/repository/restful/kind.repository'
import SaleRepository from 'service/repository/restful/sale.repository'
import ImageRepository from 'service/repository/restful/image.repository'
import ProductRepository from 'service/repository/restful/product.repository'
import SettingRepository from 'service/repository/restful/setting.repository'

class RepositoryFactory {
  getRepository(serviceName) {
    switch (serviceName) {
      case 'user':
        return UserRepository
      case 'category':
        return CategoryRepository
      case 'kind':
        return KindRepository
      case 'sale':
        return SaleRepository
      case 'image':
        return ImageRepository
      case 'product':
        return ProductRepository
      case 'setting':
        return SettingRepository
      default:
        throw Error('Invalid param')
    }
  }
}

export default new RepositoryFactory()
