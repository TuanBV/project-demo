"""
Initialization Package
"""

from .repository import CandidatesPassListRepository
from .services import CandidatesPassListService


__all__ = [
  "CandidatesPassListService",
  "CandidatesPassListRepository",
]
