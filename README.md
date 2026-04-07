# Guardi&atilde;o Digital 2: Exploracao e Combate aos Crimes Digitais

Este jogo foi desenvolvido para a disciplina de Computadores e Sociedade (ELC1076), no curso de Sistemas de Informacao da UFSM, usando Python + Pygame.

Agora o projeto possui uma base de exploracao em mapa, com movimentacao do personagem e encontros com viloes no caminho (estilo RPG classico).

## Como executar

```bash
py jogo.py
```

## Controles

- `WASD` ou `Setas` (segurando): mover livremente no mapa
- `Enter` ou clique: avancar telas e confirmar encontros
- `Esc`: sair da tela de encontro e voltar ao mapa
- `1`, `2`, `3`, `4` ou clique: responder no combate
- `F11`: alternar tela cheia

## Fluxo atual do jogo

1. Menu inicial
2. Tela de historia
3. Exploracao do mapa
4. Encontro com vilao ao tocar nele durante a exploracao
5. Combate em quiz (acerto derrota o vilao, erro reduz integridade)
6. Conclusao ao derrotar todos os viloes

## Base pronta para evolucao

A estrutura atual ja deixa pontos claros para expandir:

- novos mapas e layouts
- novos NPCs/viloes com comportamentos diferentes
- itens e inventario
- missoes secundarias
- sistemas de progressao e checkpoints

## Imagens

![menu](/assets/menu.png)

![screenshot](/assets/screenshot.png)
