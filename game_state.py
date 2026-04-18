from typing import List, Optional, Set, Tuple

import pygame

import game_assets
from game_config import (
    ATTACK_CATEGORIES,
    ATTACK_EFFECTIVENESS,
    BOOK_PAGE_SIZE,
    CATEGORY_ATTACKS,
    COLLECTIBLE_DROPS,
    ENEMY_COMBAT_PROFILES,
    ENEMY_KEYS,
    ENEMY_REQUIRED_WEAPON,
    MAP_COLS,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_ROWS,
    MAP_WIDTH,
    PLAYER_HITBOX_SIZE,
    TILE_SIZE,
    VILLAIN_SPAWNS,
    VILLAIN_TRIGGER_PADDING,
    WORLD_MAP_LAYOUT,
    crimes,
)
from game_models import CollectibleDrop, Villain


def find_start_tile() -> Tuple[int, int]:
    for row_index, row in enumerate(WORLD_MAP_LAYOUT):
        for col_index, cell in enumerate(row):
            if cell == "S":
                return col_index, row_index
    return 1, 1


def tile_is_walkable(tile_x: int, tile_y: int) -> bool:
    if tile_x < 0 or tile_y < 0 or tile_x >= MAP_COLS or tile_y >= MAP_ROWS:
        return False
    return WORLD_MAP_LAYOUT[tile_y][tile_x] != "#"


def tile_to_rect(tile_x: int, tile_y: int) -> pygame.Rect:
    return pygame.Rect(
        MAP_OFFSET_X + tile_x * TILE_SIZE,
        MAP_OFFSET_Y + tile_y * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE,
    )


def tile_to_center(tile_x: int, tile_y: int) -> Tuple[int, int]:
    rect = tile_to_rect(tile_x, tile_y)
    return rect.centerx, rect.centery


START_TILE = find_start_tile()
START_CENTER = tile_to_center(START_TILE[0], START_TILE[1])

villains: List[Villain] = []
for crime_index, crime_data in enumerate(crimes):
    fallback_pos = START_TILE
    spawn = VILLAIN_SPAWNS[crime_index] if crime_index < len(VILLAIN_SPAWNS) else fallback_pos
    combat_profile = ENEMY_COMBAT_PROFILES[crime_index]
    enemy_key = ENEMY_KEYS[crime_index] if crime_index < len(ENEMY_KEYS) else f"inimigo_{crime_index}"
    if not tile_is_walkable(spawn[0], spawn[1]):
        spawn = fallback_pos
    villains.append(
        Villain(
            id=crime_index,
            enemy_key=enemy_key,
            crime=crime_data,
            tile_pos=spawn,
            world_pos=tile_to_center(spawn[0], spawn[1]),
            max_health=combat_profile["max_health"],
            health=combat_profile["max_health"],
            weakness=combat_profile["weakness"],
            resistance=combat_profile["resistance"],
            counter_damage=combat_profile["counter_damage"],
            required_weapon_type=ENEMY_REQUIRED_WEAPON.get(enemy_key),
        )
    )

collectible_drops: List[CollectibleDrop] = []
for drop_data in COLLECTIBLE_DROPS:
    drop_tile = drop_data["tile_pos"]
    if not tile_is_walkable(drop_tile[0], drop_tile[1]):
        continue
    collectible_drops.append(
        CollectibleDrop(
            id=drop_data["id"],
            name=drop_data["name"],
            category=drop_data["category"],
            tile_pos=drop_tile,
            world_pos=tile_to_center(drop_tile[0], drop_tile[1]),
            asset_key=drop_data["asset_key"],
            weapon_type=drop_data.get("weapon_type"),
            heal_amount=drop_data.get("heal_amount", 0),
        )
    )

player_health = 5
max_player_health = 5
player_position = pygame.Vector2(START_CENTER[0], START_CENTER[1])
last_safe_player_position = pygame.Vector2(START_CENTER[0], START_CENTER[1])
game_state = "menu"
active_villain_id: Optional[int] = None
warning_villain_id: Optional[int] = None
feedback_active = False
feedback_title = ""
feedback_message = ""
feedback_tone = "neutral"
encounter_lock_villain_id: Optional[int] = None
book_collected = False
collected_categories: Set[str] = set()
unlocked_attacks: Set[str] = set()
selected_attack_category: Optional[str] = None
last_game_state = "exploring"
map_notice_message = ""
map_notice_timer = 0.0
book_page = 0


def get_villain_by_id(villain_id: Optional[int]) -> Optional[Villain]:
    if villain_id is None:
        return None
    for villain in villains:
        if villain.id == villain_id:
            return villain
    return None


def get_active_villain() -> Optional[Villain]:
    return get_villain_by_id(active_villain_id)


def get_warning_villain() -> Optional[Villain]:
    return get_villain_by_id(warning_villain_id)


def get_required_weapon_name_for_villain(villain: Villain) -> Optional[str]:
    required_type = villain.required_weapon_type
    if required_type is None:
        return None
    category_data = ATTACK_CATEGORIES.get(required_type)
    if category_data is None:
        return required_type.replace("_", " ").title()
    return category_data["name"]


def can_face_villain(villain: Villain) -> bool:
    required_type = villain.required_weapon_type
    if required_type is None:
        return True
    return required_type in collected_categories


def remaining_villains_count() -> int:
    return sum(1 for villain in villains if not villain.defeated)


def all_villains_defeated() -> bool:
    return remaining_villains_count() == 0


def build_player_hitbox(x: float, y: float) -> pygame.Rect:
    rect = pygame.Rect(0, 0, PLAYER_HITBOX_SIZE, PLAYER_HITBOX_SIZE)
    rect.center = (round(x), round(y))
    return rect


def get_player_hitbox() -> pygame.Rect:
    return build_player_hitbox(player_position.x, player_position.y)


def get_collectible_rect(drop: CollectibleDrop) -> pygame.Rect:
    image = game_assets.collectible_images[drop.asset_key]
    return image.get_rect(center=drop.world_pos)


def hitbox_collides_with_wall(hitbox: pygame.Rect) -> bool:
    if (
        hitbox.left < MAP_OFFSET_X
        or hitbox.top < MAP_OFFSET_Y
        or hitbox.right > MAP_OFFSET_X + MAP_WIDTH
        or hitbox.bottom > MAP_OFFSET_Y + MAP_HEIGHT
    ):
        return True

    start_col = max(0, (hitbox.left - MAP_OFFSET_X) // TILE_SIZE)
    end_col = min(MAP_COLS - 1, (hitbox.right - 1 - MAP_OFFSET_X) // TILE_SIZE)
    start_row = max(0, (hitbox.top - MAP_OFFSET_Y) // TILE_SIZE)
    end_row = min(MAP_ROWS - 1, (hitbox.bottom - 1 - MAP_OFFSET_Y) // TILE_SIZE)

    for row_index in range(start_row, end_row + 1):
        for col_index in range(start_col, end_col + 1):
            if WORLD_MAP_LAYOUT[row_index][col_index] != "#":
                continue
            if hitbox.colliderect(tile_to_rect(col_index, row_index)):
                return True
    return False


def find_villain_touching_player() -> Optional[Villain]:
    player_hitbox = get_player_hitbox()
    for villain in villains:
        if villain.defeated:
            continue
        enemy_rect = game_assets.map_enemy_images[villain.id].get_rect(center=villain.world_pos).inflate(
            VILLAIN_TRIGGER_PADDING,
            VILLAIN_TRIGGER_PADDING,
        )
        if player_hitbox.colliderect(enemy_rect):
            return villain
    return None


def show_map_notice(message: str, duration: float = 3.5) -> None:
    global map_notice_message, map_notice_timer
    map_notice_message = message
    map_notice_timer = duration


def update_map_notice(dt: float) -> None:
    global map_notice_message, map_notice_timer
    if map_notice_timer <= 0:
        return
    map_notice_timer = max(0.0, map_notice_timer - dt)
    if map_notice_timer == 0:
        map_notice_message = ""


def find_collectible_touching_player() -> Optional[CollectibleDrop]:
    player_hitbox = get_player_hitbox()
    for drop in collectible_drops:
        if drop.collected:
            continue
        if player_hitbox.colliderect(get_collectible_rect(drop)):
            return drop
    return None


def collected_drops_count() -> int:
    return sum(1 for drop in collectible_drops if drop.collected)


def collect_drop(drop: CollectibleDrop) -> None:
    global book_collected, player_health
    if drop.category == "healing":
        if player_health >= max_player_health:
            full_health_notice = "Integridade ja esta no maximo. Volte quando precisar de cura."
            if map_notice_message != full_health_notice:
                show_map_notice(full_health_notice, 2.8)
            return
        drop.collected = True
        healed_amount = max(1, drop.heal_amount)
        previous_health = player_health
        player_health = min(max_player_health, player_health + healed_amount)
        recovered = player_health - previous_health
        show_map_notice(f"Integridade recuperada em +{recovered}.", 2.8)
        return

    drop.collected = True
    if drop.category == "book":
        book_collected = True
        show_map_notice(
            "Parab\u00e9ns! Voc\u00ea coletou o Guia Digital M\u00e1gico que ajudar\u00e1 voc\u00ea no combate!",
            4.5,
        )
        return

    if drop.category == "weapon" and drop.weapon_type is not None:
        collected_categories.add(drop.weapon_type)
        for attack in CATEGORY_ATTACKS.get(drop.weapon_type, []):
            unlocked_attacks.add(attack["id"])
        show_map_notice(f"Categoria de ataque coletada: {drop.name}.", 2.8)


def has_any_attack() -> bool:
    return len(unlocked_attacks) > 0


def get_unlocked_categories() -> List[str]:
    return [category for category in CATEGORY_ATTACKS if category in collected_categories]


def get_unlocked_attacks_for_category(category: str) -> List[dict]:
    return [attack for attack in CATEGORY_ATTACKS.get(category, []) if attack["id"] in unlocked_attacks]


def get_attack_by_id(attack_id: str) -> Optional[dict]:
    for attacks in CATEGORY_ATTACKS.values():
        for attack in attacks:
            if attack["id"] == attack_id:
                return attack
    return None


def get_attack_effectiveness(enemy_key: str, attack_id: str) -> str:
    enemy_table = ATTACK_EFFECTIVENESS.get(enemy_key, {})
    for effectiveness in ("forte", "medio", "fraco"):
        if attack_id in enemy_table.get(effectiveness, []):
            return effectiveness
    return "neutro"


def get_book_entries() -> List[Tuple[str, dict]]:
    return list(ATTACK_EFFECTIVENESS.items())


def get_book_page_count() -> int:
    entries_count = len(get_book_entries())
    return max(1, (entries_count + BOOK_PAGE_SIZE - 1) // BOOK_PAGE_SIZE)


def get_current_book_entries() -> List[Tuple[str, dict]]:
    start = book_page * BOOK_PAGE_SIZE
    end = start + BOOK_PAGE_SIZE
    return get_book_entries()[start:end]
