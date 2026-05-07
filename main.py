import sys
from typing import Optional

import pygame

import game_assets
import game_logic
import game_render
import game_state
from game_config import (
    BOOK_CLOSE_RECT,
    BOOK_HUD_RECT,
    BOOK_NEXT_RECT,
    BOOK_PREV_RECT,
    FPS,
    WARNING_BACK_RECT,
    WARNING_PROCEED_RECT,
)
from game_config import BATTLE_FLEE_RECT


def main() -> None:
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                game_logic.toggle_fullscreen()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and game_state.book_collected
                and game_state.game_state in ("exploring", "encounter", "battle")
                and BOOK_HUD_RECT.collidepoint(event.pos)
            ):
                game_logic.open_book_screen()
                continue

            if game_state.game_state == "menu":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_logic.reset_progress()
                    game_state.game_state = "exploring"

            elif game_state.game_state == "story":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.game_state = "exploring"

            elif game_state.game_state == "exploring":
                pass

            elif game_state.game_state == "encounter":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_logic.cancel_encounter()
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.selected_attack_category = None
                    game_state.game_state = "battle"

            elif game_state.game_state == "requirement_warning":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_logic.resolve_requirement_warning(True)
                    elif event.key == pygame.K_ESCAPE:
                        game_logic.resolve_requirement_warning(False)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if WARNING_PROCEED_RECT.collidepoint(event.pos):
                        game_logic.resolve_requirement_warning(True)
                    elif WARNING_BACK_RECT.collidepoint(event.pos):
                        game_logic.resolve_requirement_warning(False)

            elif game_state.game_state == "battle":
                if game_state.feedback_active:
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                        game_logic.close_feedback_and_continue()
                else:
                    selected_attack: Optional[dict] = None
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE and game_state.selected_attack_category is not None:
                            game_state.selected_attack_category = None
                        elif event.key == pygame.K_ESCAPE:
                            game_logic.flee_battle()
                        elif game_state.selected_attack_category is None:
                            selected_index = game_logic.key_to_category_index(event.key)
                            categories = game_logic.get_available_battle_categories()
                            if selected_index is not None and selected_index < len(categories):
                                game_logic.select_battle_category(categories[selected_index])
                        else:
                            selected_index = game_logic.key_to_subattack_index(event.key)
                            attacks = game_logic.get_available_battle_attacks()
                            if selected_index is not None and selected_index < len(attacks):
                                selected_attack = attacks[selected_index]
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if BATTLE_FLEE_RECT.collidepoint(event.pos):
                            game_logic.flee_battle()
                            continue
                        if game_state.selected_attack_category is None:
                            game_logic.select_battle_category_at_pos(event.pos)
                        else:
                            selected_attack = game_logic.get_battle_attack_at_pos(event.pos)

                    if selected_attack is not None:
                        game_logic.resolve_battle_turn(selected_attack)

            elif game_state.game_state == "book":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        game_logic.close_book_screen()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        game_logic.next_book_page()
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        game_logic.previous_book_page()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if BOOK_CLOSE_RECT.collidepoint(event.pos):
                        game_logic.close_book_screen()
                    elif BOOK_NEXT_RECT.collidepoint(event.pos):
                        game_logic.next_book_page()
                    elif BOOK_PREV_RECT.collidepoint(event.pos):
                        game_logic.previous_book_page()

            elif game_state.game_state == "conclusion":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.game_state = "victory"

            elif game_state.game_state in ("victory", "game_over"):
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.game_state = "menu"

        if game_state.game_state == "exploring":
            game_logic.update_exploration(dt)

        if game_state.game_state == "menu":
            game_render.draw_menu_screen()
        elif game_state.game_state == "story":
            game_render.draw_story_screen()
        elif game_state.game_state == "exploring":
            game_render.draw_world_screen()
        elif game_state.game_state == "encounter":
            game_render.draw_encounter_screen()
        elif game_state.game_state == "requirement_warning":
            game_render.draw_requirement_warning_screen()
        elif game_state.game_state == "battle":
            game_render.draw_battle_screen()
        elif game_state.game_state == "book":
            game_render.draw_book_screen()
        elif game_state.game_state == "conclusion":
            game_render.draw_conclusion_screen()
        elif game_state.game_state in ("victory", "game_over"):
            game_render.draw_end_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
