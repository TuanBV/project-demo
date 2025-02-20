const MESSAGE = {
  LOGIN_SUCCESSFULLY: 'Đăng nhập thành công',
  RECOMMENDER: {
    ADD: {
      CONFIRM_TITLE: 'Xác nhận thêm người giới thiệu',
      CONFIRM_QUESTION: 'Bạn đồng ý thêm người giới thiệu?',
      SUCCESS: 'Thêm người giới thiệu thành công',
    },
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận cập nhật người giới thiệu',
      CONFIRM_QUESTION: 'Bạn đồng ý cập nhật thông tin của người giới thiệu <b>:fullname</b>?',
      SUCCESS: 'Cập nhật người giới thiệu thành công',
    },
    DELETE: {
      CONFIRM_TITLE: 'Xác nhận xóa người giới thiệu',
      CONFIRM_QUESTION: 'Bạn đồng ý xóa người giới thiệu <b>:fullname</b>?',
      SUCCESS: 'Xóa người giới thiệu thành công',
    },
  },
  USER: {
    ADD: {
      CONFIRM_TITLE: 'Xác nhận thêm user mới',
      CONFIRM_QUESTION: 'Bạn đồng ý thêm user mới?',
      SUCCESS: 'Thêm user mới thành công',
      ERROR: 'Thêm user mới không thành công',
      EMPLOYEE_CODE: 'Thêm user mới không thành công',
    },
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận cập nhật thông tin user',
      CONFIRM_QUESTION: 'Bạn đồng ý cập nhật thông tin user ',
      SUCCESS: 'Cập nhật thông tin user thành công',
      ERROR: 'Cập nhật thông tin user không thành công',
    },
    DELETE: {
      CONFIRM_TITLE: 'Xác nhận xóa user',
      CONFIRM_QUESTION: 'Bạn đồng ý xóa user',
      SUCCESS: 'Xóa user thành công',
      ERROR: 'Xóa user không thành công',
    },
    CHANGE_PASSWORD: {
      SUCCESS: 'Đổi mật khẩu thành công',
    },
  },
  PARAM: {
    ADD: {
      CONFIRM_TITLE: 'Xác nhận thêm param mới',
      CONFIRM_QUESTION: 'Bạn đồng ý thêm param mới ',
      SUCCESS: 'Thêm param mới thành công',
      ERROR: 'Thêm mới không thành công',
    },
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận cập nhật thông tin param',
      CONFIRM_QUESTION: 'Bạn đồng ý cập nhật thông tin param ',
      SUCCESS: 'Cập nhật thông tin param thành công',
      ERROR: 'Cập nhật không thành công',
    },
    DELETE: {
      CONFIRM_TITLE: 'Xác nhận xóa param',
      CONFIRM_QUESTION: 'Bạn đồng ý xóa param ',
      SUCCESS: 'Xóa param thành công',
      ERROR: 'Xóa không thành công',
    },
  },
  TEAM: {
    ADD: {
      CONFIRM_TITLE: 'Xác nhận thêm team mới',
      CONFIRM_QUESTION: 'Bạn đồng ý thêm team mới ',
      SUCCESS: 'Thêm team mới thành công',
      ERROR: 'Thêm mới không thành công',
    },
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận cập nhật thông tin team',
      CONFIRM_QUESTION: 'Bạn đồng ý cập nhật thông tin team ',
      SUCCESS: 'Cập nhật thông tin team thành công',
      ERROR: 'Cập nhật không thành công',
    },
    DELETE: {
      CONFIRM_TITLE: 'Xác nhận xóa team',
      CONFIRM_QUESTION: 'Bạn đồng ý xóa team ',
      SUCCESS: 'Xóa team thành công',
      ERROR: 'Xóa không thành công',
    },
  },
  TEMPLATE: {
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận cập nhật mail mẫu',
      CONFIRM_QUESTION: 'Bạn đồng ý cập nhật thông tin mail mẫu ',
      SUCCESS: 'Cập nhật thông tin mail mẫu thành công',
      ERROR: 'Cập nhật thông tin mail mẫu không thành công',
    },
  },
  ADD_CV: {
    DELETE: {
      CONFIRM_TITLE: 'Xác nhận loại ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý loại ứng viên này?',
      SUCCESS: 'Loại CV thành công',
    },
    ACCEPT: {
      CONFIRM_TITLE: 'Xác nhận duyệt ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý duyệt ứng viên này?',
      SUCCESS: 'Duyệt CV thành công',
    },
    ADD: {
      CONFIRM_TITLE: 'Xác nhận thêm CV',
      CONFIRM_QUESTION: 'Bạn đồng ý thêm CV này?',
      SUCCESS: 'Thêm CV thành công',
      CONFIRM_CLOSE: 'Đang nhập dữ liệu. Bạn đồng ý đóng màn hình?',
      CONFIRM_CLOSE_TITLE: 'Đóng màn hình thêm CV',
    },
    EDIT: {
      CONFIRM_TITLE: 'Xác nhận cập nhật CV',
      CONFIRM_QUESTION: 'Đang bị trùng :dataExist của ứng viên <b>:fullname</b>. Bạn có muốn tiếp tục cập nhật thông tin ứng viên?',
      SUCCESS: 'Cập nhật CV thành công',
    },
  },
  CONTACT: {
    DELETE: {
      CONFIRM_TITLE: 'Xác nhận loại ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý loại ứng viên này?',
      SUCCESS: 'Loại CV thành công',
    },
    ADD: {
      CONFIRM_TITLE: 'Xác nhận lưu thông tin liên hệ ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý lưu thông tin liên hệ của ứng viên này?',
      SUCCESS: 'Tạo liên hệ thành công',
    },
    PASS: {
      CONFIRM_TITLE: 'Xác nhận ứng viên qua vòng 2',
      CONFIRM_QUESTION: 'Bạn đồng ý ứng viên này qua vòng 2?',
      SUCCESS: 'Chuyển trạng thái ứng viên thành công',
    },
  },
  CONFIRM: {
    DELETE: {
      CONFIRM_TITLE: 'Xác nhận loại ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý loại ứng viên này?',
      SUCCESS: 'Loại ứng viên thành công',
    },
    DELETE_ALL: {
      CONFIRM_TITLE: 'Xác nhận loại ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý loại những ứng viên này?',
    },
    SAVE_SCORE: {
      CONFIRM_TITLE: 'Xác nhận lưu điểm ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý lưu điểm những ứng viên được chọn?',
      SUCCESS: 'Lưu điểm thành công',
    },
    EDIT_STATUS: {
      CONFIRM_TITLE: 'Xác nhận duyệt ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý duyệt những ứng viên được chọn?',
      SUCCESS: 'Duyệt ứng viên thành công',
    },
  },
  INVITE: {
    SAVE_MAIL: {
      CONFIRM_TITLE: 'Xác nhận lưu thông tin mail',
      CONFIRM_QUESTION: 'Bạn đồng ý lưu thông tin mail của ứng viên?',
    },
    CREATE_MAIL: {
      CONFIRM_TITLE: 'Xác nhận tạo mail ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý tạo mail những ứng viên được chọn?',
    },
    SEND_MAIL: {
      CONFIRM_TITLE: 'Xác nhận gửi mail ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý gửi mail những ứng viên được chọn?',
      SUCCESS: 'Gửi email thành công',
    },
    DELETE_MAIL: {
      CONFIRM_TITLE: 'Xác nhận xóa mail ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý xóa mail những ứng viên được chọn?',
      SUCCESS: 'Xóa mail thành công',
    },
  },
  INTERVIEW_SCHEDULE: {
    ADD: {
      CONFIRM_TITLE: 'Xác nhận thêm lịch phỏng vấn',
      CONFIRM_QUESTION: 'Bạn đồng ý thêm lịch phỏng vấn cho ứng viên?',
      TEST_SUCCESS: 'Thêm lịch test thành công',
      INTERVIEW_SUCCESS: 'Thêm lịch phỏng vấn thành công',
    },
    UPDATE: {
      SUCCESS: 'Lưu thông tin phỏng vấn thành công',
    },
  },
  ASSESSMENT: {
    ADD: {
      CONFIRM_TITLE: 'Xác nhận đánh giá ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý đánh giá cho ứng viên?',
      SUCCESS: 'Đánh giá ứng viên thành công',
    },
    EVALUATE: {
      SUCCESS: 'Cập nhật trạng thái ứng viên thành công',
    },
    PASS: {
      CONFIRM_TITLE: 'Xác nhận ứng viên pass?',
      CONFIRM_QUESTION: 'Bạn đồng ý ứng viên này pass?',
    },
  },
  RESULT: {
    SAVE_MAIL: {
      CONFIRM_TITLE: 'Xác nhận lưu thông tin mail',
      CONFIRM_QUESTION: 'Bạn đồng ý lưu thông tin mail của ứng viên?',
    },
    SEND_MAIL: {
      CONFIRM_TITLE: 'Xác nhận gửi mail ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý gửi mail những ứng viên được chọn?',
    },
    CREATE_MAIL: {
      CONFIRM_TITLE: 'Xác nhận tạo mail ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý tạo mail những ứng viên được chọn?',
      SUCCESS: 'Tạo mail thành công',
    },
  },
  OFFER: {
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận đổi trạng thái ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý đổi trạng thái ứng viên?',
    },
  },
  FORM: {
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận ngày đi làm cho ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý chọn ngày đi làm cho ứng viên?',
    },
    SEND_MAIL: {
      CONFIRM_TITLE: 'Xác nhận gửi mail ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý gửi mail những ứng viên được chọn?',
    },
  },
  CANDIDATE: {
    CONFIRM: {
      CONFIRM_TITLE: 'Xác nhận thông tin ứng viên',
      CONFIRM_QUESTION: 'Bạn duyệt thông tin ứng viên ',
      SUCCESS: 'Duyệt thông tin ứng viên thành công',
      ERROR: 'Duyệt thông tin ứng viên không thành công',
    },
    RE_ENTRY: {
      CONFIRM_TITLE: 'Yêu cầu nhập lại thông tin ứng viên',
      CONFIRM_QUESTION: 'Bạn yêu cầu nhập lại thông tin ứng viên ',
      SUCCESS: 'Yêu cầu nhập lại thông tin ứng viên thành công',
    },
    UPDATE: {
      CONFIRM_TITLE: 'Xác nhận cập nhật ứng viên',
      CONFIRM_QUESTION: 'Bạn đồng ý cập nhật thông tin của ứng viên <b>:name</b>?',
      SUCCESS: 'Cập nhật thông tin ứng viên thành công',
      ERROR: 'Cập nhật thông tin ứng viên không thành công',
      CONFIRM_RECEIVE_CV: 'Khi cập nhật trạng thái thành Nhận CV sẽ xóa dữ liệu test và phỏng vấn. Xác nhận tiếp tục cập nhật thông tin của ứng viên <b>:name</b>?',
      CONFIRM_ACCEPT_CV: 'Khi cập nhật trạng thái thành "Duyệt CV", "Mời test", "Làm bài test" sẽ xóa dữ liệu test, phỏng vấn và mặc định về trạng thái "Duyệt CV".<br>Xác nhận tiếp tục cập nhật thông tin của ứng viên <b>:name</b>?',
      CONFIRM_TEST_OK: 'Khi cập nhật trạng thái thành "Test OK", "Mời PV vòng 1", "PV vòng 1" sẽ xóa dữ liệu phỏng vấn và mặc định về trạng thái "Test OK".<br>Xác nhận tiếp tục cập nhật thông tin của ứng viên <b>:name</b>?',
      CONFIRM_FIRST_INTERVIEW_PASS: 'Khi cập nhật trạng thái thành "Qua vòng 1", "Mời PV vòng 2", "PV vòng 2" sẽ xóa dữ liệu phỏng vấn và mặc định về trạng thái "Qua vòng 1".<br>Xác nhận tiếp tục cập nhật thông tin của ứng viên <b>:name</b>?',
      CONFIRM_SECOND_INTERVIEW_PASS: 'Khi cập nhật trạng thái thành "Qua vòng 2", "Đã gửi offer", "Đã nhận offer", "Đã gửi form", "Đã cập nhật form" sẽ xóa dữ liệu test, phỏng vấn chưa hoàn thành.<br>Xác nhận tiếp tục cập nhật thông tin của ứng viên <b>:name</b>?',
      CONFIRM_PASS_FAILED: 'Khi cập nhật các trạng thái liên quan đến pass, trượt, offer, form, nghỉ việc,... sẽ xóa dữ liệu test, phỏng vấn chưa hoàn thành.<br>Xác nhận tiếp tục cập nhật thông tin của ứng viên <b>:name</b>?',
    },
    UPDATE_STATUS: {
      OFFER: {
        SUCCESS: 'Cập nhật trạng thái offer thành công',
      },
    },
    UPDATE_OFFER: {
      SUCCESS: 'Cập nhật trạng thái offer thành công',
    },
    UPDATE_FORM: {
      SUCCESS: 'Cập nhật thông tin thành công',
    },
    UPDATE_START_JOIN: {
      SUCCESS: 'Cập nhật thành công',
    },
    DELETE: {
      SUCCESS: 'Xóa nhân viên thành công!',
      ERROR: 'Xóa nhân viên thất bại!',
    },
    MOVE_BLACK_LIST: {
      SUCCESS: 'Đã chuyển ứng viên đến danh sách đen !',
      ERROR: 'Chuyển ứng viên đến danh sách đen thất bại !',
    },
  },
  SETTING_MAIL: {
    CONFIRM: {
      CONFIRM_TITLE: 'Xác nhận lưu thay đổi mail',
      CONFIRM_QUESTION: 'Bạn có muốn đồng ý thay đổi mail không?',
    },
  },
  SEND_RESULT: {
    SUCCESS: 'Gửi kết quả thành công',
  },
  MAIL: {
    UPDATE: {
      SUCCESS: 'Cập nhật mail thành công',
      ERROR: 'Cập nhật mail không thành công',
    },
    CREATE: {
      CONFIRM_TITLE: 'Xác nhận tạo mail cho ứng viên',
      CONFIRM_QUESTION: 'Bạn có muốn tạo mail cho các ứng viên :candidates không?',
      NOT_ALLOW: 'Không thể tạo mail cho ứng viên đã có mail',
    },
    SEND: {
      NOT_ALLOW: 'Không thể gửi mail cho ứng viên chưa có mail',
    },
  },
  OFFICE: {
    UPDATE_MAIL: {
      SUCCESS: 'Cập nhật mail thành công',
    },
    UPDATE_CALENDAR: {
      SUCCESS: 'Cập nhật Google Calendar thành công',
    },
  },
  FORGOT_PASSWORD: {
    LABEL_SEND_MAIL: 'Gửi lại mail sau :countdown giây',
    SENT_MAIL: 'Chúng tôi đã gửi mail quên mật khẩu cho bạn',
  },
  RESET_PASSWORD: {
    SUCCESS: 'Đổi mật khẩu thành công',
  },
  LINK_FORM: {
    SEND: {
      SUCCESS: 'Gửi link form thành công',
    },
  },
  SETTING_CALENDAR: {
    CONFIRM: {
      CONFIRM_TITLE: 'Xác nhận lưu thông tin Google Calendar',
      CONFIRM_QUESTION: 'Bạn có đồng ý thay đổi thông tin setting Google Calendar không?',
    },
  },
};

const WARNING = {
  SEND_FORM: 'Chỉ gửi cho ứng viên đã có ngày đi làm và đã tạo mail',
  NOT_SELECTED: 'Chưa chọn ứng viên. Vui lòng chọn',
  SELECTED: 'Ứng viên đã tạo mail. Vui lòng chọn lại',
  CREATE_MAIL: 'Ứng viên chưa tạo mail. Vui lòng chọn lại',
  CANDIDATE_HAVE_MAIL: 'Đang chọn ứng viên đã tạo mail. Vui lòng chọn lại',
  CANDIDATE_NOT_HAVE_MAIL: 'Đang chọn ứng viên chưa có mail. Vui lòng chọn lại',
  CANDIDATE_NOT_HAVE_SCORE: 'Ứng viên chưa có điểm',
  REQUIRED_SCORE: 'Cần nhập điểm đánh giá ứng viên',
  CANDIDATE_HAVE_SCORE_ALREADY: 'Ứng viên đã có điểm',
  FILE_NOT_VALID: 'Chỉ upload file định dạng pdf, doc, docx',
};

const SUCCESS = {
  CREATE_FORM: 'Tạo mail thành công !',
  SEND_MAIL: 'Gửi mail thành công !',
};

const ERROR = {
  PARAM: {
    NAME: {
      MAXLENGTH: 'Tên param không vượt quá 50 kí tự',
      REQUIRED: 'Tên param là trường bắt buộc',
      INVALID: 'Tên param không hợp lệ',
    },
    TABLE: {
      MAXLENGTH: 'Tên bảng không dài hơn 50 ký tự',
      REQUIRED: 'Tên bảng trường bắt buộc',
      INVALID: 'Tên bảng không hợp lệ',
    },
    COLUMN: {
      MAXLENGTH: 'Tên cột không quá 50 kí tự',
      REQUIRED: 'Tên cột là trường bắt buộc',
      INVALID: 'Tên cột không hợp lệ',
    },
  },
  TEAM: {
    NAME: {
      MAXLENGTH: 'Tên param không vượt quá 256 kí tự',
      REQUIRED: 'Tên param là trường bắt buộc',
    },
  },
  TEMPLATE: {
    TITLE: {
      MAXLENGTH: 'Tên tiêu đề không vượt quá 256 kí tự',
      REQUIRED: 'Tên tiêu đề là trường bắt buộc',
      INVALID: 'Tên tiêu đề không hợp lệ',
    },
    BODY: {
      REQUIRED: 'Nội dung trường bắt buộc',
      INVALID: 'Nội dung không hợp lệ',
    },
  },
  EMPLOYEE_CODE: {
    MAXLENGTH: 'Mã nhân viên không quá 6 kí tự',
    REQUIRED: 'Mã nhân viên là trường bắt buộc',
    INVALID: 'Mã nhân viên không hợp lệ',
    EXISTS: 'Mã nhân viên đã tồn tại',
  },
  EMAIL: {
    MAXLENGTH: 'Email không dài hơn 256 ký tự',
    REQUIRED: 'Email là trường bắt buộc',
    INVALID: 'Email không hợp lệ',
  },
  PASSWORD: {
    REQUIRED: 'Mật khẩu là trường bắt buộc',
    INVALID: 'Mật khẩu tối thiểu 8 ký tự, tối đa 64 ký tự, ít nhất một chữ hoa, một chữ thường và một số, một kí tự đặc biệt.',
    MAXLENGTH: 'Mật khẩu không quá 64 kí tự',
  },
  NEW_PASSWORD: {
    REQUIRED: 'Mật khẩu mới là trường bắt buộc',
    NOT_EQUAL_PASSWORD: 'Mật khẩu mới không được giống mật khẩu cũ',
    INVALID: 'Mật khẩu mới tối thiểu 8 ký tự, tối đa 64 ký tự, ít nhất một chữ hoa, một chữ thường và một số, một kí tự đặc biệt.',
  },
  CONFIRM_PASSWORD: {
    REQUIRED: 'Nhập lại mật khẩu là trường bắt buộc',
    EQUAL: 'Mật khẩu nhập lại phải giống với mật khẩu',
  },
  SERVER_ERROR: 'Lỗi máy chủ',
  FULLNAME: {
    MAXLENGTH: 'Họ tên không dài hơn 50 ký tự',
    REQUIRED: 'Họ tên là trường bắt buộc',
  },
  BIRTHDAY: {
    REQUIRED: 'Ngày sinh là trường bắt buộc',
    FAIL_DATE: 'Nhập sai ngày',
    IN_PAST: 'Ngày sinh phải trong quá khứ',
    INVALID: 'Ngày nhập không hợp lệ',
    PATTERN: 'Ngày sinh phải có format là yyyy/mm/dd',
  },
  REGISTERED_DATE: {
    INVALID: 'Ngày vào công ty phải có format là yyyy/mm/dd',
    IN_PAST: 'Ngày vào công ty phải trong quá khứ',
  },
  FULL_ADDRESS: {
    REQUIRED: 'Địa chỉ là trường bắt buộc',
    MAXLENGTH: 'Địa chỉ không dài quá 256 ký tự',
  },
  POSITION_ID: {
    REQUIRED: 'Chức danh là trường bắt buộc',
    INVALID: 'Chức danh không hợp lệ',
  },
  OFFICE_ID: {
    REQUIRED: 'Văn phòng là trường bắt buộc',
    INVALID: 'Văn phòng không hợp lệ',
  },
  PLACE_ISSUED_IDENTIFICATION: {
    REQUIRED: 'Nơi cấp CMT/CCCD là trường bắt buộc',
    MAXLENGTH: 'Nơi cấp CMT/CCCD không dài quá 100 ký tự',
  },
  IDENTIFICATION_NUMBER: {
    REQUIRED: 'Số CMT/CCCD là trường bắt buộc',
    MINLENGTH: 'Số CMT/CCCD có ít nhất 9 kí tự',
    MAXLENGTH: 'Số CMT/CCCD không quá 12 kí tự',
    INVALID: 'Số CMT/CCCD không hợp lệ',
  },
  DATE_ISSUED_IDENTIFICATION: {
    REQUIRED: 'Ngày cấp CMT/CCCD là trường bắt buộc',
    FAIL_DATE: 'Nhập sai ngày',
    INVALID: 'Ngày cấp CMT/CCCD phải có format là yyyy/mm/dd',
    IN_PAST: 'Ngày cấp CMT/CCCD phải trong quá khứ',
  },
  TELEPHONE_NO: {
    REQUIRED: 'Số điện thoại là trường bắt buộc',
    INVALID: 'Số điện thoại không hợp lệ',
  },
  TITLE_MAIL: {
    REQUIRED: 'Tiêu đề là trường bắt buộc',
    MAXLENGTH: 'Tiêu đề không được dài quá 256 ký tự',
  },
  BODY_MAIL: {
    REQUIRED: 'Nội dung mail là trường bắt buộc',
  },
  TEAM_ID: {
    REQUIRED: 'Vị trí là trường bắt buộc',
    INVALID: 'Vị trí không hợp lệ',
  },
  START_JOIN_DATE: {
    IS_FUTURE: 'Ngày đi làm dự kiến phải là tương lai',
    REQUIRED: 'Ngày đi làm dự kiến là trường bắt buộc',
    INVALID: 'Ngày đi làm dự kiến không hợp lệ',
    FAIL_DATE: 'Nhập sai ngày',
  },
  PLACE_OF_BIRTH: {
    REQUIRED: 'Nơi sinh là trường bắt buộc',
    MAXLENGTH: 'Nơi sinh không được quá 256 ký tự',
  },
  BANK_ACCOUNT: {
    REQUIRED: 'Tài khoản ngân hàng là trường bắt buộc',
    MAXLENGTH: 'Tài khoản ngân hàng không được quá 50 ký tự',
    INVALID: 'Tài khoản ngân hàng chỉ được ghi số',
  },
  BANK_BRANCH: {
    REQUIRED: 'Chi nhánh ngân hàng là trường bắt buộc',
    MAXLENGTH: 'Chi nhánh ngân hàng không được quá 256 ký tự',
    INVALID: 'Tài khoản ngân hàng chỉ được ghi số',
  },
  VEHICLE_NUMBER: {
    REQUIRED: 'Biển số xe là trường bắt buộc',
    MAXLENGTH: 'Biển số xe không được quá 9 ký tự',
    INVALID: 'Biển số xe chỉ được ghi chữ và số',
  },
  INTERVIEW_DATE: {
    REQUIRED: 'Ngày phỏng vấn là trường bắt buộc',
    INVALID: 'Ngày phỏng vấn phải có format là yyyy-mm-dd',
    FUTURE: 'Ngày phỏng vấn phải là ngày tương lai',
    FAIL_DATE: 'Nhập sai ngày',
  },
  INTERVIEW_TIME: {
    REQUIRED: 'Thời gian phỏng vấn là trường bắt buộc',
    PATTERN: 'Thời gian phỏng vấn không hợp lệ',
    INVALID: 'Thời gian phỏng vấn phải có format là HH:MM',
  },
  STATUS: {
    REQUIRED: 'Trạng thái là trường bắt buộc',
    INVALID: 'Trạng thái không hợp lệ',
  },
  NOTE: {
    MAXLENGTH: 'Ghi chú không quá 256 kí tự',
    INVALID: 'Ghi chú không hợp lệ',
  },
  LINK_INTERVIEW: {
    REQUIRED: 'Link phỏng vấn là trường bắt buộc',
  },
  MEETING_ROOM: {
    REQUIRED: 'Phòng họp là trường bắt buộc',
    INVALID: 'Phòng họp không hợp lệ',
  },
  INTERVIEWER: {
    MINITEMS: 'Phải có người phỏng vấn',
  },
  GENDER: {
    INVALID: 'Giới tính không hợp lệ',
    REQUIRED: 'Giới tính là trường bắt buộc',
  },
  EXPERIENCE: {
    REQUIRED: 'Năm kinh nghiệm là trường bắt buộc',
    INVALID: 'Năm kinh nghiệm không hợp lệ (VD: 1.5)',
  },
  COMMENT: {
    REQUIRED: 'Admin, PM cần phải ghi nội dung đánh giá khi Chấp nhận hay Loại',
  },
  EVALUATE: {
    PASS_REQUIRED: 'Admin, PM cần chọn kết quả đánh giá PASS khi Chấp nhận',
    FAILED_REQUIRED: 'Admin, PM cần chọn kết quả đánh giá TRƯỢT khi Loại',
  },
  CALENDAR_ID: {
    REQUIRED: 'Cần nhập thông tin Calendar Id',
  },
  CREDENTIALS_FILE: {
    REQUIRED: 'Vui lòng chọn file',
  },
  SUPERVISOR: {
    REQUIRED: 'Vui lòng chọn người giám sát',
  },
  APPLICATION_DATE: {
    REQUIRED: 'Ngày apply là trường bắt buộc',
    INVALID: 'Ngày apply không hợp lệ',
    NOW_OR_PAST: 'Ngày apply phải là ngày hiện tại hoặc quá khứ',
  },
  FLAG_NOT_INTERVIEW: {
    INVALID: 'Sai định dạng dữ liệu',
  },
};

export {
  MESSAGE,
  ERROR,
  WARNING,
  SUCCESS,
};
