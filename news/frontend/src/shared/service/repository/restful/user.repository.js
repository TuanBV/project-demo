import BaseRepository from './base.repository'

class UserRepository extends BaseRepository {
  constructor() {
    super('/user')
  }

  /**
   * Handle login
   *
   * @returns object|null
   */
  login(data) {
    return this.client.post('/login', data)
  }

  /**
   * Handle information of account
   *
   * @returns object|null
   */
  getMe() {
    return this.client.get('/me')
  }

  /**
   * Handle information user by userId
   *
   * @returns object|null
   */
  get(userId) {
    return this.client.get(`/${userId}`)
  }

  /**
   * Handle add user new
   *
   * @returns object|null
   */
  add(dataUser) {
    return this.client.post('', dataUser)
  }

  /**
   * Handle edit user
   *
   * @returns object|null
   */
  edit(userId, dataUser) {
    return this.client.put(`/${userId}`, dataUser)
  }

  /**
   * Handle status user
   *
   * @returns object|null
   */
  statusUser(userId, status) {
    return this.client.post(`/${userId}/${status}`)
  }

  /**
   * Handle inactive user
   *
   * @returns object|null
   */
  delete(userId) {
    return this.client.delete(`/${userId}`)
  }

  /**
   * Handle get list user
   *
   * @returns object|null
   */
  getList(flagLoading = true) {
    return this.client.get('/all', null, null, flagLoading)
  }

  /**
   * Handle log out of account
   *
   * @returns object|null
   */
  logout() {
    return this.client.post('/logout')
  }

  /**
   * Handle change password
   *
   * @param {object} data Password and confirm password
   */
  changePassword(data) {
    return this.client.put('/password', data)
  }

  /**
   * Handle send mail forgot password
   *
   * @param {string} email
   */
  forgotPassword(email) {
    return this.client.post('/forgot-password', { email })
  }

  /**
   * Handle check access reset password with token
   *
   * @param {string} token
   */
  checkTokenForgotPassword(token) {
    return this.client.get(`/forgot-password/${token}`)
  }

  /**
   * Handle reset password
   *
   * @param {string} token
   * @param {object} data
   */
  resetPassword(token, data) {
    return this.client.put(`/reset-password/${token}`, data)
  }
}

export default new UserRepository()
