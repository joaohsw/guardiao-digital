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
    (3, 6),
    (9, 3),
    (8, 8),
    (10, 9),
    (14, 9),
    (13, 4),
    (7, 5),
    (17, 8),
    (18, 1),
    (18, 9),
]

ENEMY_KEYS = [
    "phishing",
    "malware",
    "senha",
    "ransomware",
    "spyware",
    "adware",
    "golpe",
    "cyberstalking",
    "pirataria",
    "deepfake",
]

ENEMY_REQUIRED_WEAPON = {
    "phishing": "verificacao",
    "malware": "protecao",
    "senha": "privacidade",
    "ransomware": "protecao",
    "spyware": "privacidade",
    "adware": "protecao",
    "golpe": "verificacao",
    "cyberstalking": "acao",
    "pirataria": "acao",
    "deepfake": "verificacao",
}

COLLECTIBLE_DROPS = [
    {
        "id": "livro_guia",
        "name": "Livro do Guardiao",
        "category": "book",
        "asset_key": "book",
        "tile_pos": (4, 1),
    },
    {
        "id": "arma_verificacao",
        "name": "Verificacao",
        "category": "weapon",
        "asset_key": "verificacao",
        "weapon_type": "verificacao",
        "tile_pos": (2, 3),
    },
    {
        "id": "arma_protecao",
        "name": "Protecao",
        "category": "weapon",
        "asset_key": "protecao",
        "weapon_type": "protecao",
        "tile_pos": (8, 3),
    },
    {
        "id": "arma_privacidade",
        "name": "Privacidade",
        "category": "weapon",
        "asset_key": "privacidade",
        "weapon_type": "privacidade",
        "tile_pos": (10, 5),
    },
    {
        "id": "arma_acao",
        "name": "Acao",
        "category": "weapon",
        "asset_key": "acao",
        "weapon_type": "acao",
        "tile_pos": (13, 7),
    },
    {
        "id": "kit_recuperacao",
        "name": "Kit de Recuperacao",
        "category": "healing",
        "asset_key": "cura",
        "heal_amount": 2,
        "tile_pos": (5, 9),
    },
    {
        "id": "kit_recuperacao_norte",
        "name": "Kit de Recuperacao",
        "category": "healing",
        "asset_key": "cura",
        "heal_amount": 2,
        "tile_pos": (11, 3),
    },
    {
        "id": "kit_recuperacao_leste",
        "name": "Kit de Recuperacao",
        "category": "healing",
        "asset_key": "cura",
        "heal_amount": 2,
        "tile_pos": (16, 6),
    },
    {
        "id": "kit_recuperacao_oeste",
        "name": "Kit de Recuperacao",
        "category": "healing",
        "asset_key": "cura",
        "heal_amount": 2,
        "tile_pos": (2, 8),
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

ATTACK_CATEGORIES = {
    "privacidade": {"name": "Privacidade", "asset_key": "privacidade"},
    "verificacao": {"name": "Verificacao", "asset_key": "verificacao"},
    "protecao": {"name": "Protecao", "asset_key": "protecao"},
    "acao": {"name": "Acao", "asset_key": "acao"},
}

CATEGORY_ATTACKS = {
    "privacidade": [
        {"id": "perfil_privado", "name": "Perfil privado"},
        {"id": "permissoes", "name": "Revisar permissoes"},
        {"id": "2fa", "name": "Ativar 2FA"},
        {"id": "ocultar_dados", "name": "Ocultar dados pessoais"},
    ],
    "verificacao": [
        {"id": "verificador_link", "name": "Verificar links"},
        {"id": "checagem_fonte", "name": "Checar fonte"},
        {"id": "analise_contexto", "name": "Analisar contexto"},
        {"id": "verificacao_identidade", "name": "Verificar identidade"},
    ],
    "protecao": [
        {"id": "antivirus", "name": "Antivirus"},
        {"id": "backup", "name": "Backup seguro"},
        {"id": "firewall", "name": "Firewall"},
        {"id": "bloqueador_anuncios", "name": "Bloqueador de anuncios"},
        {"id": "atualizacao", "name": "Atualizar sistema"},
    ],
    "acao": [
        {"id": "bloquear", "name": "Bloquear agressor"},
        {"id": "denunciar", "name": "Denunciar"},
        {"id": "download_oficial", "name": "Download oficial"},
        {"id": "remover_app_suspeito", "name": "Remover app suspeito"},
    ],
}

ATTACK_EFFECTIVENESS = {
    "adware": {
        "forte": ["bloqueador_anuncios"],
        "medio": ["antivirus"],
        "fraco": ["backup"],
    },
    "malware": {
        "forte": ["antivirus"],
        "medio": ["atualizacao"],
        "fraco": ["verificador_link"],
    },
    "phishing": {
        "forte": ["verificador_link"],
        "medio": ["2fa"],
        "fraco": ["antivirus"],
    },
    "senha": {
        "forte": ["2fa"],
        "medio": ["permissoes"],
        "fraco": ["bloqueador_anuncios"],
    },
    "ransomware": {
        "forte": ["backup"],
        "medio": ["antivirus"],
        "fraco": ["bloqueador_anuncios"],
    },
    "spyware": {
        "forte": ["permissoes"],
        "medio": ["antivirus"],
        "fraco": ["backup"],
    },
    "golpe": {
        "forte": ["verificacao_identidade"],
        "medio": ["verificador_link"],
        "fraco": ["bloqueador_anuncios"],
    },
    "deepfake": {
        "forte": ["checagem_fonte"],
        "medio": ["analise_contexto"],
        "fraco": ["antivirus"],
    },
    "pirataria": {
        "forte": ["download_oficial"],
        "medio": ["antivirus"],
        "fraco": ["backup"],
    },
    "cyberstalking": {
        "forte": ["perfil_privado"],
        "medio": ["bloquear"],
        "fraco": ["antivirus"],
    },
}

EFFECTIVENESS_LABELS = {
    "forte": "forte",
    "medio": "medio",
    "fraco": "fraco",
    "neutro": "neutro",
}

EFFECTIVENESS_DAMAGE = {
    "forte": 24,
    "medio": 14,
    "fraco": 6,
    "neutro": 10,
}

COUNTER_DAMAGE_MODIFIERS = {
    "forte": -999,
    "medio": 0,
    "fraco": 1,
    "neutro": 0,
}

NON_FINISHING_EFFECTS = {"neutro"}

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

BATTLE_FLEE_RECT = pygame.Rect(1040, 487, 160, 38)
WARNING_PROCEED_RECT = pygame.Rect(420, 442, 200, 46)
WARNING_BACK_RECT = pygame.Rect(660, 442, 200, 46)

SUBATTACK_OPTION_RECTS = [
    pygame.Rect(210, 500, 860, 34),
    pygame.Rect(210, 540, 860, 34),
    pygame.Rect(210, 580, 860, 34),
    pygame.Rect(210, 620, 860, 34),
    pygame.Rect(210, 660, 860, 34),
]

BOOK_HUD_RECT = pygame.Rect(SCREEN_WIDTH - 74, 12, 56, 56)
BOOK_CLOSE_RECT = pygame.Rect(SCREEN_WIDTH - 205, 612, 150, 42)
BOOK_PREV_RECT = pygame.Rect(355, 612, 150, 42)
BOOK_NEXT_RECT = pygame.Rect(775, 612, 150, 42)
BOOK_PAGE_SIZE = 2
