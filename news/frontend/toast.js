import { Notify } from 'quasar';

class ToastUtil {
  success(message) {
    Notify.create({
      type: 'positive',
      message,
    });
  }

  warning(message) {
    Notify.create({
      type: 'warning',
      message,
    });
  }

  error(message) {
    Notify.create({
      type: 'negative',
      message,
      color: 'red',
    });
  }

  exception(error) {
    if (error instanceof Error) {
      if (error.code === 'ECONNABORTED') { // timeout
        this.error('ただいま、サーバーが混み合っております。しばらく経ってからもう一度お試しください');
      } else if (error.code === 'API_ERROR') { // Api Error
        this.error('サーバエラーが発生しました。システム担当者にお問合せください');
      } else { // default
        this.error('ネットワークが接続されていません。ネットワーク接続を確認後、もう一度を試しください');
      }
    } else { // ServiceErrorResponse
      this.error('ネットワークが接続されていません。ネットワーク接続を確認後、もう一度を試しください');
    }
  }
}

export default new ToastUtil();
