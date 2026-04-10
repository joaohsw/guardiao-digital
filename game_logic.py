from typing import Optional, Tuple

import pygame

import game_assets
import game_state
from game_config import ATTACKS, PLAYER_SPEED, SCREEN_SIZE
from game_models import Villain


def reset_progress() -> None:
    game_state.player_health = game_state.max_player_health
    game_state.player_position.x = game_state.START_CENTER[0]
    game_state.player_position.y = game_state.START_CENTER[1]
    game_state.active_villain_id = None
    game_state.feedback_active = False
    game_state.feedback_title = ""
    game_state.feedback_message = ""
    game_state.feedback_tone = "neutral"
    game_state.encounter_lock_villain_id = None
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
    keys = pygame.key.get_pressed()
    horizontal = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
    vertical = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
    move_player_continuous(horizontal, vertical, dt)
    try_trigger_encounter()


def try_trigger_encounter() -> None:
    villain = game_state.find_villain_touching_player()

    if game_state.encounter_lock_villain_id is not None:
        if villain is None or villain.id != game_state.encounter_lock_villain_id:
            game_state.encounter_lock_villain_id = None
        else:
            return

    if villain is not None:
        game_state.active_villain_id = villain.id
        game_state.game_state = "encounter"


def calculate_attack_damage(attack: dict, villain: Villain) -> Tuple[int, str]:
    damage = attack["base_damage"]
    effectiveness = "normal"

    if attack["type"] == villain.weakness:
        damage += 6
        effectiveness = "fraqueza"
    elif attack["type"] == villain.resistance:
        damage = max(4, damage - 6)
        effectiveness = "resistencia"

    return damage, effectiveness


def open_battle_feedback(title: str, message: str, tone: str) -> None:
    game_state.feedback_active = True
    game_state.feedback_title = title
    game_state.feedback_message = message
    game_state.feedback_tone = tone


def resolve_battle_turn(selected_index: int) -> None:
    villain = game_state.get_active_villain()
    if villain is None:
        return

    attack = ATTACKS[selected_index]
    damage, effectiveness = calculate_attack_damage(attack, villain)
    villain.health = max(0, villain.health - damage)

    if effectiveness == "fraqueza":
        attack_result = f"{attack['name']} explorou a fraqueza do inimigo e causou {damage} de dano."
    elif effectiveness == "resistencia":
        attack_result = f"{attack['name']} encontrou resistencia e causou apenas {damage} de dano."
    else:
        attack_result = f"{attack['name']} causou {damage} de dano."

    if villain.health <= 0:
        villain.defeated = True
        open_battle_feedback(
            "Vilao neutralizado",
            f"{attack_result} {villain.crime['enemy_name']} foi derrotado.",
            "victory",
        )
        return

    game_state.player_health = max(0, game_state.player_health - villain.counter_damage)
    counter_result = (
        f"{villain.crime['enemy_name']} contra-atacou e causou "
        f"{villain.counter_damage} de dano a sua integridade."
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


def key_to_attack_index(event_key: int) -> Optional[int]:
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
