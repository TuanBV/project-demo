import { STATUS_CODE } from 'utilities/const';
import BaseService from 'services/base.service';
import ToastUtil from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

class InterviewScheduleService extends BaseService {
  /**
   * Handle get list candidate
   *
   * @returns object|false
   */
  async getList(flagLoading = true) {
    const res = await this.dao.get_list(flagLoading);
    if (STATUS_CODE.SUCCESS === res.code) {
      return res.payload;
    }
    return false;
  }

  /**
   * Handle add interview
   *
   * @returns object|false
   */
  async add(candidateId, dataInterview) {
    const res = await this.dao.add(candidateId, dataInterview);
    if (STATUS_CODE.SUCCESS === res.code) {
      return true;
    }

    ToastUtil.error(res.message);
    return false;
  }

  /**
   * Handle edit interview
   *
   * @returns object|false
   */
  async edit(candidateId, dataInterview) {
    const res = await this.dao.edit(candidateId, dataInterview);
    if (STATUS_CODE.SUCCESS === res.code) {
      ToastUtil.success(MESSAGE.INTERVIEW_SCHEDULE.UPDATE.SUCCESS);
      return true;
    }

    ToastUtil.error(res.message);
    return false;
  }
}

export default new InterviewScheduleService('interview_schedule');
