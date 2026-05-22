import pygame
from typing import Optional


import game_assets
import game_state
from game_config import (
    ATTACK_CATEGORIES,
    BATTLE_BACK_RECT,
    BATTLE_FLEE_RECT,
    BATTLE_OPTION_RECTS,
    BOOK_CLOSE_RECT,
    BOOK_NEXT_RECT,
    BOOK_PREV_RECT,
    BOOK_HUD_RECT,
    BUTTON_BORDER,
    BUTTON_COLOR,
    CONCLUSION_TEXT,
    GAME_STORY,
    GREEN,
    HUD_BG,
    PANEL_BG,
    RED,
    SCREEN_HEIGHT,
    SCREEN_SIZE,
    SCREEN_WIDTH,
    START_COLOR,
    SUBATTACK_OPTION_RECTS,
    TEXT_DARK,
    THREAT_STRATEGY_HINTS,
    TILE_SIZE,
    VICTORY_MENU_RECT,
    VICTORY_QUIT_RECT,
    WARNING_BACK_RECT,
    WARNING_PROCEED_RECT,
    WHITE,
    WORLD_MAP_LAYOUT,
    ENCOUNTER_FIGHT_RECT,
    ENCOUNTER_FLEE_RECT,
    BATTLE_BUTTON_COLOR,
    BATTLE_BUTTON_BORDER,
    BATTLE_TEXT,
    DEFEAT_BUTTON_COLOR,
    DEFEAT_BUTTON_BORDER,
    DEFEAT_TEXT,
    DEFEAT_MENU_RECT,
    DEFEAT_QUIT_RECT,
    PAUSE_PANEL_RECT,
    PAUSE_CONTINUE_RECT,
    PAUSE_SETTINGS_RECT,
    PAUSE_MENU_RECT,
    PAUSE_QUIT_RECT,
)
from game_models import Villain
from game_ui import draw_panel, draw_text, draw_text_block


ENEMY_BOOK_NAMES = {
    "adware": "Adware",
    "malware": "Malware",
    "phishing": "Phishing",
    "senha": "Senha fraca",
    "ransomware": "Ransomware",
    "spyware": "Spyware",
    "golpe": "Golpe",
    "deepfake": "Deepfake",
    "pirataria": "Pirataria",
    "cyberstalking": "Cyberstalking",
}


def get_attack_display_name(attack_id: str) -> str:
    attack = game_state.get_attack_by_id(attack_id)
    if attack is None:
        return attack_id.replace("_", " ")
    return attack["name"]


def format_attack_list(attack_ids: list[str]) -> str:
    return ", ".join(get_attack_display_name(attack_id) for attack_id in attack_ids)


def format_book_attack_name(attack_ids: list[str]) -> str:
    if not attack_ids:
        return "-"
    return get_attack_display_name(attack_ids[0])


def draw_health_bar(surface: pygame.Surface, x: int, y: int) -> None:
    # Removed label "Integridade" text to draw hearts directly at the starting x position
    gap = 6
    heart_size = 20
    for i in range(game_state.max_player_health):
        hx = x + i * (heart_size + gap)
        hy = y
        filled = i < game_state.player_health

        # Draw black outline (slightly larger)
        pygame.draw.circle(surface, (15, 20, 25), (hx + 5, hy + 6), 6)
        pygame.draw.circle(surface, (15, 20, 25), (hx + 14, hy + 6), 6)
        pygame.draw.polygon(surface, (15, 20, 25), [(hx, hy + 7), (hx + 20, hy + 7), (hx + 10, hy + 20)])

        if filled:
            # Ruby red heart
            pygame.draw.circle(surface, (231, 76, 60), (hx + 5, hy + 6), 5)
            pygame.draw.circle(surface, (231, 76, 60), (hx + 14, hy + 6), 5)
            pygame.draw.polygon(surface, (231, 76, 60), [(hx + 1, hy + 7), (hx + 19, hy + 7), (hx + 10, hy + 19)])
            # Gloss highlight
            pygame.draw.circle(surface, (255, 255, 255), (hx + 3, hy + 4), 1)
        else:
            # Slate grey/empty heart container
            pygame.draw.circle(surface, (40, 44, 52), (hx + 5, hy + 6), 5)
            pygame.draw.circle(surface, (40, 44, 52), (hx + 14, hy + 6), 5)
            pygame.draw.polygon(surface, (40, 44, 52), [(hx + 1, hy + 7), (hx + 19, hy + 7), (hx + 10, hy + 19)])
            # Subtle empty slot highlight
            pygame.draw.circle(surface, (70, 75, 85), (hx + 3, hy + 4), 1)


def draw_book_hud_button() -> None:
    if not game_state.book_collected:
        return
    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, BOOK_HUD_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, BOOK_HUD_RECT, 2, border_radius=8)
    icon = game_assets.collectible_images["book"]
    bounds = icon.get_bounding_rect(min_alpha=8)
    if bounds.width > 0 and bounds.height > 0:
        icon = icon.subsurface(bounds).copy()
    
    # Scale proportionally to fit inside 36x36 without squishing
    orig_w, orig_h = icon.get_size()
    max_dim = 30
    if orig_w > orig_h:
        new_w = max_dim
        new_h = int(orig_h * (max_dim / orig_w))
    else:
        new_h = max_dim
        new_w = int(orig_w * (max_dim / orig_h))
    
    icon_scaled = pygame.transform.smoothscale(icon, (max(1, new_w), max(1, new_h)))
    icon_rect = icon_scaled.get_rect(center=BOOK_HUD_RECT.center)
    game_assets.screen.blit(icon_scaled, icon_rect)


def draw_battle_flee_hud_button() -> None:
    hovered = BATTLE_FLEE_RECT.collidepoint(game_assets.get_virtual_mouse_pos())
    fill_color = (237, 233, 214) if hovered else BUTTON_COLOR
    pygame.draw.rect(game_assets.screen, fill_color, BATTLE_FLEE_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, BATTLE_FLEE_RECT, 2, border_radius=8)
    draw_text(
        "Fugir",
        game_assets.help_font,
        TEXT_DARK,
        game_assets.screen,
        BATTLE_FLEE_RECT.centerx,
        BATTLE_FLEE_RECT.centery - 1,
        center=True,
    )


def draw_combat_back_button() -> None:
    hovered = BATTLE_BACK_RECT.collidepoint(game_assets.get_virtual_mouse_pos())
    draw_rect = BATTLE_BACK_RECT.inflate(6, 6) if hovered else BATTLE_BACK_RECT
    image = game_assets.get_combat_back_arrow_image(draw_rect.size)
    if hovered:
        image = image.copy()
        image.fill((32, 32, 32, 0), special_flags=pygame.BLEND_RGBA_ADD)
    game_assets.screen.blit(image, draw_rect.topleft)


def draw_cyber_button(
    rect: pygame.Rect,
    text: str,
    fill_color: tuple[int, int, int, int] = BATTLE_BUTTON_COLOR,
    border_color: tuple[int, int, int] = BATTLE_BUTTON_BORDER,
    text_color: tuple[int, int, int] = BATTLE_TEXT,
    hover_color: tuple[int, int, int, int] = (0, 200, 220, 30),
) -> None:
    btn_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    btn_surf.fill(fill_color)
    game_assets.screen.blit(btn_surf, rect.topleft)
    pygame.draw.rect(game_assets.screen, border_color, rect, 2, border_radius=4)
    draw_text(
        text,
        game_assets.help_font,
        text_color,
        game_assets.screen,
        rect.centerx,
        rect.centery - 1,
        center=True,
    )
    if rect.collidepoint(game_assets.get_virtual_mouse_pos()):
        hover_overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
        hover_overlay.fill(hover_color)
        game_assets.screen.blit(hover_overlay, rect.topleft)


def draw_attack_categories() -> None:
    categories = game_state.get_unlocked_categories()
    for index, category in enumerate(categories):
        if index >= len(BATTLE_OPTION_RECTS):
            break
        option_rect = BATTLE_OPTION_RECTS[index]
        category_data = ATTACK_CATEGORIES[category]
        draw_cyber_button(option_rect, f"{index + 1}. {category_data['name']}")


def draw_attack_options() -> None:
    if game_state.selected_attack_category is None:
        return

    category_name = ATTACK_CATEGORIES[game_state.selected_attack_category]["name"]
    attacks = game_state.get_unlocked_attacks_for_category(game_state.selected_attack_category)
    draw_combat_back_button()
    draw_text(
        f"Categoria: {category_name}",
        game_assets.description_font,
        BATTLE_TEXT,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        480,
        center=True,
    )
    for index, attack in enumerate(attacks):
        if index >= len(SUBATTACK_OPTION_RECTS):
            break
        option_rect = SUBATTACK_OPTION_RECTS[index]
        draw_cyber_button(option_rect, f"{index + 1}. {attack['name']}")


def draw_map_notice() -> None:
    if not game_state.map_notice_message:
        return
    notice_rect = pygame.Rect(250, SCREEN_HEIGHT - 78, 780, 46)
    draw_panel(notice_rect, (18, 24, 28, 225))
    draw_text(
        game_state.map_notice_message,
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        notice_rect.centerx,
        notice_rect.centery - 2,
        center=True,
    )


def draw_back_image_button(rect: pygame.Rect, hovered: bool = False) -> None:
    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, rect, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, rect, 2, border_radius=8)
    draw_text(
        "Voltar",
        game_assets.help_font,
        TEXT_DARK,
        game_assets.screen,
        rect.centerx,
        rect.centery - 1,
        center=True,
    )
    if hovered:
        hover_overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
        hover_overlay.fill((255, 255, 255, 34))
        game_assets.screen.blit(hover_overlay, rect.topleft)


def draw_proceed_image_button(rect: pygame.Rect, hovered: bool = False) -> None:
    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, rect, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, rect, 2, border_radius=8)
    draw_text(
        "Prosseguir",
        game_assets.help_font,
        TEXT_DARK,
        game_assets.screen,
        rect.centerx,
        rect.centery - 1,
        center=True,
    )
    if hovered:
        hover_overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
        hover_overlay.fill((255, 255, 255, 34))
        game_assets.screen.blit(hover_overlay, rect.topleft)


def get_settings_panel_rect() -> pygame.Rect:
    return pygame.Rect(166, 76, 948, 568)


def get_settings_fullscreen_rect() -> pygame.Rect:
    panel = get_settings_panel_rect()
    return pygame.Rect(panel.x + 84, panel.y + 96, panel.width - 168, 66)


def get_settings_resolution_toggle_rect() -> pygame.Rect:
    panel = get_settings_panel_rect()
    return pygame.Rect(panel.x + 84, panel.y + 206, panel.width - 168, 56)


def get_settings_resolution_rects() -> list[tuple[tuple[int, int], pygame.Rect]]:
    toggle_rect = get_settings_resolution_toggle_rect()
    option_height = 34
    option_gap = 4
    resolution_buttons: list[tuple[tuple[int, int], pygame.Rect]] = []
    for index, resolution in enumerate(game_assets.resolution_options):
        y = toggle_rect.bottom + 8 + index * (option_height + option_gap)
        resolution_buttons.append((resolution, pygame.Rect(toggle_rect.x, y, toggle_rect.width, option_height)))
    return resolution_buttons


def get_settings_resolution_at_pos(pos: tuple[int, int]) -> Optional[tuple[int, int]]:
    for resolution, rect in get_settings_resolution_rects():
        if rect.collidepoint(pos):
            return resolution
    return None


def get_settings_back_rect() -> pygame.Rect:
    panel = get_settings_panel_rect()
    return pygame.Rect(panel.centerx - 150, panel.bottom - 84, 300, 54)


def draw_menu_screen() -> None:
    game_assets.screen.blit(game_assets.menu_image, (0, 0))
    mouse_pos = game_assets.get_virtual_mouse_pos()

    for button_image, button_rect in (
        (game_assets.menu_play_button_image, game_assets.menu_play_button_rect),
        (game_assets.menu_settings_button_image, game_assets.menu_settings_button_rect),
    ):
        game_assets.screen.blit(button_image, button_rect)
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(game_assets.screen, (138, 255, 255), button_rect.inflate(24, 14), 2, border_radius=24)


def draw_settings_screen() -> None:
    game_assets.screen.blit(game_assets.settings_background, (0, 0))
    mouse_pos = game_assets.get_virtual_mouse_pos()

    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((6, 12, 15, 82))
    game_assets.screen.blit(overlay, (0, 0))

    panel = get_settings_panel_rect()
    draw_panel(panel, (10, 17, 21, 222))
    pygame.draw.rect(game_assets.screen, (83, 195, 202), panel, 2, border_radius=12)

    draw_text("Configuracoes", game_assets.title_font, WHITE, game_assets.screen, panel.centerx, panel.y + 40, center=True)
    draw_text(
        "Ajustes de exibicao",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        panel.centerx,
        panel.y + 72,
        center=True,
    )

    fullscreen_rect = get_settings_fullscreen_rect()
    is_fullscreen = game_assets.fullscreen
    fullscreen_hovered = fullscreen_rect.collidepoint(mouse_pos)
    fill_color = (41, 112, 120) if is_fullscreen else BUTTON_COLOR
    if fullscreen_hovered and not is_fullscreen:
        fill_color = (239, 235, 216)
    text_color = WHITE if is_fullscreen else TEXT_DARK
    status_text = "Ligado" if is_fullscreen else "Desligado"

    pygame.draw.rect(game_assets.screen, fill_color, fullscreen_rect, border_radius=12)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, fullscreen_rect, 2, border_radius=12)
    draw_text(
        f"Tela cheia: {status_text}",
        game_assets.description_font,
        text_color,
        game_assets.screen,
        fullscreen_rect.centerx,
        fullscreen_rect.centery - 8,
        center=True,
    )
    draw_text(
        "Clique para alternar",
        game_assets.help_font,
        text_color,
        game_assets.screen,
        fullscreen_rect.centerx,
        fullscreen_rect.centery + 17,
        center=True,
    )

    draw_text("Resolucao", game_assets.description_font, WHITE, game_assets.screen, panel.x + 92, panel.y + 184)

    toggle_rect = get_settings_resolution_toggle_rect()
    toggle_hovered = toggle_rect.collidepoint(mouse_pos)
    toggle_fill = (237, 233, 214) if toggle_hovered else BUTTON_COLOR
    pygame.draw.rect(game_assets.screen, toggle_fill, toggle_rect, border_radius=10)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, toggle_rect, 2, border_radius=10)

    current_resolution = game_assets.current_resolution
    current_resolution_text = f"{current_resolution[0]} x {current_resolution[1]}"
    draw_text(
        current_resolution_text,
        game_assets.description_font,
        TEXT_DARK,
        game_assets.screen,
        toggle_rect.x + 20,
        toggle_rect.centery - 14,
    )
    arrow_text = "^" if game_state.settings_resolution_dropdown_open else "v"
    draw_text(
        arrow_text,
        game_assets.description_font,
        TEXT_DARK,
        game_assets.screen,
        toggle_rect.right - 24,
        toggle_rect.centery - 14,
        center=True,
    )

    if game_state.settings_resolution_dropdown_open:
        for resolution, rect in get_settings_resolution_rects():
            selected = resolution == current_resolution
            hovered = rect.collidepoint(mouse_pos)
            if selected:
                button_fill = (40, 118, 126)
                button_text = WHITE
            else:
                button_fill = BUTTON_COLOR
                button_text = TEXT_DARK
                if hovered:
                    button_fill = (238, 234, 214)

            pygame.draw.rect(game_assets.screen, button_fill, rect, border_radius=8)
            pygame.draw.rect(game_assets.screen, BUTTON_BORDER, rect, 2, border_radius=8)
            draw_text(
                f"{resolution[0]} x {resolution[1]}",
                game_assets.help_font,
                button_text,
                game_assets.screen,
                rect.x + 18,
                rect.centery - 8,
            )

    back_rect = get_settings_back_rect()
    draw_back_image_button(back_rect, back_rect.collidepoint(mouse_pos))
    draw_text(
        "ESC para retornar | F11 para tela cheia",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        panel.centerx,
        panel.bottom - 18,
        center=True,
    )


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


def draw_world_screen(show_map_notice: bool = True) -> None:
    game_assets.screen.fill((23, 32, 31))

    for row_index, row in enumerate(WORLD_MAP_LAYOUT):
        for col_index, cell in enumerate(row):
            tile_rect = game_state.tile_to_rect(col_index, row_index)
            tile_surface = game_assets.tile_wall_texture if cell == "#" else game_assets.tile_path_texture
            game_assets.screen.blit(tile_surface, tile_rect)
            if cell == "S":
                start_overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                start_overlay.fill((*START_COLOR, 58))
                game_assets.screen.blit(start_overlay, tile_rect)

    for drop in game_state.collectible_drops:
        if drop.collected:
            continue
        center_x, center_y = drop.world_pos
        circle_color = (155, 218, 159) if drop.category == "healing" else (238, 226, 157)
        pygame.draw.circle(game_assets.screen, circle_color, (center_x, center_y), TILE_SIZE // 2 - 12)
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
    player_sprite = game_state.get_player_map_sprite()
    player_rect = player_sprite.get_rect(center=player_center)
    game_assets.screen.blit(player_sprite, player_rect)

    hud = pygame.Surface((SCREEN_WIDTH, 48))
    hud.fill(HUD_BG)
    game_assets.screen.blit(hud, (0, 0))
    draw_health_bar(game_assets.screen, 16, 14)
    draw_book_hud_button()
    if show_map_notice:
        draw_map_notice()


def draw_encounter_screen(show_map_notice: bool = True) -> None:
    villain = game_state.get_active_villain()
    if villain is None:
        return

    draw_world_screen(show_map_notice)
    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    game_assets.screen.blit(overlay, (0, 0))

    crime = villain.crime
    enemy_image = game_assets.dossier_enemy_images[villain.id]

    encounter_panel = pygame.Rect(330, 142, 620, 390)
    draw_panel(encounter_panel, (18, 24, 28, 220))

    draw_text(
        crime["enemy_name"],
        game_assets.title_font,
        WHITE,
        game_assets.screen,
        encounter_panel.centerx,
        encounter_panel.y + 54,
        center=True,
    )
    image_rect = enemy_image.get_rect(center=(encounter_panel.centerx, encounter_panel.y + 190))
    game_assets.screen.blit(enemy_image, image_rect)

    fight_hovered = ENCOUNTER_FIGHT_RECT.collidepoint(game_assets.get_virtual_mouse_pos())
    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, ENCOUNTER_FIGHT_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, ENCOUNTER_FIGHT_RECT, 2, border_radius=8)
    draw_text(
        "Lutar",
        game_assets.help_font,
        TEXT_DARK,
        game_assets.screen,
        ENCOUNTER_FIGHT_RECT.centerx,
        ENCOUNTER_FIGHT_RECT.centery - 1,
        center=True,
    )
    if fight_hovered:
        hover_overlay = pygame.Surface(ENCOUNTER_FIGHT_RECT.size, pygame.SRCALPHA)
        hover_overlay.fill((255, 255, 255, 34))
        game_assets.screen.blit(hover_overlay, ENCOUNTER_FIGHT_RECT.topleft)

    flee_hovered = ENCOUNTER_FLEE_RECT.collidepoint(game_assets.get_virtual_mouse_pos())
    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, ENCOUNTER_FLEE_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, ENCOUNTER_FLEE_RECT, 2, border_radius=8)
    draw_text(
        "Fugir",
        game_assets.help_font,
        TEXT_DARK,
        game_assets.screen,
        ENCOUNTER_FLEE_RECT.centerx,
        ENCOUNTER_FLEE_RECT.centery - 1,
        center=True,
    )
    if flee_hovered:
        hover_overlay = pygame.Surface(ENCOUNTER_FLEE_RECT.size, pygame.SRCALPHA)
        hover_overlay.fill((255, 255, 255, 34))
        game_assets.screen.blit(hover_overlay, ENCOUNTER_FLEE_RECT.topleft)
    draw_book_hud_button()


def draw_requirement_warning_screen() -> None:
    draw_world_screen()
    villain = game_state.get_warning_villain()

    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((10, 14, 18, 176))
    game_assets.screen.blit(overlay, (0, 0))

    warning_panel = pygame.Rect(230, 180, 820, 340)
    draw_panel(warning_panel, (18, 24, 28, 235))

    enemy_name = villain.crime["enemy_name"] if villain is not None else "esse inimigo"
    title = "Alerta de conhecimento"
    message = f"Voce nao tem o conhecimento necessario para enfrentar {enemy_name}."
    prompt = "Deseja prosseguir mesmo assim?"

    draw_text(
        title,
        game_assets.title_font,
        WHITE,
        game_assets.screen,
        warning_panel.centerx,
        warning_panel.y + 52,
        center=True,
    )

    draw_text_block(
        message,
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        warning_panel.x + 44,
        warning_panel.y + 126,
        warning_panel.width - 88,
        center=False,
    )
    draw_text(
        prompt,
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        warning_panel.centerx,
        warning_panel.y + 210,
        center=True,
    )

    if villain is not None:
        required_name = game_state.get_required_weapon_name_for_villain(villain)
        if required_name is not None and not game_state.can_face_villain(villain):
            draw_text(
                f"Recomendado: colete {required_name} antes da luta.",
                game_assets.help_font,
                WHITE,
                game_assets.screen,
                warning_panel.centerx,
                warning_panel.y + 244,
                center=True,
            )

    draw_proceed_image_button(
        WARNING_PROCEED_RECT,
        WARNING_PROCEED_RECT.collidepoint(game_assets.get_virtual_mouse_pos()),
    )

    draw_back_image_button(WARNING_BACK_RECT, WARNING_BACK_RECT.collidepoint(game_assets.get_virtual_mouse_pos()))

    draw_text(
        "ENTER: prosseguir | ESC: voltar",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        warning_panel.centerx,
        warning_panel.bottom - 26,
        center=True,
    )


def draw_enemy_health_bar(surface: pygame.Surface, villain: Villain, x: int, y: int, width: int = 320) -> None:
    bar_rect = pygame.Rect(x, y, width, 18)
    pygame.draw.rect(surface, RED, bar_rect, border_radius=4)
    if villain.health > 0:
        current_width = int(width * (villain.health / villain.max_health))
        pygame.draw.rect(surface, GREEN, (bar_rect.x, bar_rect.y, current_width, bar_rect.height), border_radius=4)
    draw_text(
        f"{villain.health}/{villain.max_health}",
        game_assets.help_font,
        WHITE,
        surface,
        bar_rect.right - 52,
        bar_rect.y - 19,
    )


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

    # Side-by-side duel staging: player lower-left, enemy upper-right.
    enemy_pos = (int(SCREEN_WIDTH * 0.66), int(SCREEN_HEIGHT * 0.38))
    player_pos = (int(SCREEN_WIDTH * 0.38), int(SCREEN_HEIGHT * 0.55))

    enemy_image = game_assets.combat_enemy_images[villain.id]
    enemy_rect = enemy_image.get_rect(center=enemy_pos)
    game_assets.screen.blit(enemy_image, enemy_rect)

    player_rect = game_assets.player_image_combat.get_rect(center=player_pos)
    game_assets.screen.blit(game_assets.player_image_combat, player_rect)

    # Enemy name at top center
    draw_text(
        villain.crime["enemy_name"],
        game_assets.title_font,
        BATTLE_TEXT,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        46,
        center=True,
    )

    # Health bars
    draw_health_bar(game_assets.screen, 110, 52)
    enemy_bar_width = 300
    enemy_bar_x = enemy_rect.centerx - enemy_bar_width // 2
    enemy_bar_y = max(72, enemy_rect.top - 32)
    draw_enemy_health_bar(game_assets.screen, villain, enemy_bar_x, enemy_bar_y, enemy_bar_width)

    if game_state.selected_attack_category is None:
        draw_attack_categories()
    else:
        draw_attack_options()

    draw_battle_flee_hud_button()
    draw_book_hud_button()

    if game_state.feedback_active:
        draw_feedback_overlay()


def get_book_page_areas(book_rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
    margin_x = 78
    margin_top = 90
    margin_bottom = 92
    center_spacing = 0

    page_width = (book_rect.width - margin_x * 2 - center_spacing) // 2
    page_height = book_rect.height - margin_top - margin_bottom

    left_page = pygame.Rect(
        book_rect.x + margin_x,
        book_rect.y + margin_top,
        page_width,
        page_height,
    )
    right_page = pygame.Rect(
        left_page.right + center_spacing,
        book_rect.y + margin_top,
        page_width,
        page_height,
    )
    return left_page, right_page


def draw_book_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    x: int,
    y: int,
    centered: bool = False,
) -> pygame.Rect:
    image = font.render(text, True, color)
    rect = image.get_rect()
    if centered:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(image, rect)
    return rect


def draw_book_value(text: str, font: pygame.font.Font, color: tuple[int, int, int], rect: pygame.Rect) -> int:
    return draw_text_block(
        text,
        font,
        color,
        game_assets.screen,
        rect.x,
        rect.y,
        rect.width,
        center=False,
        line_gap=4,
    )


def draw_enemy_book_page(enemy_key: str, table: dict, area: pygame.Rect) -> None:
    fonts = {
        "enemy": game_assets.description_font,
        "label": game_assets.book_content_font,
        "item": game_assets.book_content_font,
    }
    colors = {
        "text": TEXT_DARK,
        "hint": (34, 116, 60),
        "focus": (74, 82, 99),
        "caution": (138, 54, 45),
    }

    title_y = area.y + 18
    draw_book_text(
        game_assets.screen,
        ENEMY_BOOK_NAMES.get(enemy_key, enemy_key),
        fonts["enemy"],
        colors["text"],
        area.centerx,
        title_y,
        centered=True,
    )

    block_width = 220 if area.centerx < SCREEN_WIDTH // 2 else 240
    block_start_x = area.centerx - (block_width // 2)
    label_x = block_start_x
    item_offset = 70 if area.centerx < SCREEN_WIDTH // 2 else 76
    item_x = block_start_x + item_offset
    item_width = block_width - item_offset
    line_y = area.y + 74
    row_gap = 18
    hints = THREAT_STRATEGY_HINTS.get(
        enemy_key,
        (
            "Observe o comportamento da ameaca antes de agir.",
            "Procure a camada de defesa mais ligada ao risco.",
            "Evite respostas que tratem apenas sintomas.",
        ),
    )

    rows = [
        ("Pista", hints[0], colors["hint"]),
        ("Foco", hints[1], colors["focus"]),
        ("Evite", hints[2], colors["caution"]),
    ]

    for label, item, label_color in rows:
        draw_book_text(game_assets.screen, label, fonts["label"], label_color, label_x, line_y)
        item_rect = pygame.Rect(item_x, line_y, item_width, 62)
        item_bottom = draw_book_value(item, fonts["item"], colors["text"], item_rect)
        label_bottom = line_y + fonts["label"].get_height()
        line_y = max(label_bottom, item_bottom) + row_gap


def get_book_entries_for_current_page() -> list[tuple[str, dict]]:
    return game_state.get_current_book_entries()


def draw_book_intro_page(left_page: pygame.Rect, right_page: pygame.Rect) -> None:
    left_text_x = left_page.x + 42
    right_text_x = right_page.x + 46

    draw_book_text(
        game_assets.screen,
        "O guia acorda",
        game_assets.description_font,
        TEXT_DARK,
        left_page.centerx,
        left_page.y + 38,
        centered=True,
    )
    draw_text_block(
        "Voce encontrou um livro especial: ele guarda pistas para enfrentar as ameacas digitais.",
        game_assets.book_content_font,
        TEXT_DARK,
        game_assets.screen,
        left_text_x,
        left_page.y + 92,
        left_page.width - 82,
        center=False,
        line_gap=7,
    )
    draw_text_block(
        "Cada pagina funciona como uma bussola. Leia com calma, compare os sinais e escolha melhor.",
        game_assets.book_content_font,
        TEXT_DARK,
        game_assets.screen,
        left_text_x,
        left_page.y + 212,
        left_page.width - 82,
        center=False,
        line_gap=7,
    )
    draw_book_text(
        game_assets.screen,
        "Nas margens",
        game_assets.description_font,
        TEXT_DARK,
        right_page.centerx,
        right_page.y + 38,
        centered=True,
    )
    draw_text_block(
        "O guia mostra tres sinais: uma pista, um foco e um cuidado que voce deve evitar.",
        game_assets.book_content_font,
        TEXT_DARK,
        game_assets.screen,
        right_text_x,
        right_page.y + 92,
        right_page.width - 92,
        center=False,
        line_gap=7,
    )
    draw_text_block(
        "Quando a duvida aparecer, abra o livro. Ele nao luta por voce, mas ilumina o caminho.",
        game_assets.book_content_font,
        TEXT_DARK,
        game_assets.screen,
        right_text_x,
        right_page.y + 250,
        right_page.width - 92,
        center=False,
        line_gap=7,
    )


def draw_book_button(rect: pygame.Rect, label: str, enabled: bool = True) -> None:
    if label == "Fechar":
        draw_back_image_button(rect, rect.collidepoint(game_assets.get_virtual_mouse_pos()))
        return
    fill = BUTTON_COLOR if enabled else (185, 181, 165)
    text_color = TEXT_DARK if enabled else (100, 96, 88)
    pygame.draw.rect(game_assets.screen, fill, rect, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, rect, 2, border_radius=8)
    draw_text(label, game_assets.help_font, text_color, game_assets.screen, rect.centerx, rect.centery - 2, center=True)


def draw_book_background() -> None:
    if game_state.last_game_state == "battle":
        draw_battle_screen()
    elif game_state.last_game_state == "encounter":
        draw_encounter_screen(show_map_notice=False)
    else:
        draw_world_screen(show_map_notice=False)


def draw_book_screen() -> None:
    draw_book_background()
    book_rect = game_assets.book_open_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    draw_book_text(
        game_assets.screen,
        "Guia Digital Magico",
        game_assets.title_font,
        WHITE,
        SCREEN_WIDTH // 2,
        36,
        centered=True,
    )
    game_assets.screen.blit(game_assets.book_open_image, book_rect)

    left_page, right_page = get_book_page_areas(book_rect)
    page_areas = [left_page, right_page]
    entries = get_book_entries_for_current_page()
    if game_state.book_page == 0:
        draw_book_intro_page(left_page, right_page)
    else:
        for index, (enemy_key, table) in enumerate(entries):
            if index >= len(page_areas):
                break
            draw_enemy_book_page(enemy_key, table, page_areas[index])

    if game_state.book_page > 0 and len(entries) < 2:
        empty_area = page_areas[len(entries)]
        draw_book_text(
            game_assets.screen,
            "Fim do guia",
            game_assets.description_font,
            TEXT_DARK,
            empty_area.centerx,
            empty_area.y + 120,
            centered=True,
        )
        draw_book_value(
            "Volte quando quiser para consultar as melhores defesas.",
            game_assets.book_content_font,
            TEXT_DARK,
            pygame.Rect(empty_area.x + 20, empty_area.y + 170, empty_area.width - 40, 90),
        )

    page_count = game_state.get_book_page_count()
    page_label = f"{game_state.book_page + 1}/{page_count}"
    page_counter_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, BOOK_CLOSE_RECT.bottom + 10, 140, 36)
    draw_panel(page_counter_rect, (18, 24, 28, 225))
    draw_book_text(
        game_assets.screen,
        page_label,
        game_assets.help_font,
        WHITE,
        page_counter_rect.centerx,
        page_counter_rect.centery - 1,
        centered=True,
    )

    draw_book_button(BOOK_PREV_RECT, "Anterior", game_state.book_page > 0)
    draw_book_button(BOOK_NEXT_RECT, "Proxima", game_state.book_page < page_count - 1)
    draw_book_button(BOOK_CLOSE_RECT, "Fechar")


def draw_conclusion_screen() -> None:
    game_assets.screen.blit(game_assets.settings_background, (0, 0))
    conclusion_panel = pygame.Rect(160, 96, 960, 536)
    draw_panel(conclusion_panel)
    draw_text("Guia completo", game_assets.title_font, GREEN, game_assets.screen, conclusion_panel.centerx, 146, center=True)
    draw_text_block(
        CONCLUSION_TEXT,
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        conclusion_panel.x + 60,
        conclusion_panel.y + 182,
        conclusion_panel.width - 120,
        center=False,
    )
    draw_text(
        "ENTER ou clique para continuar",
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
        draw_cyber_button(VICTORY_MENU_RECT, "Menu")
        draw_cyber_button(VICTORY_QUIT_RECT, "Sair")
        return
    elif game_state.game_state == "game_over":
        game_assets.screen.blit(game_assets.derrota_image, (0, 0))
        draw_cyber_button(
            DEFEAT_MENU_RECT,
            "Menu",
            DEFEAT_BUTTON_COLOR,
            DEFEAT_BUTTON_BORDER,
            DEFEAT_TEXT,
            (255, 36, 96, 34),
        )
        draw_cyber_button(
            DEFEAT_QUIT_RECT,
            "Sair",
            DEFEAT_BUTTON_COLOR,
            DEFEAT_BUTTON_BORDER,
            DEFEAT_TEXT,
            (255, 36, 96, 34),
        )
        return

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


def draw_pause_screen() -> None:
    # 1. Semi-transparent dark overlay
    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    game_assets.screen.blit(overlay, (0, 0))

    # 2. Draw pause panel
    draw_panel(PAUSE_PANEL_RECT)

    # 3. Draw Title: "Jogo Pausado"
    draw_text(
        "Jogo Pausado",
        game_assets.title_font,
        WHITE,
        game_assets.screen,
        PAUSE_PANEL_RECT.centerx,
        PAUSE_PANEL_RECT.y + 40,
        center=True,
    )

    # 4. Draw buttons: Continuar, Configuracoes, Voltar ao Menu
    mouse_pos = game_assets.get_virtual_mouse_pos()

    for rect, text in (
        (PAUSE_CONTINUE_RECT, "Continuar"),
        (PAUSE_SETTINGS_RECT, "Configuracoes"),
        (PAUSE_MENU_RECT, "Voltar ao Menu"),
        (PAUSE_QUIT_RECT, "Sair do Jogo"),
    ):
        hovered = rect.collidepoint(mouse_pos)
        pygame.draw.rect(game_assets.screen, BUTTON_COLOR, rect, border_radius=8)
        pygame.draw.rect(game_assets.screen, BUTTON_BORDER, rect, 2, border_radius=8)
        draw_text(
            text,
            game_assets.help_font,
            TEXT_DARK,
            game_assets.screen,
            rect.centerx,
            rect.centery - 1,
            center=True,
        )
        if hovered:
            hover_overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            hover_overlay.fill((255, 255, 255, 34))
            game_assets.screen.blit(hover_overlay, rect.topleft)
