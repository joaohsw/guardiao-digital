import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

MAIN_16_9_RESOLUTIONS = [
    (1024, 576),
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (3840, 2160),
]

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
HUD_BG = (28, 34, 38)
PANEL_BG = (18, 24, 28, 210)
PANEL_BORDER = (202, 214, 197)
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
BATTLE_BUTTON_COLOR = (12, 48, 56, 200)
BATTLE_BUTTON_BORDER = (0, 200, 220)
BATTLE_TEXT = (0, 230, 255)
DEFEAT_BUTTON_COLOR = (56, 10, 24, 210)
DEFEAT_BUTTON_BORDER = (255, 36, 96)
DEFEAT_TEXT = (255, 72, 118)

WORLD_MAP_LAYOUT = [
    "####################",
    "#S....#.......#....#",
    "#.##..#.#######.##.#",
    "#....##.....###....#",
    "###......##.#.###..#",
    "#...####....#......#",
    "#.#...####.####.##.#",
    "#.#.#....#....#.##.#",
    "#...#.##.######....#",
    "#.....#............#",
    "####################",
]

VILLAIN_SPAWNS = [
    (3, 6),
    (9, 3),
    (8, 8),
    (10, 9),
    (14, 9),
    (13, 4),
    (8, 5),
    (17, 8),
    (18, 1),
    (17, 5),
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
        "tile_pos": (3, 4),
    },
    {
        "id": "kit_recuperacao_norte",
        "name": "Kit de Recuperacao",
        "category": "healing",
        "asset_key": "cura",
        "heal_amount": 2,
        "tile_pos": (14, 5),
    },
    {
        "id": "kit_recuperacao_leste",
        "name": "Kit de Recuperacao",
        "category": "healing",
        "asset_key": "cura",
        "heal_amount": 2,
        "tile_pos": (1, 8),
    },
    {
        "id": "kit_recuperacao_oeste",
        "name": "Kit de Recuperacao",
        "category": "healing",
        "asset_key": "cura",
        "heal_amount": 2,
        "tile_pos": (7, 7),
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
        "extremo": ["bloqueador_anuncios", "remover_app_suspeito"],
        "eficaz": ["antivirus", "atualizacao"],
        "medio": ["firewall", "permissoes", "verificador_link", "ocultar_dados", "denunciar", "perfil_privado"],
        "ineficaz": ["backup", "2fa", "download_oficial", "analise_contexto", "bloquear", "checagem_fonte", "verificacao_identidade"],
    },
    "malware": {
        "extremo": ["antivirus", "remover_app_suspeito"],
        "eficaz": ["atualizacao", "firewall"],
        "medio": ["verificador_link", "backup", "bloqueador_anuncios", "permissoes", "download_oficial"],
        "ineficaz": ["perfil_privado", "2fa", "ocultar_dados", "analise_contexto", "bloquear", "checagem_fonte", "denunciar", "verificacao_identidade"],
    },
    "phishing": {
        "extremo": ["verificador_link", "verificacao_identidade"],
        "eficaz": ["checagem_fonte", "2fa"],
        "medio": ["analise_contexto", "perfil_privado", "firewall", "permissoes", "ocultar_dados", "denunciar"],
        "ineficaz": ["antivirus", "backup", "bloqueador_anuncios", "atualizacao", "bloquear", "download_oficial", "remover_app_suspeito"],
    },
    "senha": {
        "extremo": ["2fa", "permissoes"],
        "eficaz": ["ocultar_dados", "verificacao_identidade"],
        "medio": ["perfil_privado", "atualizacao", "firewall", "analise_contexto", "verificador_link"],
        "ineficaz": ["bloqueador_anuncios", "backup", "antivirus", "bloquear", "checagem_fonte", "denunciar", "download_oficial", "remover_app_suspeito"],
    },
    "ransomware": {
        "extremo": ["backup", "antivirus"],
        "eficaz": ["atualizacao", "firewall"],
        "medio": ["verificador_link", "remover_app_suspeito", "download_oficial", "permissoes", "verificacao_identidade", "checagem_fonte"],
        "ineficaz": ["bloqueador_anuncios", "perfil_privado", "2fa", "analise_contexto", "bloquear", "denunciar", "ocultar_dados"],
    },
    "spyware": {
        "extremo": ["permissoes", "remover_app_suspeito"],
        "eficaz": ["antivirus", "ocultar_dados"],
        "medio": ["atualizacao", "firewall", "perfil_privado", "verificador_link", "verificacao_identidade", "2fa", "analise_contexto"],
        "ineficaz": ["backup", "bloqueador_anuncios", "download_oficial", "bloquear", "checagem_fonte", "denunciar"],
    },
    "golpe": {
        "extremo": ["verificacao_identidade", "checagem_fonte"],
        "eficaz": ["verificador_link", "2fa"],
        "medio": ["analise_contexto", "ocultar_dados", "denunciar", "perfil_privado", "permissoes"],
        "ineficaz": ["bloqueador_anuncios", "backup", "antivirus", "atualizacao", "bloquear", "download_oficial", "firewall", "remover_app_suspeito"],
    },
    "deepfake": {
        "extremo": ["checagem_fonte", "analise_contexto"],
        "eficaz": ["verificacao_identidade", "denunciar"],
        "medio": ["verificador_link", "perfil_privado", "ocultar_dados", "2fa"],
        "ineficaz": ["antivirus", "backup", "firewall", "atualizacao", "bloqueador_anuncios", "bloquear", "download_oficial", "permissoes", "remover_app_suspeito"],
    },
    "pirataria": {
        "extremo": ["download_oficial", "remover_app_suspeito"],
        "eficaz": ["antivirus", "atualizacao"],
        "medio": ["backup", "checagem_fonte", "denunciar", "analise_contexto", "verificador_link"],
        "ineficaz": ["bloquear", "perfil_privado", "2fa", "bloqueador_anuncios", "firewall", "ocultar_dados", "permissoes", "verificacao_identidade"],
    },
    "cyberstalking": {
        "extremo": ["bloquear", "denunciar"],
        "eficaz": ["perfil_privado", "ocultar_dados"],
        "medio": ["verificacao_identidade", "permissoes", "2fa", "analise_contexto", "checagem_fonte"],
        "ineficaz": ["antivirus", "backup", "bloqueador_anuncios", "atualizacao", "download_oficial", "firewall", "remover_app_suspeito", "verificador_link"],
    },
}

THREAT_STRATEGY_HINTS = {
    "adware": (
        "A fonte dos anuncios importa mais que os sintomas.",
        "Cortar o canal invasivo tende a render melhor.",
        "So recuperar o sistema pode nao impedir o retorno.",
    ),
    "malware": (
        "A ameaca parece pedir limpeza direta do dispositivo.",
        "Fechar falhas e remover codigo suspeito aumenta a pressao.",
        "Medidas de privacidade sozinhas nao atacam o nucleo do problema.",
    ),
    "phishing": (
        "O golpe depende de link, remetente e identidade.",
        "Validar sinais da mensagem antes de agir muda a luta.",
        "Ferramentas do aparelho ajudam pouco se a armadilha for social.",
    ),
    "senha": (
        "A brecha esta na autenticacao da conta.",
        "Camadas extras de entrada costumam virar esse confronto.",
        "Bloquear anuncios ou recuperar arquivos nao fortalece a porta.",
    ),
    "ransomware": (
        "Quando arquivos viram refens, recuperacao confiavel pesa muito.",
        "Prevenir infeccao tambem reduz o estrago.",
        "Medidas contra anuncios nao resolvem arquivos sequestrados.",
    ),
    "spyware": (
        "Observe quem ainda tem permissao para espiar em silencio.",
        "Remover apps suspeitos e reduzir coleta de dados enfraquece a ameaca.",
        "Ter copia dos arquivos nao impede monitoramento ativo.",
    ),
    "golpe": (
        "A fraude se apoia em confianca e identidade.",
        "Confirmar quem esta do outro lado revela rachaduras no plano.",
        "Defesas tecnicas ajudam menos quando a pressao e emocional.",
    ),
    "deepfake": (
        "A pista esta na origem e no contexto da midia.",
        "Comparar fontes derruba melhor a manipulacao.",
        "Proteger o dispositivo nao prova se o conteudo e real.",
    ),
    "pirataria": (
        "A origem do software e o coracao do risco.",
        "Remover instalacoes suspeitas reduz o perigo depois do download.",
        "Defesas sociais ajudam pouco contra um arquivo adulterado.",
    ),
    "cyberstalking": (
        "Reduzir o alcance do agressor muda o ritmo da ameaca.",
        "Privacidade e registro do abuso trabalham bem juntos.",
        "Ferramentas contra malware nao resolvem assedio continuo.",
    ),
}

EFFECTIVENESS_LABELS = {
    "extremo": "extremamente eficaz",
    "eficaz": "eficaz",
    "medio": "medio",
    "ineficaz": "ineficaz",
}

EFFECTIVENESS_DAMAGE = {
    "extremo": 26,
    "eficaz": 18,
    "medio": 10,
    "ineficaz": 4,
}

COUNTER_DAMAGE_MODIFIERS = {
    "extremo": -999,
    "eficaz": 0,
    "medio": 0,
    "ineficaz": 1,
}

NON_FINISHING_EFFECTS = set()

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
    "A Cidade Conectada esta sob ataque. Links falsos, programas maliciosos, "
    "golpes, perseguicoes online e conteudos manipulados abriram falhas pelos "
    "caminhos da rede.\n"
    "\n"
    "Voce e o Guardiao Digital: um defensor treinado para reconhecer sinais de "
    "risco, reunir ferramentas de verificacao, protecao, privacidade e acao, e "
    "usar cada uma no momento certo.\n"
    "\n"
    "Explore o mapa, encontre o Guia Digital Magico, colete categorias de defesa "
    "e enfrente os viloes. Para vencer, escolha respostas coerentes com cada "
    "ameaca, preserve sua integridade e neutralize todos os perigos antes que a "
    "cidade perca sua conexao."
)

CONCLUSION_TEXT = (
    "Voce explorou o mapa, enfrentou cada ameaca digital e completou o Guia Digital Magico.\n"
    "\n"
    "As paginas do guia agora guardam as pistas, os focos e os cuidados que ajudaram voce a escolher melhor em cada combate.\n"
    "\n"
    "Fora do jogo, continue como um Guardiao Digital: confirme fontes, proteja suas contas, desconfie da pressa e pense antes de clicar."
)

MAP_ROWS = len(WORLD_MAP_LAYOUT)
MAP_COLS = len(WORLD_MAP_LAYOUT[0])
MAP_WIDTH = MAP_COLS * TILE_SIZE
MAP_HEIGHT = MAP_ROWS * TILE_SIZE
MAP_OFFSET_X = (SCREEN_WIDTH - MAP_WIDTH) // 2
MAP_OFFSET_Y = (SCREEN_HEIGHT - MAP_HEIGHT) // 2

BATTLE_BUTTON_WIDTH = 330
BATTLE_BUTTON_HEIGHT = 54
BATTLE_BUTTON_LEFT_X = 110
BATTLE_BUTTON_MIDDLE_X = 475
BATTLE_BUTTON_RIGHT_X = 840
BATTLE_BUTTON_TOP_ROW_Y = 536
BATTLE_BUTTON_BOTTOM_ROW_Y = 620
BATTLE_FLEE_WIDTH = 76
BATTLE_FLEE_HEIGHT = 36
BATTLE_FLEE_GAP = 8
BATTLE_FLEE_X = SCREEN_WIDTH - 50 - BATTLE_FLEE_GAP - BATTLE_FLEE_WIDTH
BATTLE_FLEE_Y = 6
BATTLE_BACK_BUTTON_SIZE = 52
BATTLE_BACK_BUTTON_X = 42
BATTLE_BACK_BUTTON_Y = BATTLE_BUTTON_TOP_ROW_Y + 1

BATTLE_OPTION_RECTS = [
    pygame.Rect(BATTLE_BUTTON_LEFT_X, BATTLE_BUTTON_TOP_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
    pygame.Rect(BATTLE_BUTTON_MIDDLE_X, BATTLE_BUTTON_TOP_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
    pygame.Rect(BATTLE_BUTTON_RIGHT_X, BATTLE_BUTTON_TOP_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
    pygame.Rect(BATTLE_BUTTON_LEFT_X, BATTLE_BUTTON_BOTTOM_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
]

BATTLE_FLEE_RECT = pygame.Rect(
    BATTLE_FLEE_X,
    BATTLE_FLEE_Y,
    BATTLE_FLEE_WIDTH,
    BATTLE_FLEE_HEIGHT,
)
BATTLE_BACK_RECT = pygame.Rect(
    BATTLE_BACK_BUTTON_X,
    BATTLE_BACK_BUTTON_Y,
    BATTLE_BACK_BUTTON_SIZE,
    BATTLE_BACK_BUTTON_SIZE,
)
WARNING_PROCEED_RECT = pygame.Rect(420, 442, 200, 46)
WARNING_BACK_RECT = pygame.Rect(660, 442, 200, 46)

SUBATTACK_OPTION_RECTS = [
    pygame.Rect(BATTLE_BUTTON_LEFT_X, BATTLE_BUTTON_TOP_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
    pygame.Rect(BATTLE_BUTTON_MIDDLE_X, BATTLE_BUTTON_TOP_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
    pygame.Rect(BATTLE_BUTTON_RIGHT_X, BATTLE_BUTTON_TOP_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
    pygame.Rect(BATTLE_BUTTON_LEFT_X, BATTLE_BUTTON_BOTTOM_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
    pygame.Rect(BATTLE_BUTTON_MIDDLE_X, BATTLE_BUTTON_BOTTOM_ROW_Y, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT),
]

BOOK_HUD_RECT = pygame.Rect(SCREEN_WIDTH - 50, 6, 36, 36)
BOOK_CLOSE_RECT = pygame.Rect(SCREEN_WIDTH - 205, 612, 150, 42)
BOOK_PREV_RECT = pygame.Rect(355, 612, 150, 42)
BOOK_NEXT_RECT = pygame.Rect(775, 612, 150, 42)
BOOK_PAGE_SIZE = 2

VICTORY_MENU_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BATTLE_BUTTON_WIDTH - 20, 610, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT)
VICTORY_QUIT_RECT = pygame.Rect(SCREEN_WIDTH // 2 + 20, 610, BATTLE_BUTTON_WIDTH, BATTLE_BUTTON_HEIGHT)
DEFEAT_MENU_RECT = VICTORY_MENU_RECT.copy()
DEFEAT_QUIT_RECT = VICTORY_QUIT_RECT.copy()

ENCOUNTER_FIGHT_RECT = pygame.Rect(420, 456, 200, 46)
ENCOUNTER_FLEE_RECT = pygame.Rect(660, 456, 200, 46)

PAUSE_PANEL_RECT = pygame.Rect(440, 105, 400, 510)
PAUSE_CONTINUE_RECT = pygame.Rect(500, 190, 280, 50)
PAUSE_STORY_RECT = pygame.Rect(500, 255, 280, 50)
PAUSE_SETTINGS_RECT = pygame.Rect(500, 320, 280, 50)
PAUSE_MENU_RECT = pygame.Rect(500, 385, 280, 50)
PAUSE_QUIT_RECT = pygame.Rect(500, 450, 280, 50)
