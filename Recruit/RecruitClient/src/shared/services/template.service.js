import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';

class TemplateService extends BaseService {
  /**
   * Handle get list template
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
   * Handle get list template
   *
   * @returns object|null
   */
  async edit(template) {
    const res = await this.dao.edit(template);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }
    return null;
  }

  /**
   * Handle get info of template
   *
   * @returns object|null
   */
  async get(idTemplate) {
    const res = await this.dao.get(idTemplate);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return null;
  }
}

export default new TemplateService('template');
