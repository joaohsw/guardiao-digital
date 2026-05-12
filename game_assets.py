import os
from typing import List

import pygame

from game_config import ASSETS_PATH, SCREEN_HEIGHT, SCREEN_SIZE, SCREEN_WIDTH, TILE_SIZE, WINDOW_TITLE

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_TITLE)
fullscreen = False


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
book_content_font = load_font("Minecraftia-Regular.ttf", 14)

PLAYER_WALK_SHEET_FILENAME = "personagem_walk.png"
PLAYER_WALK_SHEET_COLUMNS = 4
PLAYER_WALK_SHEET_ROWS = 2
PLAYER_MAP_TARGET_HEIGHT = TILE_SIZE - 8
MENU_BUTTONS_SHEET_FILENAME = "menu_buttons.png"
MENU_BUTTON_TARGET_WIDTH = int(SCREEN_WIDTH * 0.16)
MENU_BUTTON_VERTICAL_GAP = 12
MENU_BUTTON_BLOCK_CENTER_Y = int(SCREEN_HEIGHT * 0.60)


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


combate_bg = pygame.transform.scale(load_image("combate.png"), SCREEN_SIZE)
menu_image = pygame.transform.scale(load_image("menu.png"), SCREEN_SIZE)

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
introducao_bg = pygame.transform.scale(load_image("introducao.png"), SCREEN_SIZE)
historia_bg = pygame.transform.scale(load_image("historia.png"), SCREEN_SIZE)
conclusao_bg = pygame.transform.scale(load_image("conclusao.png"), SCREEN_SIZE)

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
