# Auditoria direta do dragão difícil

> Registro da edição de 22/11/2026. Na main atual, o jogo chama-se Mineirinho, a ordem é Pirâmide → Comilão → Dragão e a velocidade base do pão é 1350 pixels/s nas três fases. A cadência e os padrões difíceis foram preservados. Use o README da raiz para instalar/jogar a versão atual; os números e pacotes abaixo documentam a edição anterior.

Referência fornecida pelo grupo: A_Fornalha_do_Castelo_Boss_Dificil.zip. SHA256: b801f875ff662d849b78f22306d08c87e96d80c01266fb7756274784ffd4249d. Comparação realizada em 22/11/2026.

Os quatro níveis de HARD_ATTACKS foram lidos diretamente da configuração do ZIP e comparados aos dicionários de boss_attacks.py: **160 valores comparados e nenhuma diferença**. Foram conferidos também a sequência dos padrões e o agendamento em engine.py/attacks.py.

| Regra | ZIP recebido e dragão desta edição |
| --- | --- |
| Vida do dragão | 480 acertos, dano 1 por pão |
| Arma | 12 tiros/s, velocidade 1450 pixels/s |
| Jogador | 3 vidas; movimento 310, gravidade 1850, salto 680 |
| Dash | velocidade 800, duração 0,21 s, recarga 0,55 s |
| Proteção após dano | 1,8 s |
| Transformação | 3,6 s; limpa ataques anteriores |
| Níveis internos | 75%, 50% e 25% da vida |
| Ataques | Dez famílias, limite 72 projéteis, fileiras e gigantes exclusivos |

A transformação agora reinicia pattern_index, breath_count e horizontal_count, como no ZIP. Assim, a alternância da primeira fileira na segunda forma não depende do número de ataques da primeira. Avisos, quantidades, velocidades e intervalos não foram reduzidos.

Comilão e Pirâmide continuam com seus perfis separados: 800 pontos de vida e 20 tiros/s a 1800 pixels/s. O perfil correto é reaplicado ao trocar de fase e ao reiniciar; ele não modifica as armas das outras lutas. Os recordes anteriores são separados desta edição.

## Limites da comparação

O ZIP usa dataclasses, colisão circular do fogo e subpassos a 120 Hz. A adaptação próxima da aula usa Sprites, Groups, dicionários e uma atualização por quadro, com colisão contínua entre a posição anterior e a atual dos projéteis. O retângulo de colisão pode ser mais rigoroso nas quinas. Não se promete reprodução numérica quadro a quadro nem a mesma sensação em todos os computadores. Os testes verificam as esquivas em 30/60/120 atualizações/s, com três vidas normais e sem proteção adicional nos casos de esquiva.

Igualar apenas duração aumentando a vida não reproduz todos os aspectos do combate. Nesta edição, a vida, a arma e os parâmetros de ataque do próprio dragão correspondem à referência enviada.
