import sys
from typing import Optional

import pygame

import game_assets
import game_logic
import game_render
import game_state
from game_config import BATTLE_OPTION_RECTS, FPS


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
                    game_state.encounter_lock_villain_id = game_state.active_villain_id
                    game_state.active_villain_id = None
                    game_state.game_state = "exploring"
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.game_state = "battle"

            elif game_state.game_state == "battle":
                if game_state.feedback_active:
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                        game_logic.close_feedback_and_continue()
                else:
                    selected_index: Optional[int] = None
                    if event.type == pygame.KEYDOWN:
                        selected_index = game_logic.key_to_attack_index(event.key)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for index, rect in enumerate(BATTLE_OPTION_RECTS):
                            if rect.collidepoint(event.pos):
                                selected_index = index
                                break

                    if selected_index is not None:
                        game_logic.resolve_battle_turn(selected_index)

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
        elif game_state.game_state == "battle":
            game_render.draw_battle_screen()
        elif game_state.game_state == "conclusion":
            game_render.draw_conclusion_screen()
        elif game_state.game_state in ("victory", "game_over"):
            game_render.draw_end_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
