"""
Template admin staff edit
"""
BODY_TEXT = """
ご連絡頂きました内容にて登録内容を変更致しましので、アクセスに必要な情報をお知らせ致します。


===========================
《 ご契約者様の情報 》

     ご契約者様No.    ： {{ shopNo }}
     ご契約者様名      ： {{ corporateName }}　 様
     代表者氏名 　　 ： {{ ownerFullName }}　 様
     メールアドレス   ： {{ ownerMail }}
     パスワード          ： {{ ownerPassword }}

    店舗責任者 　
     メールアドレス   ： {{ managerMail }}
     パスワード          ： {{ managerPassword }}

　店舗スタッフ
     メールアドレス   ： {{ staffMail }}
     パスワード          ： {{ staffPassword }}


《 ご契約サービス 》

     アクセスURL  　： {{ urlShop }}
     サービス内容       ： {{ serviceContent }}
     利用開始日      　 ： {{ startUsingDate }}
     契約開始年月　   ： {{ contractStartDate }}
===========================



===========================
▼配信に関するお問合わせ窓口
再春館システム
サービス契約マヂ口

TEL. {{ systemTel }}



※本メールの内容に覚えがない場合、大変お手数ですが上記「お問合わせ窓口」までお知らせください。


※このメールは送信専用メールアドレスから配信されています。
このままご返信いただいてもお答えできませんのでご了承ください。


"""

BODY_HTML = """
"""
