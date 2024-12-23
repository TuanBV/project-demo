"""
Message
"""

from box import Box

ERR_MESSAGE = Box({
  "INVALID_EMAIL_OR_PASSWORD": "Địa chỉ email hoặc mật khẩu không chính xác. Vui lòng thử lại.",
  "CONTACT_ADMIN": "Đăng nhập sai quá 5 lần. Vui lòng liên hệ admin!",
  "UNAUTHENTICATION": "Lỗi xác thực",
  "ACCESS_DENIED": "Truy cập bị từ chối",
  "SERVER_ERROR": "Một lỗi máy chủ đã xảy ra. Vui lòng thử lại",
  "FILE_EXT": "Vui lòng tải tệp dưới dạng pdf, docx hoặc doc",
  "FILE_SIZE": "Vui lòng tải tệp nhỏ hơn 10MB.",
  "FILE_MISSING": "Vui lòng tải tệp cv",
  # RECOMMENDER MESSAGE
  "RECOMMENDER_NOT_EXIST": "Người giới thiệu không tồn tại",
  "MISSING_RECOMMENDER_ID": "Thiếu id người giới thiệu",
  "IDENT_NUMBER_EXIST": "Số CMT/CCCD không tồn tại",
  "EMAIL_EXIST": "Email không tồn tại",
  "TEL_EXIST": "Số điện thoại không tồn tại",
  # CANDIDATE MESSAGE
  "MISSING_CANDIDATE_ID": "Thiếu id ứng viên",
  "CANDIDATE_NOT_EXIST": "Ứng viên không tồn tại",
  "CANDIDATE_HAVE_CONTACT": "Ứng viên đã được tạo liên hệ",
  "EMAIL_OR_TELEPHONE_EXIST": "Email hoặc số điện thoại đã tồn tại",
  # User
  "MSG_0001": "Mã nhân viên đã được đăng ký",
  "MSG_0002": "Email đã được đăng ký",
  "MSG_0003": "CMT/CCCD đã được đăng ký",
  "MSG_0004": "User không tồn tại",
  "MSG_0005": "Parameter không tồn tại",
  "MSG_0006": "Nhập lại ngày vào công ty",
  "CONFIRM_PASSWORD": "Nhập lại mật khẩu không đúng với mật khẩu",
  "INCORRECT_PASSWORD": "Mật khẩu không đúng",
  # Invite interview
  "TEMPLATE_NOT_FOUND": "Không có template mail",
  "CANDIDATE_HAVE_MAIL": "Ứng viên đã có mail",
  # CONFIRM
  "INTERVIEW_NOT_FOUND": "Không có dữ liệu phỏng vấn",
  "CANDIDATE_NOT_HAVE_SCORE": "Ứng viên chưa có điểm",
  "SCORE_INVALID": "Điểm ứng viên không hợp lệ",
  # Reset password
  "LINK_RESET_PASSWORD_EXPIRED": "Link reset mật khẩu hết hạn",
  # Create mail
  "MAIL_EXIST": "Mail đã được tạo trước đó",
  # Link form
  "UNABLE_SEND_FORM": "Chỉ gửi link form cho ứng viên đã nhận offer",
  "NOT_FOUND_CANDIDATE": "Not found candidate",
  # Credentials Google calendar
  "FILE_EXT_CREDENTIALS": "Vui lòng tải tệp dưới dạng json",
  "FILE_SIZE_CREDENTIALS": "Vui lòng tải tệp nhỏ hơn 1MB.",
  "FILE_MISSING_CREDENTIALS": "Vui lòng tải tệp credentials của Google Calendar",
  "ERROR_AUTH": "Xác thực Google Calendar bị lỗi",
  # Telephone exist
  "TELEPHONE_EXIST": "Số điện thoại đã được đăng ký",
  # Email and telephone exist
  "EMAIL_TELEPHONE_EXIST": "Cả email và số điện thoại đã được đăng ký ở 2 ứng viên",
  # Email or telephone in black list
  "EMAIL_TELEPHONE_IN_BLACK_LIST": "Email hoặc số điện thoại trong danh sách đen",
})


MESSAGE = Box({
  "CANDIDATE_STATUS": {
    "FAILED_TEST": "Trượt bài test",
    "FIRST_INTERVIEW_FAILED": "Trượt vòng 1",
    "FIRST_INTERVIEW_PASS": "Qua vòng 1",
    "SECOND_INTERVIEW_FAILED": "Trượt vòng 2",
    "SECOND_INTERVIEW_PASS": "Qua vòng 2",
    "SEND_OFFER": "Đã gửi offer",
    "ACCEPT_OFFER": "Đã nhận offer",
  }
})
