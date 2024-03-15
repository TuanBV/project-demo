"""
  Request of campaign
"""

from typing import Optional
from pydantic import BaseModel, Field, validator
from utils.date import get_object_date, format_date_time


class SettingShopCampaignRequest(BaseModel):
  """
    Request setting shop campaign
  """
  campaign_note: Optional[str] = None
  campaign_point:  Optional[str] = Field(None, title="point", regex=r"^[1-9]([0-9]{0,6})$|^$")
  point_default: str = Field(title="The point default", regex="^[1-9]([0-9]{0,6})$")
  campaign_start_date: Optional[str] = None
  campaign_end_date: Optional[str] = None

  @validator("campaign_start_date")
  # Convert datetime of campaign_start_date
  def convert_campaign_start_date(cls, campaign_start_date):
    if campaign_start_date:
      return format_date_time(get_object_date(campaign_start_date, "%Y/%m/%d"), "%Y-%m-%d")

    return None

  @validator("campaign_end_date")
  # Convert datetime of campaign_end_date
  def convert_campaign_end_date(cls, campaign_end_date):
    if campaign_end_date:
      return format_date_time(get_object_date(campaign_end_date, "%Y/%m/%d"), "%Y-%m-%d")

    return None

class SettingShopNotifyRequest(BaseModel):
  content: str = Field(default="")


class RankShopRequest(BaseModel):
  kbn: int
  range_date: int = Field(default=0)
  rank_s: str
  rank_a: str
  rank_b: str
  rank_c: str


class SettingShopRequest(BaseModel):
  color: str
  logo: str = Field(default="")
  logo_size: str = Field(default="")
  logo_ext: str = Field(default="")
  name: str
  slogan: str = Field(default="")
