import os
from typing import List, Optional, Tuple

import pygame

from game_config import (
    ASSETS_PATH,
    MAIN_16_9_RESOLUTIONS,
    SCREEN_HEIGHT,
    SCREEN_SIZE,
    SCREEN_WIDTH,
    TILE_SIZE,
    WINDOW_TITLE,
)

pygame.init()

pygame.display.set_caption(WINDOW_TITLE)


def sanitize_resolution(resolution: Tuple[int, int]) -> Tuple[int, int]:
    width = max(1, int(resolution[0]))
    height = max(1, int(resolution[1]))
    return width, height


def get_monitor_resolution() -> Tuple[int, int]:
    display_info = pygame.display.Info()
    if display_info.current_w <= 0 or display_info.current_h <= 0:
        return SCREEN_SIZE
    return display_info.current_w, display_info.current_h


def build_resolution_options(monitor_resolution: Tuple[int, int]) -> List[Tuple[int, int]]:
    valid_options: List[Tuple[int, int]] = []
    monitor_w, monitor_h = monitor_resolution
    for width, height in MAIN_16_9_RESOLUTIONS:
        if width <= monitor_w and height <= monitor_h:
            valid_options.append((width, height))

    if not valid_options:
        valid_options.append(SCREEN_SIZE)
    if SCREEN_SIZE not in valid_options:
        valid_options.append(SCREEN_SIZE)
    valid_options.sort(key=lambda size: size[0] * size[1])
    return valid_options


monitor_resolution = get_monitor_resolution()
resolution_options = build_resolution_options(monitor_resolution)
current_resolution = monitor_resolution
fullscreen = True

_display_surface = pygame.display.set_mode(current_resolution, pygame.FULLSCREEN)
screen = pygame.Surface(SCREEN_SIZE).convert()
_render_size = SCREEN_SIZE
_render_offset = (0, 0)


def _recalculate_render_target() -> None:
    global _render_size, _render_offset
    scale_x = current_resolution[0] / SCREEN_WIDTH
    scale_y = current_resolution[1] / SCREEN_HEIGHT
    scale = min(scale_x, scale_y)
    target_width = max(1, int(SCREEN_WIDTH * scale))
    target_height = max(1, int(SCREEN_HEIGHT * scale))
    offset_x = (current_resolution[0] - target_width) // 2
    offset_y = (current_resolution[1] - target_height) // 2
    _render_size = (target_width, target_height)
    _render_offset = (offset_x, offset_y)


_recalculate_render_target()


def set_display_mode(
    resolution: Optional[Tuple[int, int]] = None,
    force_fullscreen: Optional[bool] = None,
) -> None:
    global _display_surface, current_resolution, fullscreen
    previous_resolution = current_resolution
    previous_fullscreen = fullscreen
    if resolution is not None:
        current_resolution = sanitize_resolution(resolution)
    if force_fullscreen is not None:
        fullscreen = force_fullscreen

    flags = pygame.FULLSCREEN if fullscreen else 0
    try:
        _display_surface = pygame.display.set_mode(current_resolution, flags)
    except pygame.error:
        current_resolution = previous_resolution
        fullscreen = previous_fullscreen
        fallback_flags = pygame.FULLSCREEN if fullscreen else 0
        _display_surface = pygame.display.set_mode(current_resolution, fallback_flags)
    current_resolution = _display_surface.get_size()
    _recalculate_render_target()


def set_resolution(resolution: Tuple[int, int]) -> None:
    set_display_mode(resolution=resolution)


def toggle_fullscreen() -> None:
    set_display_mode(force_fullscreen=not fullscreen)


def get_current_resolution_index() -> int:
    if current_resolution in resolution_options:
        return resolution_options.index(current_resolution)
    return -1


def window_to_game_pos(window_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    if _render_size[0] <= 0 or _render_size[1] <= 0:
        return window_pos
    local_x = window_pos[0] - _render_offset[0]
    local_y = window_pos[1] - _render_offset[1]
    if local_x < 0 or local_y < 0 or local_x >= _render_size[0] or local_y >= _render_size[1]:
        return None
    scale_x = SCREEN_WIDTH / _render_size[0]
    scale_y = SCREEN_HEIGHT / _render_size[1]
    game_x = int(local_x * scale_x)
    game_y = int(local_y * scale_y)
    clamped_x = max(0, min(SCREEN_WIDTH - 1, game_x))
    clamped_y = max(0, min(SCREEN_HEIGHT - 1, game_y))
    return clamped_x, clamped_y


def get_virtual_mouse_pos() -> Tuple[int, int]:
    mouse_pos = window_to_game_pos(pygame.mouse.get_pos())
    if mouse_pos is None:
        return -1, -1
    return mouse_pos


def present() -> None:
    if _render_size == SCREEN_SIZE and _render_offset == (0, 0):
        _display_surface.blit(screen, (0, 0))
    else:
        scaled_surface = pygame.transform.smoothscale(screen, _render_size)
        _display_surface.fill((0, 0, 0))
        _display_surface.blit(scaled_surface, _render_offset)
    pygame.display.flip()


def load_font(filename: str, size: int) -> pygame.font.Font:
    path = os.path.join(ASSETS_PATH, filename)
    if os.path.exists(path):
        return pygame.font.Font(path, size)
    return pygame.font.Font(None, size + 8)


title_font = load_font("Minecraftia-Regular.ttf", 28)
menu_font = load_font("Minecraftia-Regular.ttf", 34)
option_font = load_font("Minecraftia-Regular.ttf", 12)
feedback_font = load_font("Minecraftia-Regular.ttf", 24)
description_font = load_font("Minecraftia-Regular.ttf", 17)
story_font = load_font("Minecraftia-Regular.ttf", 16)
help_font = load_font("Minecraftia-Regular.ttf", 12)
small_font = load_font("Minecraftia-Regular.ttf", 10)
book_content_font = load_font("Minecraftia-Regular.ttf", 13)

PLAYER_WALK_SHEET_FILENAME = "personagem_walk.png"
PLAYER_WALK_SHEET_COLUMNS = 4
PLAYER_WALK_SHEET_ROWS = 2
PLAYER_MAP_TARGET_HEIGHT = TILE_SIZE - 8
MENU_BUTTONS_SHEET_FILENAME = "menu_buttons.png"
MENU_BUTTON_TARGET_WIDTH = int(SCREEN_WIDTH * 0.16)
MENU_BUTTON_VERTICAL_GAP = 12
MENU_BUTTON_BLOCK_CENTER_Y = int(SCREEN_HEIGHT * 0.60)
TILE_PATH_TEXTURE_FILENAME = "tile_path.png"
TILE_WALL_TEXTURE_FILENAME = "tile_wall.png"


def load_image(filename: str, use_alpha: bool = False) -> pygame.Surface:
    path = os.path.join(ASSETS_PATH, filename)
    try:
        image = pygame.image.load(path)
        if use_alpha:
            return image.convert_alpha()
        return image.convert()
    except (pygame.error, FileNotFoundError):
        fallback = pygame.Surface((240, 240), pygame.SRCALPHA if use_alpha else 0)
        fallback.fill((180, 60, 60, 220) if use_alpha else (180, 60, 60))
        return fallback


def scale_image_proportional_height(image: pygame.Surface, target_height: int) -> pygame.Surface:
    original_width, original_height = image.get_size()
    if original_height == 0:
        return image.copy()
    target_width = int((original_width / original_height) * target_height)
    return pygame.transform.smoothscale(image, (target_width, target_height))


def scale_image_proportional_width(image: pygame.Surface, target_width: int) -> pygame.Surface:
    original_width, original_height = image.get_size()
    if original_width == 0:
        return image.copy()
    target_height = int((original_height / original_width) * target_width)
    return pygame.transform.smoothscale(image, (target_width, target_height))


def extract_sprite_sheet_frames(sprite_sheet: pygame.Surface, columns: int, rows: int) -> List[pygame.Surface]:
    if columns <= 0 or rows <= 0:
        return []
    frame_width = sprite_sheet.get_width() // columns
    frame_height = sprite_sheet.get_height() // rows
    if frame_width <= 0 or frame_height <= 0:
        return []

    frames: List[pygame.Surface] = []
    for row_index in range(rows):
        for col_index in range(columns):
            source_rect = pygame.Rect(
                col_index * frame_width,
                row_index * frame_height,
                frame_width,
                frame_height,
            )
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), source_rect)
            frames.append(frame)
    return align_frames_to_baseline(frames)


def align_frames_to_baseline(frames: List[pygame.Surface], min_alpha: int = 8) -> List[pygame.Surface]:
    if not frames:
        return []

    frame_bottoms: List[int] = []
    frame_centers_x: List[int] = []
    frame_width = frames[0].get_width()
    target_center_x = frame_width // 2
    for frame in frames:
        bounds = frame.get_bounding_rect(min_alpha=min_alpha)
        if bounds.width == 0 or bounds.height == 0:
            frame_bottoms.append(frame.get_height() - 1)
            frame_centers_x.append(target_center_x)
            continue
        frame_bottoms.append(bounds.bottom - 1)
        frame_centers_x.append(bounds.centerx)

    target_bottom = max(frame_bottoms)
    aligned_frames: List[pygame.Surface] = []
    for frame, bottom, center_x in zip(frames, frame_bottoms, frame_centers_x):
        x_offset = target_center_x - center_x
        y_offset = target_bottom - bottom
        if x_offset == 0 and y_offset == 0:
            aligned_frames.append(frame)
            continue
        shifted = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
        shifted.blit(frame, (x_offset, y_offset))
        aligned_frames.append(shifted)

    return aligned_frames


def extract_vertical_button_images(button_sheet: pygame.Surface, rows: int = 2) -> List[pygame.Surface]:
    if rows <= 0:
        return []
    segment_height = button_sheet.get_height() // rows
    if segment_height <= 0:
        return []

    buttons: List[pygame.Surface] = []
    for row_index in range(rows):
        segment_rect = pygame.Rect(0, row_index * segment_height, button_sheet.get_width(), segment_height)
        segment = button_sheet.subsurface(segment_rect).copy()
        bounds = segment.get_bounding_rect(min_alpha=8)
        if bounds.width == 0 or bounds.height == 0:
            continue
        buttons.append(segment.subsurface(bounds).copy())
    return buttons


def create_menu_button_fallback(label: str) -> pygame.Surface:
    button_height = int(MENU_BUTTON_TARGET_WIDTH * 0.32)
    button = pygame.Surface((MENU_BUTTON_TARGET_WIDTH, button_height), pygame.SRCALPHA)
    pygame.draw.rect(button, (18, 52, 60, 240), button.get_rect(), border_radius=18)
    pygame.draw.rect(button, (95, 230, 235), button.get_rect(), 3, border_radius=18)
    text_image = title_font.render(label, True, (174, 255, 255))
    text_rect = text_image.get_rect(center=button.get_rect().center)
    button.blit(text_image, text_rect)
    return button


def create_tile_surface_from_texture(filename: str, fallback_color: Tuple[int, int, int]) -> pygame.Surface:
    texture_path = os.path.join(ASSETS_PATH, filename)
    if os.path.exists(texture_path):
        source = load_image(filename)
        return pygame.transform.scale(source, (TILE_SIZE, TILE_SIZE))

    fallback = pygame.Surface((TILE_SIZE, TILE_SIZE))
    fallback.fill(fallback_color)
    return fallback


def create_healing_icon(size: int) -> pygame.Surface:
    icon = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    radius = max(8, size // 2 - 2)
    pygame.draw.circle(icon, (82, 166, 94), (center, center), radius)
    plus_thickness = max(4, size // 7)
    plus_width = max(10, size // 2)
    pygame.draw.rect(
        icon,
        (243, 248, 243),
        pygame.Rect(center - plus_width // 2, center - plus_thickness // 2, plus_width, plus_thickness),
        border_radius=2,
    )
    pygame.draw.rect(
        icon,
        (243, 248, 243),
        pygame.Rect(center - plus_thickness // 2, center - plus_width // 2, plus_thickness, plus_width),
        border_radius=2,
    )
    return icon


back_button_source = load_image("back_button.png", use_alpha=True)
_back_button_cache: dict[Tuple[int, int], pygame.Surface] = {}


def get_back_button_image(target_size: Tuple[int, int]) -> pygame.Surface:
    width, height = max(1, target_size[0]), max(1, target_size[1])
    cache_key = (width, height)
    cached = _back_button_cache.get(cache_key)
    if cached is not None:
        return cached
    scaled = pygame.transform.smoothscale(back_button_source, cache_key)
    _back_button_cache[cache_key] = scaled
    return scaled


proceed_button_source = load_image("prosseguir.png", use_alpha=True)
_proceed_button_cache: dict[Tuple[int, int], pygame.Surface] = {}


def get_proceed_button_image(target_size: Tuple[int, int]) -> pygame.Surface:
    width, height = max(1, target_size[0]), max(1, target_size[1])
    cache_key = (width, height)
    cached = _proceed_button_cache.get(cache_key)
    if cached is not None:
        return cached
    scaled = pygame.transform.smoothscale(proceed_button_source, cache_key)
    _proceed_button_cache[cache_key] = scaled
    return scaled


combat_back_arrow_source = load_image("flecha.png", use_alpha=True)
_combat_back_arrow_cache: dict[Tuple[int, int], pygame.Surface] = {}


def get_combat_back_arrow_image(target_size: Tuple[int, int]) -> pygame.Surface:
    width, height = max(1, target_size[0]), max(1, target_size[1])
    cache_key = (width, height)
    cached = _combat_back_arrow_cache.get(cache_key)
    if cached is not None:
        return cached
    scaled = pygame.transform.smoothscale(combat_back_arrow_source, cache_key)
    _combat_back_arrow_cache[cache_key] = scaled
    return scaled


combate_bg = pygame.transform.scale(load_image("combate.png"), SCREEN_SIZE)
menu_image = pygame.transform.scale(load_image("menu.png"), SCREEN_SIZE)
settings_background = pygame.transform.scale(load_image("settings_background.png"), SCREEN_SIZE)
tile_path_texture = create_tile_surface_from_texture(TILE_PATH_TEXTURE_FILENAME, (140, 179, 119))
tile_wall_texture = create_tile_surface_from_texture(TILE_WALL_TEXTURE_FILENAME, (57, 74, 64))
menu_play_button_image = create_menu_button_fallback("Jogar")
menu_settings_button_image = create_menu_button_fallback("Configuracoes")
menu_buttons_sheet_path = os.path.join(ASSETS_PATH, MENU_BUTTONS_SHEET_FILENAME)
if os.path.exists(menu_buttons_sheet_path):
    menu_buttons_sheet = load_image(MENU_BUTTONS_SHEET_FILENAME, use_alpha=True)
    extracted_buttons = extract_vertical_button_images(menu_buttons_sheet, rows=2)
    if len(extracted_buttons) >= 2:
        menu_play_button_image = scale_image_proportional_width(extracted_buttons[0], MENU_BUTTON_TARGET_WIDTH)
        menu_settings_button_image = scale_image_proportional_width(extracted_buttons[1], MENU_BUTTON_TARGET_WIDTH)

menu_buttons_total_height = (
    menu_play_button_image.get_height() + MENU_BUTTON_VERTICAL_GAP + menu_settings_button_image.get_height()
)
menu_buttons_top = MENU_BUTTON_BLOCK_CENTER_Y - (menu_buttons_total_height // 2)
menu_play_button_rect = menu_play_button_image.get_rect(midtop=(SCREEN_WIDTH // 2, menu_buttons_top))
menu_settings_button_rect = menu_settings_button_image.get_rect(
    midtop=(SCREEN_WIDTH // 2, menu_play_button_rect.bottom + MENU_BUTTON_VERTICAL_GAP)
)

vitoria_image = pygame.transform.scale(load_image("vitoria.png"), SCREEN_SIZE)
derrota_image = pygame.transform.scale(load_image("derrota.png"), SCREEN_SIZE)
historia_bg = pygame.transform.scale(load_image("historia.png"), SCREEN_SIZE)

player_source = load_image("personagem.png", use_alpha=True)
player_image_combat = scale_image_proportional_height(player_source, int(SCREEN_HEIGHT * 0.30))
player_image_portrait = scale_image_proportional_height(player_source, int(SCREEN_HEIGHT * 0.60))
player_image_map = scale_image_proportional_height(player_source, PLAYER_MAP_TARGET_HEIGHT)

player_walk_frames: List[pygame.Surface] = []
walk_sheet_path = os.path.join(ASSETS_PATH, PLAYER_WALK_SHEET_FILENAME)
if os.path.exists(walk_sheet_path):
    walk_sheet = load_image(PLAYER_WALK_SHEET_FILENAME, use_alpha=True)
    player_walk_frames = [
        scale_image_proportional_height(frame, PLAYER_MAP_TARGET_HEIGHT)
        for frame in extract_sprite_sheet_frames(
            walk_sheet,
            PLAYER_WALK_SHEET_COLUMNS,
            PLAYER_WALK_SHEET_ROWS,
        )
    ]
if not player_walk_frames:
    player_walk_frames = [player_image_map]
player_walk_frames_flipped = [pygame.transform.flip(frame, True, False) for frame in player_walk_frames]

collectible_filenames = {
    "book": "livro.png",
    "verificacao": "icone_verificacao.png",
    "protecao": "icone_protecao.png",
    "privacidade": "icone_privacidade.png",
    "acao": "icone_acao.png",
}

collectible_images = {
    key: scale_image_proportional_height(load_image(filename, use_alpha=True), TILE_SIZE - 22)
    for key, filename in collectible_filenames.items()
}
collectible_images["book"] = scale_image_proportional_height(load_image(collectible_filenames["book"], use_alpha=True), TILE_SIZE - 28)
collectible_images["cura"] = create_healing_icon(TILE_SIZE - 22)

book_open_image = pygame.transform.scale(load_image("livro_aberto.png", use_alpha=True), (900, 600))

enemy_filenames = [
    "phishing.png",
    "malware.png",
    "senha.png",
    "ransomware.png",
    "spyware.png",
    "adware.png",
    "golpe.png",
    "cyberstalking.png",
    "pirataria.png",
    "deepfake.png",
]

dossier_enemy_images: List[pygame.Surface] = []
combat_enemy_images: List[pygame.Surface] = []
map_enemy_images: List[pygame.Surface] = []

for filename in enemy_filenames:
    image = load_image(filename, use_alpha=True)
    dossier_enemy_images.append(scale_image_proportional_height(image, int(SCREEN_HEIGHT * 0.20)))
    combat_enemy_images.append(scale_image_proportional_height(image, int(SCREEN_HEIGHT * 0.35)))
    map_enemy_images.append(scale_image_proportional_height(image, TILE_SIZE - 16))
