import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

ASSETS_PATH = "assets"
TILE_SIZE = 64
PLAYER_SPEED = 260.0
PLAYER_HITBOX_SIZE = 26
VILLAIN_TRIGGER_PADDING = -8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (204, 57, 57)
GREEN = (56, 142, 60)
HUD_BG = (28, 34, 38, 190)
PANEL_BG = (18, 24, 28, 210)
PANEL_BORDER = (202, 214, 197)
WALL_COLOR = (57, 74, 64)
WALL_COLOR_ALT = (51, 68, 58)
PATH_COLOR = (140, 179, 119)
PATH_COLOR_ALT = (133, 172, 112)
START_COLOR = (188, 214, 142)
GRID_COLOR = (111, 138, 96)
BUTTON_COLOR = (224, 220, 202)
BUTTON_BORDER = (56, 52, 40)
TEXT_DARK = (38, 38, 38)

WORLD_MAP_LAYOUT = [
    "####################",
    "#S....#.......#....#",
    "#.##..#.#####.#.##.#",
    "#....##.....#.#....#",
    "###......##.#.###..#",
    "#...###.....#......#",
    "#.#...####.#####.#.#",
    "#.#.#....#.....#.#.#",
    "#...#.##.#####.#...#",
    "#.....#.........#..#",
    "####################",
]

VILLAIN_SPAWNS = [
    (4, 1),
    (10, 1),
    (17, 1),
    (2, 3),
    (8, 3),
    (18, 9),
    (9, 5),
    (16, 5),
    (3, 8),
    (14, 9),
]

crimes = [
    {
        "enemy_name": "Ameaca de Phishing",
        "description": "Mensagens falsas tentam roubar dados pessoais com links e anexos suspeitos.",
        "options": [
            "Clicar no link para validar a conta.",
            "Responder o e-mail e pedir confirmacao.",
            "Verificar remetente e ignorar links suspeitos.",
            "Encaminhar para outro contato testar.",
        ],
        "correct_option_index": 2,
        "explanation": "Interagir com a mensagem confirma que seu contato esta ativo para golpistas.",
        "correct_explanation": "Boa decisao. Desconfiar e validar a origem da mensagem reduz muito esse risco.",
    },
    {
        "enemy_name": "Ataque de Malware",
        "description": "Programas maliciosos podem danificar o dispositivo e roubar informacoes.",
        "options": [
            "Manter sistema e antivirus atualizados.",
            "Instalar qualquer limpador de PC anunciado.",
            "Desativar alertas do navegador.",
            "Conectar pendrive desconhecido.",
        ],
        "correct_option_index": 0,
        "explanation": "Arquivos ou programas de origem duvidosa podem infectar rapidamente a maquina.",
        "correct_explanation": "Perfeito. Atualizacoes corrigem falhas de seguranca usadas por malware.",
    },
    {
        "enemy_name": "Invasao por Senha Fraca",
        "description": "Senhas simples ou reutilizadas facilitam invasoes em varias contas.",
        "options": [
            "Usar a data de aniversario na senha.",
            "Repetir a mesma senha em todos os servicos.",
            "Salvar senhas em texto simples no computador.",
            "Criar senhas fortes e diferentes para cada servico.",
        ],
        "correct_option_index": 3,
        "explanation": "Reutilizacao de senha aumenta o impacto de qualquer vazamento.",
        "correct_explanation": "Exato. Senhas unicas e fortes sao base de uma boa protecao digital.",
    },
    {
        "enemy_name": "Sequestro por Ransomware",
        "description": "Arquivos sao criptografados e criminosos exigem pagamento para liberar acesso.",
        "options": [
            "Formatar e restaurar de backup seguro.",
            "Pagar o resgate para tentar recuperar rapido.",
            "Baixar descriptografador em site duvidoso.",
            "Negociar com o criminoso por mensagem.",
        ],
        "correct_option_index": 0,
        "explanation": "Pagar nao garante recuperacao e ainda financia o crime.",
        "correct_explanation": "Correto. Backup confiavel e a estrategia mais segura para recuperar os dados.",
    },
    {
        "enemy_name": "Espionagem por Spyware",
        "description": "Aplicativos maliciosos monitoram atividades e capturam informacoes em silencio.",
        "options": [
            "Aceitar permissoes sem analisar.",
            "Achar que modo anonimo bloqueia tudo.",
            "Usar anti-spyware e revisar permissoes de apps.",
            "Instalar app que pede acesso desnecessario.",
        ],
        "correct_option_index": 2,
        "explanation": "Permissoes excessivas podem expor dados sensiveis sem voce perceber.",
        "correct_explanation": "Boa. Controle de permissoes e ferramentas de seguranca dificultam espionagem.",
    },
    {
        "enemy_name": "Inundacao de Adware",
        "description": "Pop-ups e anuncios excessivos podem degradar desempenho e abrir portas para golpes.",
        "options": [
            "Clicar em todos os botoes de fechar pop-up.",
            "Instalar acelerador milagroso de internet.",
            "Ignorar os anuncios para sempre.",
            "Usar bloqueador e revisar instalacoes recentes.",
        ],
        "correct_option_index": 3,
        "explanation": "Programas milagrosos costumam incluir ainda mais adware.",
        "correct_explanation": "Acertou. Controle do que e instalado evita reincidencia desse tipo de ameaca.",
    },
    {
        "enemy_name": "Golpe do Estelionato Eletronico",
        "description": "Fraudes usam engenharia social para convencer vitimas a enviar dinheiro ou dados.",
        "options": [
            "Fazer PIX sem confirmar por outro canal.",
            "Usar cartao virtual em compras online.",
            "Clicar em SMS de oferta urgente.",
            "Informar senha em e-mail falso de banco.",
        ],
        "correct_option_index": 1,
        "explanation": "Contas e perfis podem ser clonados para solicitar dinheiro com urgencia.",
        "correct_explanation": "Perfeito. Cartao virtual cria uma camada extra de seguranca em compras.",
    },
    {
        "enemy_name": "Perseguicao Online (Cyberstalking)",
        "description": "Assedio digital repetitivo causa risco real e deve ser tratado com seriedade.",
        "options": [
            "Publicar localizacao em tempo real.",
            "Bloquear e denunciar o perfil agressor.",
            "Manter o perfil totalmente aberto.",
            "Responder e provocar nos comentarios.",
        ],
        "correct_option_index": 1,
        "explanation": "Confronto direto pode escalar a situacao e aumentar o risco.",
        "correct_explanation": "Isso. Bloquear, denunciar e guardar provas e o caminho mais seguro.",
    },
    {
        "enemy_name": "Pirataria de Software",
        "description": "Arquivos piratas violam direitos autorais e podem trazer malware oculto.",
        "options": [
            "Comprar licenca oficial.",
            "Usar ativador crackeado.",
            "Baixar aplicativo em torrent duvidoso.",
            "Copiar jogo pago de terceiros.",
        ],
        "correct_option_index": 0,
        "explanation": "Ativadores e cracks sao vetores comuns para infeccoes graves.",
        "correct_explanation": "Correto. Software oficial reduz riscos tecnicos e juridicos.",
    },
    {
        "enemy_name": "Ameaca Deepfake",
        "description": "Videos e audios falsos gerados por IA podem parecer reais e manipular pessoas.",
        "options": [
            "Confiar em audio urgente sem verificar.",
            "Acreditar em video famoso sem checar fonte.",
            "Buscar inconsistencias e validar em fontes confiaveis.",
            "Assumir que sempre e facil detectar falsificacao.",
        ],
        "correct_option_index": 2,
        "explanation": "Deepfakes estao cada vez mais realistas e exigem verificacao ativa.",
        "correct_explanation": "Excelente. Pensamento critico e verificacao de fonte sao essenciais.",
    },
]

ATTACKS = [
    {"name": "Analise de Sistema", "type": "analise", "base_damage": 14},
    {"name": "Firewall Defensivo", "type": "defesa", "base_damage": 10},
    {"name": "Varredura Antivirus", "type": "antivirus", "base_damage": 16},
    {"name": "Forca Bruta", "type": "bruteforce", "base_damage": 18},
]

ENEMY_COMBAT_PROFILES = [
    {"max_health": 34, "weakness": "analise", "resistance": "defesa", "counter_damage": 1},
    {"max_health": 40, "weakness": "antivirus", "resistance": "bruteforce", "counter_damage": 1},
    {"max_health": 36, "weakness": "bruteforce", "resistance": "defesa", "counter_damage": 1},
    {"max_health": 42, "weakness": "antivirus", "resistance": "analise", "counter_damage": 1},
    {"max_health": 38, "weakness": "defesa", "resistance": "analise", "counter_damage": 1},
    {"max_health": 35, "weakness": "analise", "resistance": "defesa", "counter_damage": 1},
    {"max_health": 39, "weakness": "defesa", "resistance": "bruteforce", "counter_damage": 1},
    {"max_health": 37, "weakness": "defesa", "resistance": "bruteforce", "counter_damage": 1},
    {"max_health": 41, "weakness": "analise", "resistance": "antivirus", "counter_damage": 1},
    {"max_health": 44, "weakness": "analise", "resistance": "bruteforce", "counter_damage": 1},
]

GAME_STORY = (
    "A internet da cidade foi tomada por viloes digitais. "
    "Como Guardiao Digital, voce deve explorar o mapa, encontrar cada ameaca "
    "e neutralizar ataques digitais para proteger os usuarios."
)

CONCLUSION_TEXT = (
    "Voce neutralizou todas as ameacas do mapa.\n"
    "Leve essas praticas para fora do jogo:\n"
    "- Senhas fortes e unicas em cada servico.\n"
    "- Desconfianca de links e mensagens urgentes.\n"
    "- Atualizacao constante de apps e sistema.\n"
    "- Compartilhar orientacoes de seguranca com outras pessoas."
)

MAP_ROWS = len(WORLD_MAP_LAYOUT)
MAP_COLS = len(WORLD_MAP_LAYOUT[0])
MAP_WIDTH = MAP_COLS * TILE_SIZE
MAP_HEIGHT = MAP_ROWS * TILE_SIZE
MAP_OFFSET_X = (SCREEN_WIDTH - MAP_WIDTH) // 2
MAP_OFFSET_Y = (SCREEN_HEIGHT - MAP_HEIGHT) // 2

BATTLE_OPTION_RECTS = [
    pygame.Rect(80, 530, 515, 72),
    pygame.Rect(685, 530, 515, 72),
    pygame.Rect(80, 620, 515, 72),
    pygame.Rect(685, 620, 515, 72),
]

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Guardi\u00e3o Digital 2")
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


@dataclass
class Villain:
    id: int
    crime: dict
    tile_pos: Tuple[int, int]
    world_pos: Tuple[int, int]
    max_health: int
    health: int
    weakness: str
    resistance: str
    counter_damage: int
    defeated: bool = False


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
    screen.blit(panel, rect.topleft)


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


def find_start_tile() -> Tuple[int, int]:
    for row_index, row in enumerate(WORLD_MAP_LAYOUT):
        for col_index, cell in enumerate(row):
            if cell == "S":
                return col_index, row_index
    return 1, 1


def tile_is_walkable(tile_x: int, tile_y: int) -> bool:
    if tile_x < 0 or tile_y < 0 or tile_x >= MAP_COLS or tile_y >= MAP_ROWS:
        return False
    return WORLD_MAP_LAYOUT[tile_y][tile_x] != "#"


def tile_to_rect(tile_x: int, tile_y: int) -> pygame.Rect:
    return pygame.Rect(
        MAP_OFFSET_X + tile_x * TILE_SIZE,
        MAP_OFFSET_Y + tile_y * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE,
    )


def tile_to_center(tile_x: int, tile_y: int) -> Tuple[int, int]:
    rect = tile_to_rect(tile_x, tile_y)
    return rect.centerx, rect.centery


START_TILE = find_start_tile()
START_CENTER = tile_to_center(START_TILE[0], START_TILE[1])

villains: List[Villain] = []
for crime_index, crime_data in enumerate(crimes):
    fallback_pos = START_TILE
    spawn = VILLAIN_SPAWNS[crime_index] if crime_index < len(VILLAIN_SPAWNS) else fallback_pos
    combat_profile = ENEMY_COMBAT_PROFILES[crime_index]
    if not tile_is_walkable(spawn[0], spawn[1]):
        spawn = fallback_pos
    villains.append(
        Villain(
            id=crime_index,
            crime=crime_data,
            tile_pos=spawn,
            world_pos=tile_to_center(spawn[0], spawn[1]),
            max_health=combat_profile["max_health"],
            health=combat_profile["max_health"],
            weakness=combat_profile["weakness"],
            resistance=combat_profile["resistance"],
            counter_damage=combat_profile["counter_damage"],
        )
    )

player_health = 5
max_player_health = 5
player_position = pygame.Vector2(START_CENTER[0], START_CENTER[1])
game_state = "menu"
active_villain_id: Optional[int] = None
feedback_active = False
feedback_title = ""
feedback_message = ""
feedback_tone = "neutral"
encounter_lock_villain_id: Optional[int] = None


def get_active_villain() -> Optional[Villain]:
    if active_villain_id is None:
        return None
    for villain in villains:
        if villain.id == active_villain_id:
            return villain
    return None


def remaining_villains_count() -> int:
    return sum(1 for villain in villains if not villain.defeated)


def all_villains_defeated() -> bool:
    return remaining_villains_count() == 0


def build_player_hitbox(x: float, y: float) -> pygame.Rect:
    rect = pygame.Rect(0, 0, PLAYER_HITBOX_SIZE, PLAYER_HITBOX_SIZE)
    rect.center = (round(x), round(y))
    return rect


def get_player_hitbox() -> pygame.Rect:
    return build_player_hitbox(player_position.x, player_position.y)


def hitbox_collides_with_wall(hitbox: pygame.Rect) -> bool:
    if (
        hitbox.left < MAP_OFFSET_X
        or hitbox.top < MAP_OFFSET_Y
        or hitbox.right > MAP_OFFSET_X + MAP_WIDTH
        or hitbox.bottom > MAP_OFFSET_Y + MAP_HEIGHT
    ):
        return True

    start_col = max(0, (hitbox.left - MAP_OFFSET_X) // TILE_SIZE)
    end_col = min(MAP_COLS - 1, (hitbox.right - 1 - MAP_OFFSET_X) // TILE_SIZE)
    start_row = max(0, (hitbox.top - MAP_OFFSET_Y) // TILE_SIZE)
    end_row = min(MAP_ROWS - 1, (hitbox.bottom - 1 - MAP_OFFSET_Y) // TILE_SIZE)

    for row_index in range(start_row, end_row + 1):
        for col_index in range(start_col, end_col + 1):
            if WORLD_MAP_LAYOUT[row_index][col_index] != "#":
                continue
            if hitbox.colliderect(tile_to_rect(col_index, row_index)):
                return True
    return False


def find_villain_touching_player() -> Optional[Villain]:
    player_hitbox = get_player_hitbox()
    for villain in villains:
        if villain.defeated:
            continue
        enemy_rect = map_enemy_images[villain.id].get_rect(center=villain.world_pos).inflate(
            VILLAIN_TRIGGER_PADDING, VILLAIN_TRIGGER_PADDING
        )
        if player_hitbox.colliderect(enemy_rect):
            return villain
    return None


def draw_health_bar(surface: pygame.Surface, x: int, y: int) -> None:
    draw_text("Integridade", help_font, WHITE, surface, x, y)
    bar_x = x + 140
    bar_y = y + 2
    segment_width = 40
    segment_height = 16
    total_width = segment_width * max_player_health
    pygame.draw.rect(surface, RED, (bar_x, bar_y, total_width, segment_height), border_radius=3)
    if player_health > 0:
        pygame.draw.rect(
            surface,
            GREEN,
            (bar_x, bar_y, segment_width * player_health, segment_height),
            border_radius=3,
        )


def draw_menu_screen() -> None:
    screen.blit(menu_image, (0, 0))

    title_panel = pygame.Rect(180, 92, 920, 240)
    draw_panel(title_panel)
    draw_text("GUARDI\u00c3O DIGITAL 2", menu_font, WHITE, screen, SCREEN_WIDTH // 2, 155, center=True)
    draw_text(
        "Explore o mapa, encontre viloes e neutralize crimes digitais",
        description_font,
        WHITE,
        screen,
        SCREEN_WIDTH // 2,
        220,
        center=True,
    )
    draw_text(
        "ENTER ou clique para iniciar",
        title_font,
        WHITE,
        screen,
        SCREEN_WIDTH // 2,
        282,
        center=True,
    )
    draw_text("F11 alterna tela cheia", help_font, WHITE, screen, SCREEN_WIDTH - 180, 12)


def draw_story_screen() -> None:
    screen.blit(historia_bg, (0, 0))
    portrait_rect = player_image_portrait.get_rect(center=(SCREEN_WIDTH * 0.20, SCREEN_HEIGHT * 0.54))
    screen.blit(player_image_portrait, portrait_rect)

    story_panel = pygame.Rect(450, 92, 760, 530)
    draw_panel(story_panel)
    draw_text("Missao no mapa", title_font, WHITE, screen, story_panel.centerx, 136, center=True)
    draw_text_block(
        GAME_STORY,
        story_font,
        WHITE,
        screen,
        story_panel.x + 45,
        story_panel.y + 205,
        story_panel.width - 90,
        center=False,
    )
    draw_text(
        "Pressione ENTER ou clique para explorar",
        help_font,
        WHITE,
        screen,
        story_panel.centerx,
        story_panel.bottom - 40,
        center=True,
    )


def draw_world_screen() -> None:
    screen.fill((23, 32, 31))

    for row_index, row in enumerate(WORLD_MAP_LAYOUT):
        for col_index, cell in enumerate(row):
            tile_rect = tile_to_rect(col_index, row_index)
            if cell == "#":
                color = WALL_COLOR if (row_index + col_index) % 2 == 0 else WALL_COLOR_ALT
            elif cell == "S":
                color = START_COLOR
            else:
                color = PATH_COLOR if (row_index + col_index) % 2 == 0 else PATH_COLOR_ALT
            pygame.draw.rect(screen, color, tile_rect)

    pygame.draw.rect(
        screen,
        GRID_COLOR,
        (MAP_OFFSET_X - 2, MAP_OFFSET_Y - 2, MAP_WIDTH + 4, MAP_HEIGHT + 4),
        2,
    )

    for villain in villains:
        if villain.defeated:
            continue
        center_x, center_y = villain.world_pos
        pygame.draw.circle(screen, (163, 42, 42), (center_x, center_y), TILE_SIZE // 2 - 6)
        sprite = map_enemy_images[villain.id]
        sprite_rect = sprite.get_rect(center=(center_x, center_y))
        screen.blit(sprite, sprite_rect)

    player_center = (round(player_position.x), round(player_position.y))
    player_rect = player_image_map.get_rect(center=player_center)
    screen.blit(player_image_map, player_rect)

    hud = pygame.Surface((SCREEN_WIDTH, 84), pygame.SRCALPHA)
    hud.fill(HUD_BG)
    screen.blit(hud, (0, 0))
    draw_health_bar(screen, 14, 11)
    draw_text(
        f"Viloes restantes: {remaining_villains_count()}",
        help_font,
        WHITE,
        screen,
        14,
        38,
    )
    draw_text(
        "Mover livremente: segure WASD/Setas | Toque no vilao para iniciar encontro",
        help_font,
        WHITE,
        screen,
        SCREEN_WIDTH // 2,
        17,
        center=True,
    )
    draw_text("F11: tela cheia", help_font, WHITE, screen, SCREEN_WIDTH - 180, 11)


def draw_encounter_screen() -> None:
    villain = get_active_villain()
    if villain is None:
        return

    screen.blit(introducao_bg, (0, 0))
    crime = villain.crime
    enemy_image = dossier_enemy_images[villain.id]

    encounter_panel = pygame.Rect(180, 92, 920, 548)
    draw_panel(encounter_panel)

    draw_text(crime["enemy_name"], title_font, WHITE, screen, encounter_panel.centerx, 138, center=True)
    image_rect = enemy_image.get_rect(center=(encounter_panel.centerx, 265))
    screen.blit(enemy_image, image_rect)
    draw_text_block(
        crime["description"],
        description_font,
        WHITE,
        screen,
        encounter_panel.x + 54,
        encounter_panel.y + 330,
        encounter_panel.width - 108,
        center=False,
    )
    draw_text(
        "ENTER/click: enfrentar | ESC: voltar ao mapa",
        help_font,
        WHITE,
        screen,
        encounter_panel.centerx,
        encounter_panel.bottom - 28,
        center=True,
    )


def draw_enemy_health_bar(surface: pygame.Surface, villain: Villain, x: int, y: int, width: int = 320) -> None:
    draw_text("Estabilidade do inimigo", help_font, WHITE, surface, x, y)
    bar_rect = pygame.Rect(x, y + 18, width, 18)
    pygame.draw.rect(surface, RED, bar_rect, border_radius=4)
    if villain.health > 0:
        current_width = int(width * (villain.health / villain.max_health))
        pygame.draw.rect(surface, GREEN, (bar_rect.x, bar_rect.y, current_width, bar_rect.height), border_radius=4)
    draw_text(f"{villain.health}/{villain.max_health}", help_font, WHITE, surface, bar_rect.right - 52, y - 1)


def draw_feedback_overlay() -> None:
    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    if feedback_tone == "victory":
        overlay.fill((0, 100, 0, 180))
    elif feedback_tone == "defeat":
        overlay.fill((110, 0, 0, 180))
    else:
        overlay.fill((20, 55, 90, 180))
    screen.blit(overlay, (0, 0))
    feedback_panel = pygame.Rect(140, 120, 1000, 450)
    draw_panel(feedback_panel, (15, 20, 24, 220))

    draw_text(feedback_title, feedback_font, WHITE, screen, feedback_panel.centerx, 186, center=True)
    draw_text_block(
        feedback_message,
        description_font,
        WHITE,
        screen,
        feedback_panel.x + 58,
        feedback_panel.y + 230,
        feedback_panel.width - 116,
        center=False,
    )

    if player_health <= 0:
        footer = "Integridade zerada. ENTER ou clique para continuar."
    else:
        villain = get_active_villain()
        villain_defeated = villain.defeated if villain is not None else False
        if villain_defeated and all_villains_defeated():
            footer = "Todos os viloes foram derrotados. ENTER ou clique para concluir a missao."
        elif villain_defeated:
            footer = "Vilao neutralizado. ENTER ou clique para voltar ao mapa."
        else:
            footer = "ENTER ou clique para continuar o combate."

    draw_text(footer, help_font, WHITE, screen, feedback_panel.centerx, feedback_panel.bottom - 35, center=True)


def draw_battle_screen() -> None:
    villain = get_active_villain()
    if villain is None:
        return

    screen.blit(combate_bg, (0, 0))

    enemy_pos = (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.29))
    player_pos = (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.54))

    enemy_image = combat_enemy_images[villain.id]
    enemy_rect = enemy_image.get_rect(center=enemy_pos)
    screen.blit(enemy_image, enemy_rect)

    player_rect = player_image_combat.get_rect(center=player_pos)
    screen.blit(player_image_combat, player_rect)

    battle_header = pygame.Rect(230, 16, 820, 92)
    draw_panel(battle_header, (18, 24, 28, 200))
    draw_text(villain.crime["enemy_name"], title_font, WHITE, screen, battle_header.centerx, 40, center=True)
    draw_health_bar(screen, battle_header.x + 26, 73)
    draw_enemy_health_bar(screen, villain, battle_header.right - 348, 46)

    info_panel = pygame.Rect(160, 365, 960, 112)
    draw_panel(info_panel, (18, 24, 28, 200))
    draw_text_block(
        villain.crime["description"],
        description_font,
        WHITE,
        screen,
        info_panel.x + 30,
        info_panel.y + 24,
        info_panel.width - 60,
        center=False,
    )

    for index, attack in enumerate(ATTACKS):
        option_rect = BATTLE_OPTION_RECTS[index]
        pygame.draw.rect(screen, BUTTON_COLOR, option_rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_BORDER, option_rect, 2, border_radius=10)
        labeled_option = f"{index + 1}. {attack['name']}\nTipo: {attack['type']} | Dano: {attack['base_damage']}"
        draw_text_block(
            labeled_option,
            option_font,
            TEXT_DARK,
            screen,
            option_rect.centerx,
            option_rect.centery,
            option_rect.width - 30,
            center=True,
            line_gap=2,
        )

    draw_text(
        "Escolha um ataque com clique ou teclas 1-4",
        help_font,
        WHITE,
        screen,
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 14,
        center=True,
    )

    if feedback_active:
        draw_feedback_overlay()


def draw_conclusion_screen() -> None:
    screen.blit(conclusao_bg, (0, 0))
    conclusion_panel = pygame.Rect(160, 96, 960, 536)
    draw_panel(conclusion_panel)
    draw_text("Missao concluida", title_font, GREEN, screen, conclusion_panel.centerx, 146, center=True)
    draw_text_block(
        CONCLUSION_TEXT,
        description_font,
        WHITE,
        screen,
        conclusion_panel.x + 60,
        conclusion_panel.y + 220,
        conclusion_panel.width - 120,
        center=False,
    )
    draw_text(
        "ENTER ou clique para tela de vitoria",
        help_font,
        WHITE,
        screen,
        conclusion_panel.centerx,
        conclusion_panel.bottom - 30,
        center=True,
    )


def draw_end_screen() -> None:
    if game_state == "victory":
        screen.blit(vitoria_image, (0, 0))
    elif game_state == "game_over":
        screen.blit(derrota_image, (0, 0))

    end_panel = pygame.Rect(290, 618, 700, 56)
    draw_panel(end_panel, (18, 24, 28, 200))
    draw_text(
        "ENTER ou clique para voltar ao menu",
        help_font,
        WHITE,
        screen,
        end_panel.centerx,
        end_panel.centery,
        center=True,
    )


def reset_progress() -> None:
    global player_health, active_villain_id, feedback_active, feedback_title, feedback_message, feedback_tone, encounter_lock_villain_id
    player_health = max_player_health
    player_position.x = START_CENTER[0]
    player_position.y = START_CENTER[1]
    active_villain_id = None
    feedback_active = False
    feedback_title = ""
    feedback_message = ""
    feedback_tone = "neutral"
    encounter_lock_villain_id = None
    for villain in villains:
        villain.defeated = False
        villain.health = villain.max_health


def move_player_continuous(input_x: int, input_y: int, dt: float) -> None:
    if input_x == 0 and input_y == 0:
        return

    move_vector = pygame.Vector2(input_x, input_y)
    if move_vector.length_squared() > 1:
        move_vector = move_vector.normalize()
    move_vector *= PLAYER_SPEED * dt

    next_x = player_position.x + move_vector.x
    if not hitbox_collides_with_wall(build_player_hitbox(next_x, player_position.y)):
        player_position.x = next_x

    next_y = player_position.y + move_vector.y
    if not hitbox_collides_with_wall(build_player_hitbox(player_position.x, next_y)):
        player_position.y = next_y


def update_exploration(dt: float) -> None:
    keys = pygame.key.get_pressed()
    horizontal = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
    vertical = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
    move_player_continuous(horizontal, vertical, dt)
    try_trigger_encounter()


def try_trigger_encounter() -> None:
    global game_state, active_villain_id, encounter_lock_villain_id
    villain = find_villain_touching_player()

    if encounter_lock_villain_id is not None:
        if villain is None or villain.id != encounter_lock_villain_id:
            encounter_lock_villain_id = None
        else:
            return

    if villain is not None:
        active_villain_id = villain.id
        game_state = "encounter"


def calculate_attack_damage(attack: dict, villain: Villain) -> Tuple[int, str]:
    damage = attack["base_damage"]
    effectiveness = "normal"

    if attack["type"] == villain.weakness:
        damage += 6
        effectiveness = "fraqueza"
    elif attack["type"] == villain.resistance:
        damage = max(4, damage - 6)
        effectiveness = "resistencia"

    return damage, effectiveness


def open_battle_feedback(title: str, message: str, tone: str) -> None:
    global feedback_active, feedback_title, feedback_message, feedback_tone
    feedback_active = True
    feedback_title = title
    feedback_message = message
    feedback_tone = tone


def resolve_battle_turn(selected_index: int) -> None:
    global player_health
    villain = get_active_villain()
    if villain is None:
        return

    attack = ATTACKS[selected_index]
    damage, effectiveness = calculate_attack_damage(attack, villain)
    villain.health = max(0, villain.health - damage)

    if effectiveness == "fraqueza":
        attack_result = f"{attack['name']} explorou a fraqueza do inimigo e causou {damage} de dano."
    elif effectiveness == "resistencia":
        attack_result = f"{attack['name']} encontrou resistencia e causou apenas {damage} de dano."
    else:
        attack_result = f"{attack['name']} causou {damage} de dano."

    if villain.health <= 0:
        villain.defeated = True
        open_battle_feedback(
            "Vilao neutralizado",
            f"{attack_result} {villain.crime['enemy_name']} foi derrotado.",
            "victory",
        )
        return

    player_health = max(0, player_health - villain.counter_damage)
    counter_result = (
        f"{villain.crime['enemy_name']} contra-atacou e causou "
        f"{villain.counter_damage} de dano a sua integridade."
    )

    if player_health <= 0:
        open_battle_feedback(
            "Integridade comprometida",
            f"{attack_result} {counter_result}",
            "defeat",
        )
    else:
        open_battle_feedback(
            "Troca de golpes",
            f"{attack_result} {counter_result}",
            "neutral",
        )


def close_feedback_and_continue() -> None:
    global game_state, active_villain_id, feedback_active, encounter_lock_villain_id
    previous_villain_id = active_villain_id
    feedback_active = False
    if player_health <= 0:
        active_villain_id = None
        game_state = "game_over"
        return

    villain = get_active_villain()
    if villain is not None and villain.defeated:
        active_villain_id = None
        if all_villains_defeated():
            game_state = "conclusion"
            return
        encounter_lock_villain_id = previous_villain_id
        game_state = "exploring"
        return

    game_state = "battle"


def toggle_fullscreen() -> None:
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(SCREEN_SIZE)


def key_to_attack_index(event_key: int) -> Optional[int]:
    key_map = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_KP1: 0,
        pygame.K_KP2: 1,
        pygame.K_KP3: 2,
        pygame.K_KP4: 3,
    }
    return key_map.get(event_key)


def main() -> None:
    global game_state, active_villain_id, encounter_lock_villain_id

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()

            if game_state == "menu":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    reset_progress()
                    game_state = "exploring"

            elif game_state == "story":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "exploring"

            elif game_state == "exploring":
                pass

            elif game_state == "encounter":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    encounter_lock_villain_id = active_villain_id
                    active_villain_id = None
                    game_state = "exploring"
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "battle"

            elif game_state == "battle":
                if feedback_active:
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                        close_feedback_and_continue()
                else:
                    selected_index: Optional[int] = None
                    if event.type == pygame.KEYDOWN:
                        selected_index = key_to_attack_index(event.key)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for index, rect in enumerate(BATTLE_OPTION_RECTS):
                            if rect.collidepoint(event.pos):
                                selected_index = index
                                break

                    if selected_index is not None:
                        resolve_battle_turn(selected_index)

            elif game_state == "conclusion":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "victory"

            elif game_state in ("victory", "game_over"):
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "menu"

        if game_state == "exploring":
            update_exploration(dt)

        if game_state == "menu":
            draw_menu_screen()
        elif game_state == "story":
            draw_story_screen()
        elif game_state == "exploring":
            draw_world_screen()
        elif game_state == "encounter":
            draw_encounter_screen()
        elif game_state == "battle":
            draw_battle_screen()
        elif game_state == "conclusion":
            draw_conclusion_screen()
        elif game_state in ("victory", "game_over"):
            draw_end_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
