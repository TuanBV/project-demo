"""
Initialization Package
"""

from .users import user_routers
from .recommenders import recommender_routers
from .candidates import candidate_routers
from .positions import position_routers
from .teams import team_routers
from .templates import template_routers
from .parameters import parameter_routers
from .offices import offices_routers
from .mails import mail_routers
from .candidates_confirm import candidate_confirm_routers
from .candidates_list import candidates_routers
from .meeting_rooms import meeting_room_routers
from .candidates_pass import candidate_pass_list_routers
from .black_list import black_list_routers
from .staff_list import staff_routers

__all__ = [
  "user_routers",
  "recommender_routers",
  "candidate_routers",
  "position_routers",
  "team_routers",
  "template_routers",
  "parameter_routers",
  "offices_routers",
  "mail_routers",
  "candidate_confirm_routers",
  "candidates_routers",
  "meeting_room_routers",
  "candidate_pass_list_routers",
  "black_list_routers",
  "staff_routers",
]
