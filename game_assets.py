import os
from typing import List

import pygame

from game_config import ASSETS_PATH, SCREEN_HEIGHT, SCREEN_SIZE, TILE_SIZE, WINDOW_TITLE

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


combate_bg = pygame.transform.scale(load_image("combate.png"), SCREEN_SIZE)
menu_image = pygame.transform.scale(load_image("menu.png"), SCREEN_SIZE)
vitoria_image = pygame.transform.scale(load_image("vitoria.png"), SCREEN_SIZE)
derrota_image = pygame.transform.scale(load_image("derrota.png"), SCREEN_SIZE)
introducao_bg = pygame.transform.scale(load_image("introducao.png"), SCREEN_SIZE)
historia_bg = pygame.transform.scale(load_image("historia.png"), SCREEN_SIZE)
conclusao_bg = pygame.transform.scale(load_image("conclusao.png"), SCREEN_SIZE)

player_source = load_image("personagem.png", use_alpha=True)
player_image_combat = scale_image_proportional_height(player_source, int(SCREEN_HEIGHT * 0.30))
player_image_portrait = scale_image_proportional_height(player_source, int(SCREEN_HEIGHT * 0.60))
player_image_map = scale_image_proportional_height(player_source, TILE_SIZE - 12)

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
