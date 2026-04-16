from typing import Optional, Tuple

import pygame

import game_assets
import game_state
from game_config import (
    BATTLE_OPTION_RECTS,
    COUNTER_DAMAGE_MODIFIERS,
    EFFECTIVENESS_DAMAGE,
    NON_FINISHING_EFFECTS,
    PLAYER_SPEED,
    SCREEN_SIZE,
    SUBATTACK_OPTION_RECTS,
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
    game_state.active_villain_id = None
    game_state.feedback_active = False
    game_state.feedback_title = ""
    game_state.feedback_message = ""
    game_state.feedback_tone = "neutral"
    game_state.encounter_lock_villain_id = None
    for drop in game_state.collectible_drops:
        drop.collected = False
    for villain in game_state.villains:
        villain.defeated = False
        villain.health = villain.max_health


def move_player_continuous(input_x: int, input_y: int, dt: float) -> None:
    if input_x == 0 and input_y == 0:
        return

    move_vector = pygame.Vector2(input_x, input_y)
    if move_vector.length_squared() > 1:
        move_vector = move_vector.normalize()
    move_vector *= PLAYER_SPEED * dt

    next_x = game_state.player_position.x + move_vector.x
    if not game_state.hitbox_collides_with_wall(game_state.build_player_hitbox(next_x, game_state.player_position.y)):
        game_state.player_position.x = next_x

    next_y = game_state.player_position.y + move_vector.y
    if not game_state.hitbox_collides_with_wall(game_state.build_player_hitbox(game_state.player_position.x, next_y)):
        game_state.player_position.y = next_y


def update_exploration(dt: float) -> None:
    game_state.update_map_notice(dt)
    keys = pygame.key.get_pressed()
    horizontal = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
    vertical = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
    move_player_continuous(horizontal, vertical, dt)
    collect_touched_drop()
    try_trigger_encounter()


def collect_touched_drop() -> None:
    drop = game_state.find_collectible_touching_player()
    if drop is not None:
        game_state.collect_drop(drop)


def try_trigger_encounter() -> None:
    villain = game_state.find_villain_touching_player()

    if game_state.encounter_lock_villain_id is not None:
        if villain is None or villain.id != game_state.encounter_lock_villain_id:
            game_state.encounter_lock_villain_id = None
        else:
            return

    if villain is not None:
        if not game_state.has_any_attack():
            game_state.encounter_lock_villain_id = villain.id
            game_state.show_map_notice("Encontre pelo menos um tipo de ataque antes de lutar.", 3.2)
            return
        game_state.active_villain_id = villain.id
        game_state.game_state = "encounter"


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

    if effectiveness == "forte":
        attack_result = f"{attack['name']} foi uma escolha forte, teve alto efeito e bloqueou o contra-ataque."
    elif effectiveness == "medio":
        attack_result = f"{attack['name']} funcionou bem e teve efeito normal."
    elif effectiveness == "fraco":
        attack_result = f"{attack['name']} ajudou pouco contra essa ameaca."
    else:
        attack_result = f"{attack['name']} teve efeito parcial. Ataques neutros nao finalizam a ameaca sozinhos."

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
    game_state.selected_attack_category = None
    game_state.feedback_active = False
    game_state.active_villain_id = None
    game_state.encounter_lock_villain_id = fleeing_villain_id
    game_state.game_state = "exploring"
    game_state.show_map_notice("Voce fugiu da luta e voltou ao mapa.", 2.6)


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
    game_assets.fullscreen = not game_assets.fullscreen
    if game_assets.fullscreen:
        game_assets.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    else:
        game_assets.screen = pygame.display.set_mode(SCREEN_SIZE)

