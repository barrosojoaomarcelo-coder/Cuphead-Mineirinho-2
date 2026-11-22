# Arquitetura e acordo da equipe

## João Marcelo — main.py

initialize carrega o jogo. game_screen contém o loop. handle_event cuida da janela e dos comandos. read_controls monta um dicionário booleano. update_game avança a luta e o recorde. draw_screen apresenta a arena, ajustada à janela.

O dicionário ui guarda janela, relógio, tela de desenho, botões, preferências e referências ao jogo e aos recursos. O arquivo preferences.json fica na pasta de dados do usuário, fora do repositório. Para testes, FORNALHA_SAVE_DIR define outra pasta.

## Moisés — engine.py, sprites.py, attacks.py e config.py

GameModel cria o jogador, o chefe e seus grupos. Os grupos shots, fire e beams representam tiros, bolas de fogo e sopros. Os grupos chamam update nos seus sprites; a apresentação chama draw.

Player e Boss têm image para desenho, rect para posicionar a arte e hitbox para a colisão. A hitbox menor facilita esquivas. Bread e Fire saem dos grupos por kill quando expiram ou deixam a arena.

step recebe dt em segundos e controles left, right, up, down, jump, shoot e dash. Ele avança uma vez por quadro, limita pausas grandes a 0,05 segundo e coordena movimento, ataques e colisões. shots e fire usam groupcollide/spritecollide com a função hitboxes_overlap. Flame usa o teste pronto de linha contra retângulo do Pygame.

attacks.py guarda os nove padrões, seus avisos e os disparos agendados. Um aviso registra a direção; a bola gigante e o sopro não perseguem o jogador depois de anunciados.

Estados: title, intro, playing, transform, paused, dead e victory. As fases de ataque 1 e 2 usam o corpo do dragão; 3 e 4 usam a cabeça. A transformação passa do dia para a noite e limpa ataques antigos.

## Davi — assets.py, scene.py e audio.py

load_assets devolve imagens, listas de quadros, manifesto e sons. load_sheet recorta spritesheets. player_pose escolhe o quadro de acordo com a ação do personagem. As classes de sprites pedem esses quadros para manter image e rect atualizados.

Renderer desenha cenário, grupos, avisos, partículas e interface. draw devolve nome -> pygame.Rect para os botões. main converte cliques da janela para coordenadas da arena.

Os sons são chamados diretamente por play_sound(assets, nome). audio.py carrega WAV e controla o volume. Não há callback, barramento de eventos, síntese de áudio em execução ou dependência de Node.js.

## Acordo para integrar

A arena é 1280 x 720, com chão em y=622. x/y do jogador indicam seus pés. Velocidades são pixels por segundo; os tempos são segundos. Mudanças em nomes públicos, controles, constantes e formatos dos avisos devem ser combinadas entre os responsáveis.

Moisés altera regras e caixas; Davi altera imagem, som e escolha de animações; João altera janelas, entradas e telas. Não reescrever a parte do colega para integrar uma tarefa sem conversar e revisar.
