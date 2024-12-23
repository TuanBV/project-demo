import Toastify from 'toastify-js'
import 'toastify-js/src/toastify.css'

class ToastUtil {
  success(message) {
    Toastify({
      text: message,
      duration: 3000,
      gravity: 'top',
      position: 'right',
      backgroundColor: 'linear-gradient(to right, #00b09b, #96c93d)',
      close: true
    }).showToast()
  }

  warning(message) {
    Toastify({
      text: message,
      duration: 3000,
      gravity: 'top',
      position: 'right',
      backgroundColor: 'linear-gradient(to right, #ffbb33, #ff6600)',
      close: true
    }).showToast()
  }

  error(message) {
    Toastify({
      text: message,
      duration: 3000,
      gravity: 'top',
      position: 'right',
      backgroundColor: 'linear-gradient(to right, #ff5f6d, #ffc3a0)',
      close: true
    }).showToast()
  }

  exception(error) {
    if (error instanceof Error) {
      if (error.code === 'ECONNABORTED') {
        // timeout
        this.error('TIMEOUT')
      } else if (error.code === 'API_ERROR') {
        // Api Error
        this.error('ERROR API')
      } else {
        // default
        this.error('ERROR')
      }
    } else {
      // ServiceErrorResponse
      this.error('ERROR SERVICE')
    }
  }
}

export default new ToastUtil()
