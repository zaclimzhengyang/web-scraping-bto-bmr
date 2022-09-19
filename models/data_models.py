from datetime import datetime

from pydantic import BaseModel

from models.bto_enums import EthnicType, BlockType


class UnitInformation(BaseModel):
    unit_number: str
    unit_size_sqm: int
    unit_price_sgd: int
    ethnic_type: EthnicType
    block_type: BlockType
    created_at: datetime
    available: bool


def convert_unit_size_sqm_to_unit_size(unit_size_string: str) -> int:
    """
    convert '89 sqm' to int 89
    """
    unit_size_string = unit_size_string.replace(' sqm', '')
    return int(unit_size_string)


def convert_price_string_to_price(price_string: str) -> int:
    """
    convert '$729,500' to int 729500
    """
    price_string = price_string.replace('$', '')
    price_string = price_string.replace(',', '')
    return int(price_string)