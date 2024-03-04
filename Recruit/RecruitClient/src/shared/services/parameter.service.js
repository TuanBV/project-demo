import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';

class ParameterService extends BaseService {
  /**
   * Handle get list param
   *
   * @returns object|null
   */
  async getList() {
    const res = await this.dao.getList();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return null;
  }

  /**
   * Handle update parameter
   *
   * @returns object|null
   */
  async edit(param) {
    const res = await this.dao.edit(param);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }

  /**
   * Handle delete parameter
   *
   * @returns object|null
   */
  async delete(idParameters) {
    const res = await this.dao.delete(idParameters);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }

  /**
   * Handle add parameter new
   *
   * @returns object|null
   */
  async add(param) {
    const res = await this.dao.add(param);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return null;
  }

  /**
   * Handle get information of param
   *
   * @returns object|null
   */
  async get(idParam) {
    const res = await this.dao.get(idParam);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return null;
  }
}

export default new ParameterService('parameter');
