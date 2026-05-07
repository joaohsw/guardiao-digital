import pygame

import game_assets
import game_state
from game_config import (
    ATTACK_CATEGORIES,
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
    SUBATTACK_OPTION_RECTS,
    TEXT_DARK,
    TILE_SIZE,
    WARNING_BACK_RECT,
    WARNING_PROCEED_RECT,
    WALL_COLOR,
    WALL_COLOR_ALT,
    WHITE,
    WORLD_MAP_LAYOUT,
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


def draw_book_hud_button() -> None:
    if not game_state.book_collected:
        return
    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, BOOK_HUD_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, BOOK_HUD_RECT, 2, border_radius=8)
    icon = game_assets.collectible_images["book"]
    icon_rect = icon.get_rect(center=BOOK_HUD_RECT.center)
    game_assets.screen.blit(icon, icon_rect)


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
        "Colete drops para liberar viloes especificos | WASD/Setas para explorar",
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        17,
        center=True,
    )
    draw_text("F11: tela cheia", game_assets.help_font, WHITE, game_assets.screen, SCREEN_WIDTH - 180, 11)
    draw_book_hud_button()
    draw_map_notice()


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
    draw_book_hud_button()


def draw_requirement_warning_screen() -> None:
    draw_world_screen()
    villain = game_state.get_warning_villain()

    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((10, 14, 18, 176))
    game_assets.screen.blit(overlay, (0, 0))

    warning_panel = pygame.Rect(230, 180, 820, 340)
    draw_panel(warning_panel, (18, 24, 28, 235))

    draw_text(
        "Alerta de conhecimento",
        game_assets.title_font,
        WHITE,
        game_assets.screen,
        warning_panel.centerx,
        warning_panel.y + 52,
        center=True,
    )

    enemy_name = villain.crime["enemy_name"] if villain is not None else "esse inimigo"
    draw_text_block(
        f"Voce nao tem o conhecimento necessario para enfrentar {enemy_name}.",
        game_assets.description_font,
        WHITE,
        game_assets.screen,
        warning_panel.x + 44,
        warning_panel.y + 126,
        warning_panel.width - 88,
        center=False,
    )
    draw_text(
        "Deseja prosseguir mesmo assim?",
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

    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, WARNING_PROCEED_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, WARNING_PROCEED_RECT, 2, border_radius=8)
    draw_text(
        "Prosseguir",
        game_assets.help_font,
        TEXT_DARK,
        game_assets.screen,
        WARNING_PROCEED_RECT.centerx,
        WARNING_PROCEED_RECT.centery - 1,
        center=True,
    )

    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, WARNING_BACK_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, WARNING_BACK_RECT, 2, border_radius=8)
    draw_text(
        "Voltar",
        game_assets.help_font,
        TEXT_DARK,
        game_assets.screen,
        WARNING_BACK_RECT.centerx,
        WARNING_BACK_RECT.centery - 1,
        center=True,
    )

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

    pygame.draw.rect(game_assets.screen, BUTTON_COLOR, BATTLE_FLEE_RECT, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, BATTLE_FLEE_RECT, 2, border_radius=8)
    draw_text("Fugir", game_assets.help_font, TEXT_DARK, game_assets.screen, BATTLE_FLEE_RECT.centerx, BATTLE_FLEE_RECT.y + 9, center=True)
    draw_text(
        "Voltar ao mapa",
        game_assets.small_font,
        TEXT_DARK,
        game_assets.screen,
        BATTLE_FLEE_RECT.centerx,
        BATTLE_FLEE_RECT.y + 22,
        center=True,
    )

    if game_state.selected_attack_category is None:
        categories = game_state.get_unlocked_categories()
        for index, category in enumerate(categories):
            if index >= len(BATTLE_OPTION_RECTS):
                break
            option_rect = BATTLE_OPTION_RECTS[index]
            pygame.draw.rect(game_assets.screen, BUTTON_COLOR, option_rect, border_radius=8)
            pygame.draw.rect(game_assets.screen, BUTTON_BORDER, option_rect, 2, border_radius=8)
            category_data = ATTACK_CATEGORIES[category]
            icon = game_assets.collectible_images[category_data["asset_key"]]
            icon_rect = icon.get_rect(center=(option_rect.x + 48, option_rect.centery))
            game_assets.screen.blit(icon, icon_rect)
            draw_text(
                f"{index + 1}. {category_data['name']}",
                game_assets.description_font,
                TEXT_DARK,
                game_assets.screen,
                option_rect.x + 92,
                option_rect.y + 18,
            )
            draw_text(
                "Abrir ataques desta categoria",
                game_assets.help_font,
                TEXT_DARK,
                game_assets.screen,
                option_rect.x + 92,
                option_rect.y + 43,
            )
        footer = "Escolha uma categoria com clique/teclas 1-4 | ESC ou botao Fugir volta ao mapa"
    else:
        category_name = ATTACK_CATEGORIES[game_state.selected_attack_category]["name"]
        attacks = game_state.get_unlocked_attacks_for_category(game_state.selected_attack_category)
        draw_text(
            f"Categoria: {category_name}",
            game_assets.description_font,
            WHITE,
            game_assets.screen,
            SCREEN_WIDTH // 2,
            492,
            center=True,
        )
        for index, attack in enumerate(attacks):
            if index >= len(SUBATTACK_OPTION_RECTS):
                break
            option_rect = SUBATTACK_OPTION_RECTS[index]
            pygame.draw.rect(game_assets.screen, BUTTON_COLOR, option_rect, border_radius=8)
            pygame.draw.rect(game_assets.screen, BUTTON_BORDER, option_rect, 2, border_radius=8)
            effectiveness = game_state.get_attack_effectiveness(villain.enemy_key, attack["id"])
            visible_effect = f" | Efeito: {effectiveness}" if game_state.book_collected else ""
            draw_text(
                f"{index + 1}. {attack['name']}{visible_effect}",
                game_assets.help_font,
                TEXT_DARK,
                game_assets.screen,
                option_rect.x + 18,
                option_rect.y + 9,
            )
        footer = "Escolha um ataque com clique/teclas 1-5 | ESC volta para categorias"

    draw_text(
        footer,
        game_assets.help_font,
        WHITE,
        game_assets.screen,
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 14,
        center=True,
    )
    draw_book_hud_button()

    if game_state.feedback_active:
        draw_feedback_overlay()


def get_book_page_areas(book_rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
    margin_x = 78
    margin_top = 106
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


def draw_book_value(text: str, font: pygame.font.Font, color: tuple[int, int, int], rect: pygame.Rect) -> None:
    draw_text_block(
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
        "forte": (34, 116, 60),
        "medio": (74, 82, 99),
        "fraco": (138, 54, 45),
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
    line_spacing = 88

    rows = [
        ("Forte", format_book_attack_name(table["forte"]), colors["forte"]),
        ("Medio", format_book_attack_name(table["medio"]), colors["medio"]),
        ("Fraco", format_book_attack_name(table["fraco"]), colors["fraco"]),
    ]

    for label, item, label_color in rows:
        draw_book_text(game_assets.screen, label, fonts["label"], label_color, label_x, line_y)
        item_rect = pygame.Rect(item_x, line_y, item_width, 62)
        draw_book_value(item, fonts["item"], colors["text"], item_rect)
        line_y += line_spacing


def get_book_entries_for_current_page() -> list[tuple[str, dict]]:
    return game_state.get_current_book_entries()


def draw_book_button(rect: pygame.Rect, label: str, enabled: bool = True) -> None:
    fill = BUTTON_COLOR if enabled else (185, 181, 165)
    text_color = TEXT_DARK if enabled else (100, 96, 88)
    pygame.draw.rect(game_assets.screen, fill, rect, border_radius=8)
    pygame.draw.rect(game_assets.screen, BUTTON_BORDER, rect, 2, border_radius=8)
    draw_text(label, game_assets.help_font, text_color, game_assets.screen, rect.centerx, rect.centery - 2, center=True)


def draw_book_screen() -> None:
    game_assets.screen.fill((23, 32, 31))
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
    for index, (enemy_key, table) in enumerate(entries):
        if index >= len(page_areas):
            break
        draw_enemy_book_page(enemy_key, table, page_areas[index])

    if len(entries) < 2:
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
    page_label = f"Pagina {game_state.book_page + 1}/{page_count}"
    draw_book_text(
        game_assets.screen,
        page_label,
        game_assets.help_font,
        WHITE,
        SCREEN_WIDTH // 2,
        BOOK_CLOSE_RECT.y - 24,
        centered=True,
    )

    draw_book_button(BOOK_PREV_RECT, "Anterior", game_state.book_page > 0)
    draw_book_button(BOOK_NEXT_RECT, "Proxima", game_state.book_page < page_count - 1)
    draw_book_button(BOOK_CLOSE_RECT, "Fechar")


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
