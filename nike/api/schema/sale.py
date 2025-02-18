import re
from datetime import datetime
from typing import Optional, List
from core import CommonException
from pydantic import BaseModel, Field, model_validator


class SaleRequest(BaseModel):
    """
        Model request sale
    """
    name: str = Field(..., title="The username")
    file: Optional[str] = Field(..., title="The image file")
    file_ext: Optional[str] = Field(..., title="The ext file")
    file_size: Optional[int] = Field(..., title="The size file")
    discount: int = Field(..., title="The discount")
    start_date: str = Field(..., title="Start date")
    end_date: str = Field(..., title="End date")

    @model_validator(mode='after')
    def validate_model(self):
        """
            Validate the data request
        """
        message_list = []
        # Validate for name of sale program
        if not self.name or not self.name.strip():
            message_list.append("Name must have at least 1 character.")
        if len(self.name) > 256:
            message_list.append("Name cannot be longer than 256 characters.")

        # Check discount
        if self.discount < 0 or self.discount > 100:
            message_list.append("Discount is greater than 0 and must be between 0 and 100")
        pattern_date = r'^\d{4}-\d{2}-\d{2}$'
        # If start_date and end_date are null then return value

        if self.start_date and not bool(re.match(pattern_date, self.start_date)):
            message_list.append("Start date is invalid")
        if self.end_date and not bool(re.match(pattern_date, self.end_date)):
            message_list.append("End date is invalid")

        time_current = datetime.today().date()
        if bool(re.match(pattern_date, self.start_date)):
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            if start_date < time_current:
                message_list.append("Start date is greater than current date")
        if bool(re.match(pattern_date, self.end_date)):
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            if end_date < start_date:
                message_list.append("End date is greater than start date")

        if message_list:
            raise CommonException(message=message_list)
        return self

class SaleResponse(BaseModel):
    """
        Response sale
    """
    id: int
    name: str
    discount: int
    image: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    flg_del: int

class ListSaleResponse(BaseModel):
    """
        Response list sale
    """
    item: Optional[List[SaleResponse]] = None
