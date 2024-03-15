"""
Template mail send OTP
"""
BODY_TEXT = """
認証コード： {{ otp }}
この認証は1分で有効になります。
"""

BODY_HTML = """
認証コード： {{ otp }}
この認証は1分で有効になります。
"""
