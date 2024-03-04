"""
Message
"""

from box import Box

ERR_MESSAGE = Box({
  "INVALID_EMAIL_OR_PASSWORD": "メールアドレスまたはパスワードが正しくありません。入力し直してください。",
  "UNAUTHENTICATION": "認証エラー",
  "ACCESS_DENIED": "アクセス拒否。",
  "SERVER_ERROR": "サーバエラーが発生しました。再試行してください 。"
})
