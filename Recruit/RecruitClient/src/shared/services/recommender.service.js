import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class RecommenderService extends BaseService {
  /**
   * Handle get recommender list
   *
   * @returns array List of recommender
   */
  async getList() {
    const res = await this.dao.getList();
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }

    ToastUtil.error(res.message);
    return [];
  }

  /**
   * Handle edit recommender
   *
   * @param int recommenderId
   * @param object recommender
   * @returns object Recommender
   */
  async getDetail(recommenderId) {
    const res = await this.dao.getDetail(recommenderId);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return {};
  }

  /**
   * Handle add recommender
   *
   * @param object recommender
   * @returns object|null Recommender
   */
  async add(recommender) {
    const res = await this.dao.add(recommender);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.RECOMMENDER.ADD.SUCCESS);
      return res.payload;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return null;
  }

  /**
   * Handle delete recommender
   *
   * @param int recommenderId
   * @returns bool
   */
  async delete(recommenderId) {
    const res = await this.dao.delete(recommenderId);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.RECOMMENDER.DELETE.SUCCESS);
      return true;
    }

    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }

  /**
   * Handle edit recommender
   *
   * @param int recommenderId
   * @param object recommender data
   * @returns bool
   */
  async edit(recommenderId, recommender) {
    const res = await this.dao.edit(recommenderId, recommender);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.RECOMMENDER.UPDATE.SUCCESS);
      return true;
    }
    if (res.message) {
      ToastUtil.error(res.message);
    }
    return false;
  }
}

export default new RecommenderService('recommender');
