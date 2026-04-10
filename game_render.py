import pygame

import game_assets
import game_state
from game_config import (
    ATTACKS,
    BATTLE_OPTION_RECTS,
    BUTTON_BORDER,
    BUTTON_COLOR,
    CONCLUSION_TEXT,
    GAME_STORY,
    GREEN,
    GRID_COLOR,
    HUD_BG,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    PANEL_BG,
    PATH_COLOR,
    PATH_COLOR_ALT,
    RED,
    SCREEN_HEIGHT,
    SCREEN_SIZE,
    SCREEN_WIDTH,
    START_COLOR,
    TEXT_DARK,
    TILE_SIZE,
    WALL_COLOR,
    WALL_COLOR_ALT,
    WHITE,
    WORLD_MAP_LAYOUT,
)
from game_models import Villain
from game_ui import draw_panel, draw_text, draw_text_block


def draw_health_bar(surface: pygame.Surface, x: int, y: int) -> None:
    draw_text("Integridade", game_assets.help_font, WHITE, surface, x, y)
    bar_x = x + 140
    bar_y = y + 2
    segment_width = 40
    segment_height = 16
    total_width = segment_width * game_state.max_player_health
    pygame.draw.rect(surface, RED, (bar_x, bar_y, total_width, segment_height), border_radius=3)
    if game_state.player_health > 0:
        pygame.draw.rect(
            surface,
            GREEN,
            (bar_x, bar_y, segment_width * game_state.player_health, segment_height),
            border_radius=3,
        )


def draw_menu_screen() -> None:
    game_assets.screen.blit(game_assets.menu_image, (0, 0))

    title_panel = pygame.Rect(180, 92, 920, 240)
    draw_panel(title_panel)
    draw_text(
        "GUARDI\u00c3O DIGITAL 2",
        game_assets.menu_font,
        WHITE,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        155,
        center=True,
    )
    draw_text(
        "Explore o mapa, encontre viloes e neutralize crimes digitais",
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        220,
        center=True,
    )
    draw_text(
        "ENTER ou clique para iniciar",
        game_assets.title_font,
        WHITE,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        282,
        center=True,
    )
    draw_text("F11 alterna tela cheia", game_assets.help_font, WHITE, game_assets.screen, SCREEN_WIDTH - 180, 12)


def draw_story_screen() -> None:
    game_assets.screen.blit(game_assets.historia_bg, (0, 0))
    portrait_rect = game_assets.player_image_portrait.get_rect(center=(SCREEN_WIDTH * 0.20, SCREEN_HEIGHT * 0.54))
    game_assets.screen.blit(game_assets.player_image_portrait, portrait_rect)

    story_panel = pygame.Rect(450, 92, 760, 530)
    draw_panel(story_panel)
    draw_text("Missao no mapa", game_assets.title_font, WHITE, game_assets.screen, story_panel.centerx, 136, center=True)
    draw_text_block(
        GAME_STORY,
        game_assets.story_font,
        WHITE,
        game_assets.screen,
        story_panel.x + 45,
        story_panel.y + 205,
        story_panel.width - 90,
        center=False,
    )
    draw_text(
        "Pressione ENTER ou clique para explorar",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        story_panel.centerx,
        story_panel.bottom - 40,
        center=True,
    )


def draw_world_screen() -> None:
    game_assets.screen.fill((23, 32, 31))

    for row_index, row in enumerate(WORLD_MAP_LAYOUT):
        for col_index, cell in enumerate(row):
            tile_rect = game_state.tile_to_rect(col_index, row_index)
            if cell == "#":
                color = WALL_COLOR if (row_index + col_index) % 2 == 0 else WALL_COLOR_ALT
            elif cell == "S":
                color = START_COLOR
            else:
                color = PATH_COLOR if (row_index + col_index) % 2 == 0 else PATH_COLOR_ALT
            pygame.draw.rect(game_assets.screen, color, tile_rect)

    pygame.draw.rect(
        game_assets.screen,
        GRID_COLOR,
        (MAP_OFFSET_X - 2, MAP_OFFSET_Y - 2, MAP_WIDTH + 4, MAP_HEIGHT + 4),
        2,
    )

    for drop in game_state.collectible_drops:
        if drop.collected:
            continue
        center_x, center_y = drop.world_pos
        pygame.draw.circle(game_assets.screen, (238, 226, 157), (center_x, center_y), TILE_SIZE // 2 - 12)
        sprite = game_assets.collectible_images[drop.asset_key]
        sprite_rect = sprite.get_rect(center=(center_x, center_y))
        game_assets.screen.blit(sprite, sprite_rect)

    for villain in game_state.villains:
        if villain.defeated:
            continue
        center_x, center_y = villain.world_pos
        pygame.draw.circle(game_assets.screen, (163, 42, 42), (center_x, center_y), TILE_SIZE // 2 - 6)
        sprite = game_assets.map_enemy_images[villain.id]
        sprite_rect = sprite.get_rect(center=(center_x, center_y))
        game_assets.screen.blit(sprite, sprite_rect)

    player_center = (round(game_state.player_position.x), round(game_state.player_position.y))
    player_rect = game_assets.player_image_map.get_rect(center=player_center)
    game_assets.screen.blit(game_assets.player_image_map, player_rect)

    hud = pygame.Surface((SCREEN_WIDTH, 84), pygame.SRCALPHA)
    hud.fill(HUD_BG)
    game_assets.screen.blit(hud, (0, 0))
    draw_health_bar(game_assets.screen, 14, 11)
    draw_text(
        f"Viloes restantes: {game_state.remaining_villains_count()}",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        14,
        38,
    )
    draw_text(
        f"Drops coletados: {game_state.collected_drops_count()}/{len(game_state.collectible_drops)}",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        14,
        62,
    )
    draw_text(
        "Mover livremente: segure WASD/Setas | Toque no vilao para iniciar encontro",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        17,
        center=True,
    )
    draw_text("F11: tela cheia", game_assets.help_font, WHITE, game_assets.screen, SCREEN_WIDTH - 180, 11)


def draw_encounter_screen() -> None:
    villain = game_state.get_active_villain()
    if villain is None:
        return

    game_assets.screen.blit(game_assets.introducao_bg, (0, 0))
    crime = villain.crime
    enemy_image = game_assets.dossier_enemy_images[villain.id]

    encounter_panel = pygame.Rect(180, 92, 920, 548)
    draw_panel(encounter_panel)

    draw_text(crime["enemy_name"], game_assets.title_font, WHITE, game_assets.screen, encounter_panel.centerx, 138, center=True)
    image_rect = enemy_image.get_rect(center=(encounter_panel.centerx, 265))
    game_assets.screen.blit(enemy_image, image_rect)
    draw_text_block(
        crime["description"],
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        encounter_panel.x + 54,
        encounter_panel.y + 330,
        encounter_panel.width - 108,
        center=False,
    )
    draw_text(
        "ENTER/click: enfrentar | ESC: voltar ao mapa",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        encounter_panel.centerx,
        encounter_panel.bottom - 28,
        center=True,
    )


def draw_enemy_health_bar(surface: pygame.Surface, villain: Villain, x: int, y: int, width: int = 320) -> None:
    draw_text("Estabilidade do inimigo", game_assets.help_font, WHITE, surface, x, y)
    bar_rect = pygame.Rect(x, y + 18, width, 18)
    pygame.draw.rect(surface, RED, bar_rect, border_radius=4)
    if villain.health > 0:
        current_width = int(width * (villain.health / villain.max_health))
        pygame.draw.rect(surface, GREEN, (bar_rect.x, bar_rect.y, current_width, bar_rect.height), border_radius=4)
    draw_text(f"{villain.health}/{villain.max_health}", game_assets.help_font, WHITE, surface, bar_rect.right - 52, y - 1)


def draw_feedback_overlay() -> None:
    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    if game_state.feedback_tone == "victory":
        overlay.fill((0, 100, 0, 180))
    elif game_state.feedback_tone == "defeat":
        overlay.fill((110, 0, 0, 180))
    else:
        overlay.fill((20, 55, 90, 180))
    game_assets.screen.blit(overlay, (0, 0))
    feedback_panel = pygame.Rect(140, 120, 1000, 450)
    draw_panel(feedback_panel, (15, 20, 24, 220))

    draw_text(
        game_state.feedback_title,
        game_assets.feedback_font,
        WHITE,
        game_assets.screen,
        feedback_panel.centerx,
        186,
        center=True,
    )
    draw_text_block(
        game_state.feedback_message,
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        feedback_panel.x + 58,
        feedback_panel.y + 230,
        feedback_panel.width - 116,
        center=False,
    )

    if game_state.player_health <= 0:
        footer = "Integridade zerada. ENTER ou clique para continuar."
    else:
        villain = game_state.get_active_villain()
        villain_defeated = villain.defeated if villain is not None else False
        if villain_defeated and game_state.all_villains_defeated():
            footer = "Todos os viloes foram derrotados. ENTER ou clique para concluir a missao."
        elif villain_defeated:
            footer = "Vilao neutralizado. ENTER ou clique para voltar ao mapa."
        else:
            footer = "ENTER ou clique para continuar o combate."

    draw_text(
        footer,
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        feedback_panel.centerx,
        feedback_panel.bottom - 35,
        center=True,
    )


def draw_battle_screen() -> None:
    villain = game_state.get_active_villain()
    if villain is None:
        return

    game_assets.screen.blit(game_assets.combate_bg, (0, 0))

    enemy_pos = (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.29))
    player_pos = (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.54))

    enemy_image = game_assets.combat_enemy_images[villain.id]
    enemy_rect = enemy_image.get_rect(center=enemy_pos)
    game_assets.screen.blit(enemy_image, enemy_rect)

    player_rect = game_assets.player_image_combat.get_rect(center=player_pos)
    game_assets.screen.blit(game_assets.player_image_combat, player_rect)

    battle_header = pygame.Rect(230, 16, 820, 92)
    draw_panel(battle_header, (18, 24, 28, 200))
    draw_text(villain.crime["enemy_name"], game_assets.title_font, WHITE, game_assets.screen, battle_header.centerx, 40, center=True)
    draw_health_bar(game_assets.screen, battle_header.x + 26, 73)
    draw_enemy_health_bar(game_assets.screen, villain, battle_header.right - 348, 46)

    info_panel = pygame.Rect(160, 365, 960, 112)
    draw_panel(info_panel, (18, 24, 28, 200))
    draw_text_block(
        villain.crime["description"],
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        info_panel.x + 30,
        info_panel.y + 24,
        info_panel.width - 60,
        center=False,
    )

    for index, attack in enumerate(ATTACKS):
        option_rect = BATTLE_OPTION_RECTS[index]
        pygame.draw.rect(game_assets.screen, BUTTON_COLOR, option_rect, border_radius=10)
        pygame.draw.rect(game_assets.screen, BUTTON_BORDER, option_rect, 2, border_radius=10)
        labeled_option = f"{index + 1}. {attack['name']}\nTipo: {attack['type']} | Dano: {attack['base_damage']}"
        draw_text_block(
            labeled_option,
            game_assets.option_font,
            TEXT_DARK,
            game_assets.screen,
            option_rect.centerx,
            option_rect.centery,
            option_rect.width - 30,
            center=True,
            line_gap=2,
        )

    draw_text(
        "Escolha um ataque com clique ou teclas 1-4",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 14,
        center=True,
    )

    if game_state.feedback_active:
        draw_feedback_overlay()


def draw_conclusion_screen() -> None:
    game_assets.screen.blit(game_assets.conclusao_bg, (0, 0))
    conclusion_panel = pygame.Rect(160, 96, 960, 536)
    draw_panel(conclusion_panel)
    draw_text("Missao concluida", game_assets.title_font, GREEN, game_assets.screen, conclusion_panel.centerx, 146, center=True)
    draw_text_block(
        CONCLUSION_TEXT,
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        conclusion_panel.x + 60,
        conclusion_panel.y + 220,
        conclusion_panel.width - 120,
        center=False,
    )
    draw_text(
        "ENTER ou clique para tela de vitoria",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        conclusion_panel.centerx,
        conclusion_panel.bottom - 30,
        center=True,
    )


def draw_end_screen() -> None:
    if game_state.game_state == "victory":
        game_assets.screen.blit(game_assets.vitoria_image, (0, 0))
    elif game_state.game_state == "game_over":
        game_assets.screen.blit(game_assets.derrota_image, (0, 0))

    end_panel = pygame.Rect(290, 618, 700, 56)
    draw_panel(end_panel, (18, 24, 28, 200))
    draw_text(
        "ENTER ou clique para voltar ao menu",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        end_panel.centerx,
        end_panel.centery,
        center=True,
    )
