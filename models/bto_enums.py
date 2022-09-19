from enum import Enum


class SelectionType(str, Enum):
    flat_type: str = "Choose Flat Type"
    ethnic_type: str = "Choose Ethnic Type"
    block_type: str = "Choose Block No."
    unknown: str = "Unknown"

    @classmethod
    def _missing_(cls, value):
        return cls.unknown


class EthnicType(str, Enum):
    chinese: str = "Chinese"
    indian_or_other_races: str = "Indian/Other Races"
    malay: str = "Malay"


class BlockType(str, Enum):
    blk_132a: str = "Blk 132A"
    blk_134a: str = "Blk 134A"
    blk_135a: str = "Blk 135A"
    blk_136a: str = "Blk 136A"
    blK_137a: str = "Blk 137A"