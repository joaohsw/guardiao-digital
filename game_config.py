import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

ASSETS_PATH = "assets"
WINDOW_TITLE = "Guardi\u00e3o Digital 2"
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

COLLECTIBLE_DROPS = [
    {
        "id": "livro_guia",
        "name": "Livro do Guardiao",
        "category": "book",
        "asset_key": "book",
        "tile_pos": (4, 4),
    },
    {
        "id": "arma_verificacao",
        "name": "Verificacao",
        "category": "weapon",
        "asset_key": "verificacao",
        "weapon_type": "verificacao",
        "tile_pos": (13, 2),
    },
    {
        "id": "arma_protecao",
        "name": "Protecao",
        "category": "weapon",
        "asset_key": "protecao",
        "weapon_type": "protecao",
        "tile_pos": (1, 9),
    },
    {
        "id": "arma_privacidade",
        "name": "Privacidade",
        "category": "weapon",
        "asset_key": "privacidade",
        "weapon_type": "privacidade",
        "tile_pos": (8, 9),
    },
    {
        "id": "arma_acao",
        "name": "Acao",
        "category": "weapon",
        "asset_key": "acao",
        "weapon_type": "acao",
        "tile_pos": (18, 6),
    },
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
