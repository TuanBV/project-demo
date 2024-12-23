"""
KBN
"""
import enum
from box import Box
import sqlalchemy as db

# delete flag
DEL_FLG = Box({
  "OFF": 0,
  "ON": 1,
})

# Data cookie name
COOKIE_NAME = Box({
  "USER": "__USER",
})

# Type database
TYPE_DB = Box({
  "READ": 0,
  "WRITE": 1
})

# Step skip
STEP_SKIP = Box({
  "SKIP_SECOND_INTERVIEW": ",5,6",
  "SECOND_INTERVIEW_FAILED": ",7,8",
  "FIRST_INTERVIEW_FAILED": ",5,6,7,8",
  "REFUSE_OFFER": ",8",
  "NO_SKIP": ""
})

# role
class ROLE(enum.IntEnum):
  INTERN = 1
  STAFF = 2
  LEADER = 3
  MANAGER = 4
  COLLABORATORS = 5
  ADMIN = 6


# Login notify flag
class LoginNotifyFlg(enum.IntEnum):
  OFF = 0
  ON = 1

# Delete flag
class DeleteFlag(enum.IntEnum):
  OFF = 0
  ON = 1

# Recommender flag
class RecommenderFlag(enum.IntEnum):
  OFF = 0
  ON = 1

# Count apply
class CountApply(enum.IntEnum):
  TWO_APPLY = 2

# Template mail
class TemplateMail(enum.IntEnum):
  SEND_MAIL_CANDIDATE_HN = 17
  SEND_MAIL_CANDIDATE_HUE = 18

# Mail flag
class MailFlag(enum.IntEnum):
  UNSENT = 0
  SENT = 1

# Candidate result status
class CandidateResultStatus(enum.IntEnum):
  """
    Candidate result status
  """
  UNSENT = 0
  SENT = 1

# Flag second interview
class SecondInterviewFlag(enum.IntEnum):
  SKIP = 0
  INTERVIEW = 1

class EvaluateType(enum.IntEnum):
  ELIMINATE = 0
  SAVE = 1
  ACCEPT = 2

class TypeCalendar(enum.IntEnum):
  CREATE = 0
  UPDATE = 1


# Candidate status
class CandidateStatus(enum.IntEnum):
  """
    Candidate status
  """
  RECEIVE_CV = 0
  FAILED_CV = 1
  ACCEPT_CV = 2
  INVITE_TEST = 3
  TEST = 4
  TEST_OK = 5
  FAILED_TEST = 6
  INVITE_FIRST_INTERVIEW = 7
  FIRST_INTERVIEW = 8
  FIRST_INTERVIEW_PASS = 9
  FIRST_INTERVIEW_FAILED = 10
  INVITE_SECOND_INTERVIEW = 11
  SECOND_INTERVIEW = 12
  SECOND_INTERVIEW_PASS = 13
  SECOND_INTERVIEW_FAILED = 14
  SEND_OFFER = 15
  ACCEPT_OFFER = 16
  REFUSE_OFFER = 17
  SEND_FORM = 18
  ALL_OK = 19
  NOT_INTERVIEW = 20
  UPDATED_FORM = 21
  TUTORIAL = 22
  BLACK_LIST = 23
  NOT_TEST = 24
  NOT_START_WORKING = 25
  QUIT_JOB = 26

# Positions id
class Positions(enum.IntEnum):
  INTERNSHIP = 1
  STAFF = 2
  LEADER = 3
  MANAGER = 4
  COLLABORATORS = 5
  ADMIN = 6

# Render flag
class RenderFlag(enum.IntEnum):
  RENDER_AUTO_GG = 0
  SELF_ENTER = 1

# Interview status
class InterviewStatus(enum.IntEnum):
  PREPARE_INTERVIEW = 0
  PASS = 1
  FAILED = 2
  NOT_TEST = 8
  NOT_INTERVIEW = 9

# Interview type
class InterviewType(enum.IntEnum):
  TEST = 0
  FIRST_INTERVIEW = 1
  SECOND_INTERVIEW =2

class Evaluate(enum.IntEnum):
  NOT_INTERVIEW_YET = 0
  PASS = 1
  FAILED = 2

class InterviewForm(enum.IntEnum):
  OFFLINE = 1
  ONLINE = 2

class Office(enum.IntEnum):
  HANOI = 1
  HUE = 2

class Gender(enum.IntEnum):
  MALE = 0
  FEMALE = 1
  UNKNOWN = 2

class Team(enum.IntEnum):
  """
    Team
  """
  C_SHARP = 1
  PHP = 2
  JAVA = 3
  DESIGNER = 4
  NODEJS = 5
  PYTHON = 6
  FRONTEND = 7
  CPLUS = 8
  FLUTTER = 9
  REACTJS = 10
  COMTOR = 11
  QAQC = 12
  CTV = 13
  TESTER = 14
  ADMIN = 15

# Custom class IntEnum
class IntEnum(db.TypeDecorator):
  """
  Enables passing in a Python enum and storing the enum's *value* in the db.
  The default would have stored the enum's *name* (ie the string).
  """
  impl = db.Integer
  cache_ok = True

  def __init__(self, enumtype, *args, **kwargs):
    super(IntEnum, self).__init__(*args, **kwargs)
    self._enumtype = enumtype

  def process_bind_param(self, value, dialect):
    if isinstance(value, int):
      return value

    return value.value

  def process_result_value(self, value, dialect):
    return self._enumtype(value)
