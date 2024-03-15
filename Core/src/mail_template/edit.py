"""
Template email edit
"""
BODY_TEXT = """
Wellcome {{ fullName }} to CRM
"""

BODY_HTML = """
<html>
<head></head>
<body>
  <h1>CRM SMTP Email Edit</h1>
  <p>Wellcome <b> {{ fullName }} </b> to CRM</p>
</body>
</html>
"""