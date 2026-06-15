from typing import Optional, Tuple

import pygame

import game_assets
import game_state
from game_config import (
    BATTLE_BACK_RECT,
    BATTLE_OPTION_RECTS,
    COUNTER_DAMAGE_MODIFIERS,
    EFFECTIVENESS_DAMAGE,
    NON_FINISHING_EFFECTS,
    PLAYER_SPEED,
    SUBATTACK_OPTION_RECTS,
    THREAT_STRATEGY_HINTS,
)
from game_models import Villain


def reset_progress() -> None:
    game_state.book_collected = False
    game_state.collected_categories.clear()
    game_state.unlocked_attacks.clear()
    game_state.selected_attack_category = None
    game_state.last_game_state = "exploring"
    game_state.map_notice_message = ""
    game_state.map_notice_timer = 0.0
    game_state.book_page = 0
    game_state.player_health = game_state.max_player_health
    game_state.player_position.x = game_state.START_CENTER[0]
    game_state.player_position.y = game_state.START_CENTER[1]
    game_state.last_safe_player_position.x = game_state.START_CENTER[0]
    game_state.last_safe_player_position.y = game_state.START_CENTER[1]
    game_state.active_villain_id = None
    game_state.warning_villain_id = None
    game_state.feedback_active = False
    game_state.feedback_title = ""
    game_state.feedback_message = ""
    game_state.feedback_tone = "neutral"
    game_state.encounter_lock_villain_id = None
    game_state.reset_player_animation()
    for drop in game_state.collectible_drops:
        drop.collected = False
    for villain in game_state.villains:
        villain.defeated = False
        villain.health = villain.max_health


def move_player_continuous(input_x: int, input_y: int, dt: float) -> pygame.Vector2:
    applied_movement = pygame.Vector2(0, 0)
    if input_x == 0 and input_y == 0:
        return applied_movement

    move_vector = pygame.Vector2(input_x, input_y)
    if move_vector.length_squared() > 1:
        move_vector = move_vector.normalize()
    move_vector *= PLAYER_SPEED * dt

    next_x = game_state.player_position.x + move_vector.x
    if not game_state.hitbox_collides_with_wall(game_state.build_player_hitbox(next_x, game_state.player_position.y)):
        game_state.player_position.x = next_x
        applied_movement.x = move_vector.x

    next_y = game_state.player_position.y + move_vector.y
    if not game_state.hitbox_collides_with_wall(game_state.build_player_hitbox(game_state.player_position.x, next_y)):
        game_state.player_position.y = next_y
        applied_movement.y = move_vector.y

    return applied_movement


def update_exploration(dt: float) -> None:
    game_state.update_map_notice(dt)
    keys = pygame.key.get_pressed()
    horizontal = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
    vertical = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
    movement = move_player_continuous(horizontal, vertical, dt)
    game_state.update_player_walk_animation(movement, dt)
    collect_touched_drop()
    try_trigger_encounter()


def collect_touched_drop() -> None:
    drop = game_state.find_collectible_touching_player()
    if drop is not None:
        game_state.collect_drop(drop)


def try_trigger_encounter() -> None:
    villain = game_state.find_villain_touching_player()

    if villain is None:
        game_state.last_safe_player_position.x = game_state.player_position.x
        game_state.last_safe_player_position.y = game_state.player_position.y
        game_state.encounter_lock_villain_id = None
        return

    if game_state.encounter_lock_villain_id == villain.id:
        return

    game_state.encounter_lock_villain_id = None
    if not game_state.can_face_villain(villain):
        game_state.warning_villain_id = villain.id
        game_state.game_state = "requirement_warning"
        return
    game_state.active_villain_id = villain.id
    game_state.game_state = "encounter"


def retreat_from_villain(
    villain_id: Optional[int],
    notice: str,
    duration: float = 2.6,
    keep_encounter_lock: bool = True,
) -> None:
    game_state.selected_attack_category = None
    game_state.feedback_active = False
    game_state.active_villain_id = None
    game_state.warning_villain_id = None
    game_state.player_position.x = game_state.last_safe_player_position.x
    game_state.player_position.y = game_state.last_safe_player_position.y
    game_state.encounter_lock_villain_id = villain_id if keep_encounter_lock else None
    game_state.game_state = "exploring"
    game_state.show_map_notice(notice, duration)


def cancel_encounter() -> None:
    retreat_from_villain(
        game_state.active_villain_id,
        "Voce recuou do confronto e voltou ao mapa.",
        keep_encounter_lock=False,
    )


def resolve_requirement_warning(proceed_anyway: bool) -> None:
    warning_villain_id = game_state.warning_villain_id
    game_state.warning_villain_id = None

    if warning_villain_id is None:
        game_state.game_state = "exploring"
        return

    if proceed_anyway:
        game_state.active_villain_id = warning_villain_id
        game_state.selected_attack_category = None
        game_state.game_state = "encounter"
        return

    retreat_from_villain(
        warning_villain_id,
        "Volte quando estiver mais preparado para esse confronto.",
        2.8,
        keep_encounter_lock=False,
    )


def start_battle() -> None:
    game_state.selected_attack_category = None
    game_state.game_state = "battle"


def open_story_screen(return_state: str = "exploring") -> None:
    game_state.last_game_state = return_state
    game_state.game_state = "story"


def close_story_screen() -> None:
    if game_state.last_game_state in ("exploring", "paused"):
        game_state.game_state = game_state.last_game_state
        return
    game_state.game_state = "exploring"


def calculate_attack_effect(attack: dict, villain: Villain) -> Tuple[int, str]:
    effectiveness = game_state.get_attack_effectiveness(villain.enemy_key, attack["id"])
    damage = EFFECTIVENESS_DAMAGE[effectiveness]
    return damage, effectiveness


def calculate_effective_damage(villain: Villain, damage: int, effectiveness: str) -> int:
    if effectiveness in NON_FINISHING_EFFECTS and villain.health - damage <= 0:
        return max(0, villain.health - 1)
    return damage


def calculate_counter_damage(villain: Villain, effectiveness: str) -> int:
    modifier = COUNTER_DAMAGE_MODIFIERS.get(effectiveness, 0)
    return max(0, villain.counter_damage + modifier)


def build_subtle_attack_hint(villain: Villain, effectiveness: str) -> str:
    hints = THREAT_STRATEGY_HINTS.get(villain.enemy_key)
    if hints is None:
        return "Pista: observe melhor o comportamento dessa ameaca antes do proximo movimento."

    hint_index_by_effectiveness = {
        "eficaz": 0,
        "medio": 1,
        "ineficaz": 2,
    }
    hint_index = hint_index_by_effectiveness.get(effectiveness, 0)
    return f"Pista: {hints[hint_index]}"


def open_battle_feedback(title: str, message: str, tone: str) -> None:
    game_state.feedback_active = True
    game_state.feedback_title = title
    game_state.feedback_message = message
    game_state.feedback_tone = tone


def open_book_screen() -> None:
    if not game_state.book_collected:
        return
    game_state.last_game_state = game_state.game_state
    game_state.game_state = "book"


def close_book_screen() -> None:
    game_state.game_state = game_state.last_game_state


def next_book_page() -> None:
    page_count = game_state.get_book_page_count()
    game_state.book_page = min(page_count - 1, game_state.book_page + 1)


def previous_book_page() -> None:
    game_state.book_page = max(0, game_state.book_page - 1)


def get_available_battle_categories() -> list[str]:
    return game_state.get_unlocked_categories()


def get_available_battle_attacks() -> list[dict]:
    if game_state.selected_attack_category is None:
        return []
    return game_state.get_unlocked_attacks_for_category(game_state.selected_attack_category)


def select_battle_category(category: str) -> None:
    if category in game_state.get_unlocked_categories():
        game_state.selected_attack_category = category


def return_to_battle_categories() -> None:
    game_state.selected_attack_category = None


def handle_battle_back_button(pos: Tuple[int, int]) -> bool:
    if game_state.selected_attack_category is None:
        return False
    if not BATTLE_BACK_RECT.collidepoint(pos):
        return False
    return_to_battle_categories()
    return True


def select_battle_category_at_pos(pos: Tuple[int, int]) -> bool:
    categories = get_available_battle_categories()
    for index, category in enumerate(categories):
        if index >= len(BATTLE_OPTION_RECTS):
            break
        if BATTLE_OPTION_RECTS[index].collidepoint(pos):
            select_battle_category(category)
            return True
    return False


def get_battle_attack_at_pos(pos: Tuple[int, int]) -> Optional[dict]:
    attacks = get_available_battle_attacks()
    for index, attack in enumerate(attacks):
        if index >= len(SUBATTACK_OPTION_RECTS):
            break
        if SUBATTACK_OPTION_RECTS[index].collidepoint(pos):
            return attack
    return None


def key_to_category_index(event_key: int) -> Optional[int]:
    key_map = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_KP1: 0,
        pygame.K_KP2: 1,
        pygame.K_KP3: 2,
        pygame.K_KP4: 3,
    }
    return key_map.get(event_key)


def key_to_subattack_index(event_key: int) -> Optional[int]:
    key_map = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_5: 4,
        pygame.K_KP1: 0,
        pygame.K_KP2: 1,
        pygame.K_KP3: 2,
        pygame.K_KP4: 3,
        pygame.K_KP5: 4,
    }
    return key_map.get(event_key)


def resolve_battle_turn(attack: dict) -> None:
    villain = game_state.get_active_villain()
    if villain is None:
        return

    base_damage, effectiveness = calculate_attack_effect(attack, villain)
    damage = calculate_effective_damage(villain, base_damage, effectiveness)
    villain.health = max(0, villain.health - damage)

    if effectiveness == "extremo":
        attack_result = f"{attack['name']} abriu uma brecha decisiva e bloqueou o contra-ataque."
    elif effectiveness == "eficaz":
        attack_result = f"{attack['name']} pressionou bem a ameaca e causou dano consistente."
    elif effectiveness == "medio":
        attack_result = f"{attack['name']} teve algum efeito, mas nao explorou totalmente a falha."
    else:
        attack_result = f"{attack['name']} quase nao abalou a ameaca."

    if effectiveness != "extremo":
        attack_result = f"{attack_result} {build_subtle_attack_hint(villain, effectiveness)}"

    if villain.health <= 0:
        villain.defeated = True
        open_battle_feedback(
            "Vilao neutralizado",
            f"{attack_result} {villain.crime['enemy_name']} foi derrotado.",
            "victory",
        )
        return

    counter_damage = calculate_counter_damage(villain, effectiveness)
    game_state.player_health = max(0, game_state.player_health - counter_damage)
    if counter_damage == 0:
        counter_result = f"{villain.crime['enemy_name']} nao conseguiu contra-atacar neste turno."
    else:
        counter_result = (
            f"{villain.crime['enemy_name']} contra-atacou e causou "
            f"{counter_damage} de dano a sua integridade."
        )

    if game_state.player_health <= 0:
        open_battle_feedback(
            "Integridade comprometida",
            f"{attack_result} {counter_result}",
            "defeat",
        )
    else:
        open_battle_feedback(
            "Troca de golpes",
            f"{attack_result} {counter_result}",
            "neutral",
        )


def flee_battle() -> None:
    fleeing_villain_id = game_state.active_villain_id
    retreat_from_villain(
        fleeing_villain_id,
        "Voce fugiu da luta e voltou ao mapa.",
        keep_encounter_lock=False,
    )


def close_feedback_and_continue() -> None:
    previous_villain_id = game_state.active_villain_id
    game_state.feedback_active = False
    if game_state.player_health <= 0:
        game_state.active_villain_id = None
        game_state.game_state = "game_over"
        return

    villain = game_state.get_active_villain()
    if villain is not None and villain.defeated:
        game_state.active_villain_id = None
        game_state.selected_attack_category = None
        if game_state.all_villains_defeated():
            game_state.game_state = "conclusion"
            return
        game_state.encounter_lock_villain_id = previous_villain_id
        game_state.game_state = "exploring"
        return

    game_state.game_state = "battle"


def toggle_fullscreen() -> None:
    game_assets.toggle_fullscreen()


def set_resolution(resolution: Tuple[int, int]) -> None:
    game_assets.set_resolution(resolution)

