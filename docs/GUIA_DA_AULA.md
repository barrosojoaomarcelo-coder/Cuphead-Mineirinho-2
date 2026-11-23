# Guia de leitura com o handout do professor

Referência: https://insper.github.io/DesignDeSoftware/pygame/handout/.

## Ordem para estudar

1. config.py: constantes que determinam tamanho, movimento e dificuldade.
2. main.py: leia initialize e game_screen para enxergar a estrutura geral.
3. assets.py: load_assets carrega os recursos em um dicionário.
4. sprites.py: veja primeiro Bread, depois Fire, Player, Boss e Flame.
5. engine.py: criação dos grupos, atualização, colisões, vida e estados.
6. attacks.py: comece pelo caso fan, depois leia os outros padrões.
7. comilao.py: compare os ataques e sprites da fase 2 com os do dragão.
8. scene.py e audio.py: desenho de interface e reprodução dos sons.

## Relação com o exemplo da aula

| No exemplo do professor | Nesta versão |
| --- | --- |
| pygame.init e janela | initialize em main.py |
| while game e clock.tick | game_screen em main.py |
| Tratamento de eventos | handle_event e handle_key |
| load_assets | assets.py |
| Classes de nave, meteoro e bala | Player, Boss, Bread, Fire e Flame |
| image e rect | Cada classe em sprites.py |
| all_sprites.update/draw | Grupos por tipo em engine.py e scene.py |
| Remover uma bala com kill | Bread.update e Fire.update |
| spritecollide e groupcollide | GameModel.check_collisions |
| pygame.mixer.Sound | audio.load_sounds |
| Estados do jogo | title, story, intro, playing, transform, paused, dead e victory |
| Separação por arquivos | main, config, assets, sprites, engine, attacks, comilao, scene e audio |

## Um quadro do jogo

Em game_screen:

1. Clock.tick limita a taxa a 60 quadros por segundo e informa o tempo decorrido.
2. O programa lê os eventos da janela e as teclas pressionadas.
3. update_game chama game.step.
4. Os grupos atualizam seus sprites, os ataques avançam e as colisões são verificadas.
5. draw_screen chama o desenho da arena e usa pygame.display.flip para apresentar o quadro.

flip atualiza a janela inteira; exerce aqui a função de apresentação que display.update tem nos exemplos do handout.

## image, rect e hitbox

image é a imagem desenhada. rect posiciona essa imagem. hitbox é outro pygame.Rect, menor, usado para colisões. Assim a transparência e a cauda das artes não tornam o combate injusto.

A função hitboxes_overlap apenas chama first.hitbox.colliderect(second.hitbox). Ela é passada ao Pygame para definir o teste usado por spritecollide/groupcollide. A estrutura é semelhante ao exemplo que passa collide_mask, mas aqui a colisão é retangular.

Não foram adotadas máscaras por pixel. A escolha de caixas menores preserva melhor a margem de esquiva do jogo. O caminho do sopro é uma linha espessa; Rect.clipline verifica se ela atravessa uma caixa ampliada do jogador, substituindo o algoritmo geométrico escrito à mão na versão anterior.

## Tempo e movimento

A posição usa x e y decimais; rect recebe os valores arredondados. Uma velocidade em pixels por segundo é multiplicada por dt. Isso mantém o movimento semelhante quando o número de quadros muda.

Há uma atualização por quadro, sem subpassos internos. O limite de 0,05 segundo evita um salto muito grande depois de uma travada. Como no handout, uma máquina muito lenta ainda prejudica a fluidez; é necessário testar no computador da feira.

## O que ainda vai além da aula

O jogo mantém trigonometria para mirar e fazer ondas, aceleração/gravidade para o salto, uma curta tolerância para pular perto do chão, spritesheets, persistência em JSON e ajuste da imagem ao tamanho da janela. Essas partes são necessárias para manter esta proposta de jogo e estão separadas em funções que podem ser estudadas individualmente.

Não é uma cópia literal do Asteroids do handout. É a mesma estrutura básica aplicada às lutas contra o dragão e o Comilão.

Na segunda fase, Comilao herda de Boss para reutilizar vida, temporizadores e a transformação. Tongue, EyeRay e Spike também são Sprites. Os dois primeiros usam Rect.clipline nos segmentos do ataque; os espinhos usam hitbox. stage_index escolhe o cenário; boss.phase é o nível de ataque dentro de uma luta.

## Simplificações desta edição

- Constantes de config substituem as dataclasses de configuração.
- Construtores normais de Sprite substituem Player/Boss como dataclasses.
- Grupos substituem listas de projéteis e a atualização central de seus movimentos.
- Sprite.kill substitui a marcação e filtragem de objetos mortos.
- O próprio Player encontra o indicador na animação; não existe callback.
- Sons são chamados diretamente; não existe fila de eventos do motor.
- Os WAV foram preparados antes da execução; não há síntese matemática de áudio no código do jogo.
- O loop está em game_screen; menus e controles estão em funções nomeadas.
- Expressões encadeadas foram expandidas em passos e if/elif.

## Perguntas para cada integrante

Moisés: como um tiro nasce, se move, colide e some? Por que um dash protege? Quando o chefe muda de forma?

Davi: como uma folha vira uma lista de quadros? Como o programa escolhe o quadro? Como substituir um WAV e ajustar seu volume?

João Marcelo: qual é a ordem do loop? Como um clique é convertido para a arena? O que pausa o jogo e onde o recorde é salvo?

Todos devem conseguir acompanhar o caminho inteiro de uma ação, mesmo quando o arquivo principal é responsabilidade de outro colega.

## Arquivos acrescentados no perfil difícil

boss_attacks.py usa tuplas e dicionários para os números do ZIP, sem dataclasses. animation.py usa Surface e transform.smoothscale para poses elásticas e guarda as imagens prontas em um dicionário limitado. O loop continua fazendo uma atualização por quadro. Na bola rápida, Rect.clipline verifica o caminho entre a posição anterior e a atual. A divisão em responsabilidades está também no arquivo DIVISAO_DA_EQUIPE.md, na raiz.

## Leitura da terceira fase

Leia primeiro Servant.update em piramide.py: posição, velocidade, escolha de quadro, image, rect, hitbox e kill. Depois veja PyramidLaser, que usa Rect.clipline em uma lista de segmentos. piramide_attacks.py prepara um dicionário de aviso e, ao vencer o prazo, cria os sprites. O grupo minions usa groupcollide contra os pães; a vida do chefe continua interna. A colisão do anel vazado usa a equação simples de uma elipse e é uma parte que vai além do handout. A integração completa está em COMO_INTEGRAR_FASE_3.md.

## Integrações posteriores — 23/11/2026

A main inclui também Pirâmide, pimenta, menu novo, pausa e controle. O componente poder_pimenta.py usa uma dataclass para suas regras; portanto, a simplificação das dataclasses descrita acima se refere ao motor original, não a todos os módulos atuais. Esses recursos exigem estudar também composição, objetos de configuração e entradas de joystick. O fluxo principal continua com eventos, atualização, desenho, Sprites e Groups. A ordem do menu é Pirâmide → Comilão → Dragão.
