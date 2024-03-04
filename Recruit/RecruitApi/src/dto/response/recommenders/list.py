"""
List recommenders response model
"""

from typing import List
from pydantic import BaseModel
from .recommender import RecommenderItemResponse

class ListRecommendersResponse(BaseModel):
  item: List[RecommenderItemResponse]
