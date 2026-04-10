from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Villain:
    id: int
    crime: dict
    tile_pos: Tuple[int, int]
    world_pos: Tuple[int, int]
    max_health: int
    health: int
    weakness: str
    resistance: str
    counter_damage: int
    defeated: bool = False


@dataclass
class CollectibleDrop:
    id: str
    name: str
    category: str
    tile_pos: Tuple[int, int]
    world_pos: Tuple[int, int]
    asset_key: str
    weapon_type: Optional[str] = None
    collected: bool = False
