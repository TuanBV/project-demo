import { useQuasar } from 'quasar';
import { countStore } from 'stores/count-store';
import userService from 'services/user.service';

export default function useMixin() {
  const confirm = useQuasar();

  const confirmPopup = (titleConfirm, messageConfirm, ok, onClose = null) => {
    confirm.dialog({
      persistent: true,
      dark: false,
      title: titleConfirm,
      message: messageConfirm,
      cancel: true,
      color: 'teal-10',
      html: true,
    }).onOk(() => {
      ok();
    }).onCancel(() => {
      if (onClose) {
        onClose();
      }
    });
  };

  /**
 * Handle count record of page
 *
 * @returns boolean
 */
  const countRecord = async () => {
    const { setCountRecord } = countStore();
    const dataCount = await userService.countRecord();
    setCountRecord(dataCount);
  };

  return {
    confirmPopup,
    countRecord,
  };
}
