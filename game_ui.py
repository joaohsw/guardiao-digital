from typing import List, Tuple

import pygame

import game_assets
from game_config import PANEL_BG, PANEL_BORDER


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    lines: List[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if not paragraph:
            lines.append("")
    return lines


def draw_text(
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    surface: pygame.Surface,
    x: int,
    y: int,
    center: bool = False,
) -> None:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)


def draw_panel(rect: pygame.Rect, fill_color: Tuple[int, int, int, int] = PANEL_BG) -> None:
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, fill_color, panel.get_rect(), border_radius=14)
    pygame.draw.rect(panel, PANEL_BORDER, panel.get_rect(), 2, border_radius=14)
    game_assets.screen.blit(panel, rect.topleft)


def draw_text_block(
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    surface: pygame.Surface,
    x: int,
    y: int,
    max_width: int,
    center: bool = False,
    line_gap: int = 4,
) -> int:
    lines = wrap_text(text, font, max_width)
    total_height = len(lines) * font.get_height() + max(0, len(lines) - 1) * line_gap
    draw_y = y - (total_height // 2) if center else y

    for line in lines:
        rendered = font.render(line, True, color)
        rect = rendered.get_rect()
        if center:
            rect.center = (x, draw_y + font.get_height() // 2)
        else:
            rect.topleft = (x, draw_y)
        surface.blit(rendered, rect)
        draw_y += font.get_height() + line_gap
    return draw_y
