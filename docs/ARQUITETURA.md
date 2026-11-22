# Arquitetura e acordo da equipe

## João Marcelo — main.py

initialize carrega o jogo. game_screen contém o loop. handle_event cuida da janela e dos comandos. read_controls monta um dicionário booleano. update_game avança a luta e o recorde. draw_screen apresenta a arena, ajustada à janela.

O dicionário ui guarda janela, relógio, tela de desenho, botões, preferências e referências ao jogo e aos recursos. O arquivo preferences.json fica na pasta de dados do usuário, fora do repositório. Para testes, FORNALHA_SAVE_DIR define outra pasta.

## Moisés — engine.py, sprites.py, attacks.py, comilao.py e config.py

GameModel cria o jogador, o chefe e seus grupos. Os grupos shots, fire e beams representam tiros, bolas de fogo e sopros. Os grupos chamam update nos seus sprites; a apresentação chama draw.

Player e Boss têm image para desenho, rect para posicionar a arte e hitbox para a colisão. A hitbox menor facilita esquivas. Bread e Fire saem dos grupos por kill quando expiram ou deixam a arena.

step recebe dt em segundos e controles left, right, up, down, jump, shoot e dash. Ele avança uma vez por quadro, limita pausas grandes a 0,05 segundo e coordena movimento, ataques e colisões. shots e fire usam groupcollide/spritecollide com a função hitboxes_overlap. Flame usa o teste pronto de linha contra retângulo do Pygame.

attacks.py guarda os nove padrões, seus avisos e os disparos agendados. Um aviso registra a direção; a bola gigante e o sopro não perseguem o jogador depois de anunciados.

Estados: title, story, intro, playing, transform, paused, dead e victory. story é a introdução narrativa; intro é a chamada curta antes de cada luta. As fases de ataque 1 e 2 usam o corpo do dragão; 3 e 4 usam a cabeça. Na fase do dragão, a transformação passa do dia para a noite. As duas transformações limpam ataques antigos.

Atenção aos dois números: stage_index seleciona o cenário (0 dragão, 1 Comilão); boss.phase seleciona o nível de ataque dentro de cada luta (1/2 corpo, 3/4 segunda forma). Não são a mesma coisa. start(índice) começa um cenário com três vidas, start_story abre a narrativa e next_stage só avança após uma vitória. A fase 3 ainda não tem implementação.

comilao.py contém Comilao (subclasse de Boss), EyeRay, Tongue e Spike. As regras chamam update_comilao somente no segundo cenário. Língua e raios usam Rect.clipline nos mesmos segmentos desenhados, com uma margem para a espessura; os espinhos usam hitbox. Os avisos registram os pontos antes do disparo e não seguem o jogador. draw_comilao_warning é a única função de apresentação específica deste módulo; Davi pode ajustá-la em acordo com Moisés.

## Davi — assets.py, scene.py e audio.py

load_assets devolve imagens, listas de quadros, manifesto e sons. load_sheet recorta spritesheets. player_pose escolhe o quadro de acordo com a ação do personagem. As classes de sprites pedem esses quadros para manter image e rect atualizados.

Renderer desenha cenário, grupos, avisos, partículas e interface. draw devolve nome -> pygame.Rect para os botões. main converte cliques da janela para coordenadas da arena.

Os sons são chamados diretamente por play_sound(assets, nome). audio.py carrega WAV e controla o volume. Não há callback, barramento de eventos, síntese de áudio em execução ou dependência de Node.js.

## Acordo para integrar

A arena é 1280 x 720, com chão em y=622. x/y do jogador indicam seus pés. Velocidades são pixels por segundo; os tempos são segundos. Mudanças em nomes públicos, controles, constantes e formatos dos avisos devem ser combinadas entre os responsáveis.

Moisés altera regras e caixas; Davi altera imagem, som e escolha de animações; João altera janelas, entradas e telas. Não reescrever a parte do colega para integrar uma tarefa sem conversar e revisar.

## Perfil difícil e animação

boss_attacks.py contém os 40 parâmetros por nível do perfil recebido em dicionários. attacks.py prepara, avisa e dispara dez famílias de ataques. Boss.move_mouth anima a altura das fileiras; clear_attacks limpa também a pose e todas as sequências pendentes. Fire.previous_center permite conferir o trajeto de projéteis rápidos por Rect.clipline. comilao.py usa a mesma lista scheduled para ondas de espinhos e avisos de golpes seguintes.

animation.py escolhe deformações visuais discretas e guarda imagens reaproveitáveis em assets["animated"], limitado a 256 entradas. Não há alteração da hitbox por efeito visual. As folhas do Comilão têm 12 quadros. O recorde salvo inclui ruleset para separar a versão difícil da anterior.

## Terceiro cenário

STAGES tem três entradas. Índice 2 seleciona o Olho da Pirâmide, cuja vida é compartilhada entre Piramide (corpo principal/direito) e PyramidSide (esquerdo, ativo somente após a transformação). boss.phase continua sendo um dos quatro níveis internos: 1/2 na primeira forma, 3/4 na segunda.

O grupo minions contém Servant; seus tiros recebidos não tiram vida do chefe. EnergyRing e PyramidLaser ficam em beams e implementam touches. clear_attacks limpa também criaturas e invocações pendentes. safe_floor_lanes calcula as marcas verdes usando os mesmos segmentos do ataque. O intervalo de tiro preserva a fração restante entre quadros para manter 20 disparos/s; a vida do chefe é atualizada por acerto até uma mudança de estado, evitando contar dano depois da vitória.
