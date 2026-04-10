from dataclasses import dataclass
from typing import Tuple


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
