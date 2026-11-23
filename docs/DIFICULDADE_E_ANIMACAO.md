# Dificuldade e animação

> Registro da edição de 22/11/2026. Na main atual, o jogo chama-se Mineirinho, a ordem é Pirâmide → Comilão → Dragão e a velocidade base do pão é 1350 pixels/s nas três fases. A cadência e os padrões difíceis foram preservados. Use o README da raiz para instalar/jogar a versão atual; os números e pacotes abaixo documentam a edição anterior.

## Fase 1 recebida no ZIP

O pacote A_Fornalha_do_Castelo_Boss_Dificil.zip usa outro motor, com dataclasses e subdivisão do tempo. Para manter a organização próxima da aula, foram portadas suas regras de ataque para Sprites, Groups, listas e dicionários do projeto atual. Nenhuma fase foi substituída por uma tela vazia.

Os quatro dicionários HARD_ATTACKS em boss_attacks.py reproduzem exatamente os 40 parâmetros por nível do ZIP. O dragão usa também sua vida e arma originais: 480 pontos, 12 tiros/s a 1450 pixels/s. Comilão e Pirâmide usam 800 pontos e 20 tiros/s a 1800 pixels/s. Três vidas, velocidade do jogador 310, salto 680 e dash de 0,21 segundo foram preservados.

A conferência direta do ZIP comparou 160 valores de ataque, sem diferenças, e identificou o reinício de horizontal_count na transformação, agora corrigido. A duração de fluxo do dragão nesta edição é 44,467 s a 60/120 atualizações/s e 44,500 s a 30. A proteção usada nessa medição serve somente para isolar duração e progressão; não mede dificuldade humana. A cadência mantém 12/s em 30/60/120, sem tornar a arma dependente do computador. Consulte AUDITORIA_DRAGAO_ZIP.md para os limites da equivalência entre os motores.

| Parâmetro | Nível 1 | Nível 2 | Nível 3 | Nível 4 |
| --- | --- | --- | --- | --- |
| Velocidade normal | 440 | 490 | 550 | 610 |
| Intervalo entre padrões | 1,95 s | 1,80 s | 1,65 s | 1,50 s |
| Aviso normal | 0,80 s | 0,76 s | 0,72 s | 0,68 s |
| Velocidade horizontal | 700 | 760 | 840 | 920 |
| Fileiras horizontais | 2 | 2 | 3 | 4 |
| Tiros por fileira | 4 | 5 | 5 | 6 |
| Velocidade da bola gigante | 720 | 800 | 860 | 920 |
| Bolas gigantes | 1 | 1 | 2 | 2 |

O dragão abaixa a boca até a altura anunciada. Fileiras baixas pedem pulo; altas pedem agachamento. A boca se move gradualmente entre as fileiras. O sopro, as bolas gigantes e as fileiras não se misturam com outros padrões; uma segunda bola agendada continua bloqueando novos padrões. A chuva mantém a faixa segura entre ondas. O limite é de 72 projéteis simultâneos.

O projeto continua com uma atualização por quadro, em vez do motor com subpassos do ZIP. Para que uma bola rápida não atravesse o jogador entre dois quadros, a colisão verifica também a linha entre a posição anterior e a atual, com Rect.clipline. A adaptação não promete equivalência numérica quadro a quadro com o motor do ZIP.

## Comilão reforçado

O Comilão usa 800 pontos para acompanhar a duração do dragão com os tiros rápidos. Os avisos diminuem de 1,0 s para 0,78 s ao longo da luta; os intervalos, de 2,55 s para 1,95 s. Os combos acrescentam um novo aviso de pelo menos 0,72 s antes de cada golpe. A língua estica em 0,19 s; os raios passam de três para até cinco. A segunda forma dispara duas ou três ondas de espinhos a até 500 pixels/s, preservando o mesmo corredor anunciado.

## Pirâmide e condições de esquiva

A Pirâmide também tem 800 pontos, compartilhados pelos dois olhos. As duas formas e os quatro níveis internos continuam nos limites de 75%, 50% e 25% da vida. Todos os padrões mantêm aviso; os raios usam os mesmos caminhos anunciados e não perseguem o jogador depois de disparar. Na transformação, os ataques antigos desaparecem. Os lasers finais não se sobrepõem.

Além dos testes de pulo/agachamento do dragão e do Comilão, as faixas de fuga dos lasers foram alcançadas com movimento e um dash quando necessário, partindo de cinco posições, em ambos os níveis finais e em 30/60/120 atualizações/s. Foram reservados 0,15 s para reação; o dash ocorre antes do disparo, sem sua proteção cobrir o raio. Segurar tiro parado leva à derrota nas três fases. Esses testes verificam pressão e saídas possíveis; a avaliação com jogadores continua necessária.

## Apresentação cartunesca

As duas folhas novas têm 4 colunas × 3 linhas, com 12 poses distintas por forma. A animação percorre repouso/piscada, preparação, disparo e recuperação em ritmos diferentes. A seleção está em Comilao.refresh_image. animation.py guarda versões comprimidas e alongadas das poses do jogador/dragão e flashes de impacto. As caixas de colisão não mudam devido à deformação visual. O desenho usa rastros no dash, estrelas nos impactos e nuvem na transformação.

Imagens novas geradas com a ferramenta integrada de imagens do Codex/ChatGPT a partir das artes anteriores, por solicitação do grupo. Prompts em ARTES_COMILAO.md. Não são animações oficiais de Cuphead. A referência está nos princípios de preparação, exagero e recuperação do movimento.

Testem o conforto da dificuldade com pessoas e teclado físico antes de entregar. Ajustes de dificuldade ficam com Moisés; arte/tempo visual com Davi; fluxo e integração com João Marcelo.
