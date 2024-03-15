"""
Setting rank shop request
"""

from __future__ import annotations

from pydantic import BaseModel, Field
import helpers.const as env


class DataRankOfAmountPurchase(BaseModel):
  rank_s: str = Field(..., regex=env.REGEXP.RANK, title="Rank s")
  rank_a: str = Field(..., regex=env.REGEXP.RANK, title="Rank a")
  rank_b: str = Field(..., regex=env.REGEXP.RANK, title="Rank b")
  rank_c: str = Field(..., regex=env.REGEXP.RANK, title="Rank c")

class DataRankOfNumberVisit(BaseModel):
  rank_s_visit: str = Field(..., regex=env.REGEXP.RANK, title="Rank s")
  rank_a_visit: str = Field(..., regex=env.REGEXP.RANK, title="Rank a")
  rank_b_visit: str = Field(..., regex=env.REGEXP.RANK, title="Rank b")
  rank_c_visit: str = Field(..., regex=env.REGEXP.RANK, title="Rank c")


class DataAmountPurchase(BaseModel):
  range_date: str = Field(..., title="The range date", regex=r"^[0-5]|null$")
  rank: DataRankOfAmountPurchase

class DataNumberVisit(BaseModel):
  range_date: str = Field(..., title="The range date", regex=r"^[0-5]|null$")
  rank: DataRankOfNumberVisit

class SettingShopEditRankRequest(BaseModel):
  amount_purchase: DataAmountPurchase
  number_visit: DataNumberVisit
