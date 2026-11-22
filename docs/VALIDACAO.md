# Validação da versão simplificada

Data: 22/11/2026. Ambiente local: Windows, Python 3.12.14, Pygame 2.6.1 e SDL 2.28.4. Foram usados dispositivos virtuais do SDL para vídeo e áudio.

## Testes de comportamento

Comando: python -m unittest discover -s tests -v

Resultado: **36 testes aprovados**, sem falhas ou testes ignorados.

- 26 testes das regras e sprites: grupos reais do Pygame, movimento e limites, pulo variável e antecipado, dash, dano e vidas, pausa, cadência e origem dos tiros, mira, remoção de projéteis, colisões, transformação, vitória e nove padrões nos quatro níveis.
- 10 testes da aplicação: carregamento dos recursos e telas, início/pausa/reinício, ajuda, foco, redimensionamento/cliques, tela cheia, preferências, recorde e encerramento.

Além dos casos individuais, a suíte joga até a vitória em 30, 60 e 120 atualizações por segundo, com uma transformação e 360 acertos. Os testes de esquiva conferem pulo e dash no sopro baixo e permanência no chão/agachamento no sopro alto.

## Execução integrada e imagens

Um roteiro com main.update_game e main.draw_screen percorreu a luta com proteção prolongada apenas no teste. A vitória ocorreu com 360 acertos em aproximadamente 34,48 segundos no cronômetro da partida. Foram amostrados 544 quadros de desenho nessa execução.

Também foram renderizadas as 36 combinações de nove padrões x quatro níveis, além de menu, ajuda, pausa, derrota, vitória e transformação. O sopro foi exercitado com o jogador próximo ao chefe para conferir que sua imagem fica limitada ao tamanho da arena.

Foram inspecionadas imagens do menu, da segunda forma, do sopro e do leque. docs/preview.png é uma captura produzida pelo Pygame.

## Diferenças intencionais em relação à versão anterior

Esta edição usa uma atualização por quadro e colisões por pygame.Rect. Antes, o motor usava subpassos internos e alguns testes geométricos próprios de círculo/segmento. Os controles, os nove padrões, os parâmetros principais e o objetivo foram mantidos; não se promete uma simulação numericamente idêntica em cada quadro. As bordas das colisões e alguns instantes de movimento podem variar ligeiramente.

As antigas referências numéricas do JavaScript não foram apresentadas como testes desta versão. A suíte atual verifica comportamentos do jogo após a simplificação.

## Conferência do grupo antes da entrega

A execução virtual não substitui jogar com teclado físico, ouvir os volumes, avaliar a dificuldade com pessoas e testar a instalação no computador da apresentação. O iniciador Windows depende de Python disponível no computador; Python 3.12 é a versão recomendada e testada diretamente.

O fluxo do GitHub está preparado para Windows/Linux com Python 3.10 e 3.12, mas a execução remota só será confirmada depois da publicação. A validação local foi feita em Windows/Python 3.12. O pacote não foi publicado no GitHub nesta tarefa.
