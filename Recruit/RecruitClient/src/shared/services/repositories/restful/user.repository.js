import BaseRepository from './base.repository';

class UserRepository extends BaseRepository {
  constructor() {
    super('/users');
  }

  /**
   * Handle login
   *
   * @returns object|null
   */
  login(data) {
    return this.client.post('/login', data);
  }

  /**
   * Handle information of account
   *
   * @returns object|null
   */
  getMe() {
    return this.client.get('/me');
  }

  /**
   * Handle count record of page
   *
   * @returns object|null
   */
  countRecord() {
    return this.client.get('/count-record');
  }

  /**
   * Handle login
   *
   * @returns object|null
   */
  get(employeeCode) {
    return this.client.get(`/${employeeCode}`);
  }

  /**
   * Handle add user new
   *
   * @returns object|null
   */
  add(dataUser) {
    return this.client.post('', dataUser);
  }

  /**
   * Handle edit user
   *
   * @returns object|null
   */
  edit(dataUser) {
    return this.client.put(`/${dataUser.employee_code}`, dataUser);
  }

  /**
   * Handle add user new
   *
   * @returns object|null
   */
  delete(employeeCode) {
    return this.client.delete(`/${employeeCode}`);
  }

  /**
   * Handle get list user
   *
   * @returns object|null
   */
  getList(flagLoading = true) {
    return this.client.get('', null, null, flagLoading);
  }

  /**
   * Handle log out of account
   *
   * @returns object|null
   */
  logout() {
    return this.client.post('/logout');
  }

  /**
   * Handle change password
   *
   * @param {object} data Password and confirm password
   */
  changePassword(data) {
    return this.client.put('/password', data);
  }

  /**
   * Handle send mail forgot password
   *
   * @param {string} email
   */
  forgotPassword(email) {
    return this.client.post('/forgot-password', { email });
  }

  /**
   * Handle check access reset password with token
   *
   * @param {string} token
   */
  checkTokenForgotPassword(token) {
    return this.client.get(`/forgot-password/${token}`);
  }

  /**
   * Handle reset password
   *
   * @param {string} token
   * @param {object} data
   */
  resetPassword(token, data) {
    return this.client.put(`/reset-password/${token}`, data);
  }

  /**
   * Handle get list user
   *
   * @returns object|null
   */
  getListInterviewer() {
    return this.client.get('/interviewer');
  }
}

export default new UserRepository();
