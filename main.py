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
    BATTLE_FLEE_RECT,
    ENCOUNTER_FIGHT_RECT,
    ENCOUNTER_FLEE_RECT,
    PAUSE_CONTINUE_RECT,
    PAUSE_SETTINGS_RECT,
    PAUSE_MENU_RECT,
    PAUSE_QUIT_RECT,
)


def main() -> None:
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            mouse_pos = game_assets.window_to_game_pos(event.pos) if hasattr(event, "pos") else None
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                game_logic.toggle_fullscreen()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and game_state.book_collected
                and game_state.game_state in ("exploring", "encounter", "battle")
                and mouse_pos is not None
                and BOOK_HUD_RECT.collidepoint(mouse_pos)
            ):
                game_logic.open_book_screen()
                continue

            if game_state.game_state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_logic.reset_progress()
                    game_state.game_state = "exploring"
                elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos is not None:
                    if game_assets.menu_play_button_rect.collidepoint(mouse_pos):
                        game_logic.reset_progress()
                        game_state.game_state = "exploring"
                    elif game_assets.menu_settings_button_rect.collidepoint(mouse_pos):
                        game_state.settings_resolution_dropdown_open = False
                        game_state.last_game_state = "menu"
                        game_state.game_state = "settings"

            elif game_state.game_state == "settings":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game_state.settings_resolution_dropdown_open:
                            game_state.settings_resolution_dropdown_open = False
                        else:
                            game_state.settings_resolution_dropdown_open = False
                            game_state.game_state = game_state.last_game_state
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        game_logic.toggle_fullscreen()
                elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos is not None:
                    if game_render.get_settings_fullscreen_rect().collidepoint(mouse_pos):
                        game_logic.toggle_fullscreen()
                    elif game_render.get_settings_back_rect().collidepoint(mouse_pos):
                        game_state.settings_resolution_dropdown_open = False
                        game_state.game_state = game_state.last_game_state
                    elif game_render.get_settings_resolution_toggle_rect().collidepoint(mouse_pos):
                        game_state.settings_resolution_dropdown_open = not game_state.settings_resolution_dropdown_open
                    elif game_state.settings_resolution_dropdown_open:
                        selected_resolution = game_render.get_settings_resolution_at_pos(mouse_pos)
                        if selected_resolution is not None:
                            game_logic.set_resolution(selected_resolution)
                        game_state.settings_resolution_dropdown_open = False

            elif game_state.game_state == "story":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.game_state = "exploring"

            elif game_state.game_state == "exploring":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state.game_state = "paused"

            elif game_state.game_state == "paused":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state.game_state = "exploring"
                elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos is not None:
                    if PAUSE_CONTINUE_RECT.collidepoint(mouse_pos):
                        game_state.game_state = "exploring"
                    elif PAUSE_SETTINGS_RECT.collidepoint(mouse_pos):
                        game_state.settings_resolution_dropdown_open = False
                        game_state.last_game_state = "paused"
                        game_state.game_state = "settings"
                    elif PAUSE_MENU_RECT.collidepoint(mouse_pos):
                        game_state.game_state = "menu"
                    elif PAUSE_QUIT_RECT.collidepoint(mouse_pos):
                        running = False

            elif game_state.game_state == "encounter":
                if event.type == pygame.MOUSEBUTTONDOWN and mouse_pos is not None:
                    if ENCOUNTER_FIGHT_RECT.collidepoint(mouse_pos):
                        game_logic.start_battle()
                    elif ENCOUNTER_FLEE_RECT.collidepoint(mouse_pos):
                        game_logic.cancel_encounter()

            elif game_state.game_state == "requirement_warning":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_logic.resolve_requirement_warning(True)
                    elif event.key == pygame.K_ESCAPE:
                        game_logic.resolve_requirement_warning(False)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_pos is not None and WARNING_PROCEED_RECT.collidepoint(mouse_pos):
                        game_logic.resolve_requirement_warning(True)
                    elif mouse_pos is not None and WARNING_BACK_RECT.collidepoint(mouse_pos):
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
                    elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos is not None:
                        if BATTLE_FLEE_RECT.collidepoint(mouse_pos):
                            game_logic.flee_battle()
                            continue
                        if game_state.selected_attack_category is None:
                            game_logic.select_battle_category_at_pos(mouse_pos)
                        else:
                            selected_attack = game_logic.get_battle_attack_at_pos(mouse_pos)

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
                    if mouse_pos is not None and BOOK_CLOSE_RECT.collidepoint(mouse_pos):
                        game_logic.close_book_screen()
                    elif mouse_pos is not None and BOOK_NEXT_RECT.collidepoint(mouse_pos):
                        game_logic.next_book_page()
                    elif mouse_pos is not None and BOOK_PREV_RECT.collidepoint(mouse_pos):
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
        elif game_state.game_state == "settings":
            game_render.draw_settings_screen()
        elif game_state.game_state == "story":
            game_render.draw_story_screen()
        elif game_state.game_state == "exploring":
            game_render.draw_world_screen()
        elif game_state.game_state == "paused":
            game_render.draw_world_screen()
            game_render.draw_pause_screen()
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

        game_assets.present()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
