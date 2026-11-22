# Validação — três chefes e terceira fase

Data: 22/11/2026. Windows, Python 3.12.14, Pygame 2.6.1 e dispositivos virtuais SDL.

## Resultado

python -m unittest discover -s tests -q

**79 testes aprovados**, sem falhas ou testes ignorados. Os 77 casos da edição de três chefes foram mantidos e foram acrescentados dois casos de pressão e alcance real das faixas de esquiva. As lutas completas também verificam que cada nível interno dura pelo menos 9,5 segundos com tiro contínuo e acertos reais.

Os tiros mantêm 20 disparos/s em 30/60/120 atualizações por segundo, com velocidade de 1800 pixels/s. Os testes conferem também a origem do tiro, o reinício do intervalo e o fim de uma luta com dois acertos simultâneos.

## Terceiro chefe

- Os dois olhos recebem tiros e descontam a mesma vida; o olho esquerdo não recebe dano na primeira forma.
- Serpentes/morcegos avançam na direção do jogador e podem ser destruídos; isso não desconta vida do chefe. O contato tira uma vida e respeita a proteção normal após dano.
- Os seis ataques da primeira forma recebem aviso antes do lançamento. O centro vazio dos anéis não causa dano.
- Anéis altos passam sobre o jogador no chão; os baixos permitem pulo em 30/60/120 atualizações por segundo, sem proteção adicional nos testes de esquiva.
- Cruzamento, losango, reflexão no chão e mira refletida têm faixas seguras verificadas nos níveis internos 3 e 4, em 30/60/120 atualizações por segundo. O raio horizontal baixo permite pulo e o alto passa sobre o jogador no chão.
- A mira refletida fica fixada no aviso; não segue o jogador depois. Cada raio atinge uma vez, e o dash protege.
- A transformação ocorre em metade da vida e limpa criaturas, anéis e invocações agendadas. A pausa congela tudo.
- O fluxo chega ao terceiro chefe após o Comilão, reinicia a fase atual e retorna ao menu após a vitória final. As três telas não exibem barra de vida de chefe.

As lutas completas dos três chefes chegam à vitória com 800 pontos de dano por pães reais, em 30/60/120 atualizações por segundo. Somente esses testes de fluxo usam proteção prolongada; não medem dificuldade humana. As regras difíceis do dragão continuam com os mesmos 40 parâmetros por nível do ZIP anterior. Foram comparados boss_attacks.py e attacks.py ao commit e6a50a6: nenhuma mudança.

## Recuperação da dificuldade

A 60 atualizações/s, contando transformação e viagem dos tiros, sem esquivas:

| Chefe | Versão difícil anterior (480 / 12 tiros/s) | Correção (800 / 20 tiros/s) |
| --- | --- | --- |
| Dragão | 44,483 s | 44,350 s |
| Comilão | 44,417 s | 44,283 s |
| Pirâmide | Ainda não existia | 45,217 s |

A medição isola o tempo mínimo do combate, com proteção apenas para o teste de fluxo. A pessoa que precisa parar de atirar para esquivar leva mais tempo. A edição inicial com três chefes tinha mantido 480 pontos apesar de aumentar o tiro para 20/s; esta correção compensa essa diferença. Os tiros continuam rápidos.

Sem proteção de teste, segurar tiro parado resulta em derrota nos três cenários, em 30/60/120 atualizações/s. As rotas de laser também foram verificadas com movimento real, partindo de cinco posições, nos dois níveis finais e nas três taxas. O controle espera 0,15 s antes de reagir e usa um dash inicial nas travessias maiores; a proteção desse dash já acabou quando o laser dispara. Não há reposicionamento durante essas esquivas. Os testes anteriores de pulo/agachamento, combos, anéis e corredores seguros continuam aprovados.

## Conferência visual

Foram inspecionados menu, pirâmide base, serpentes, anéis, dois olhos, losango, reflexão e encerramento. A prévia contém 188 quadros, aproximadamente 19 segundos, capturados do jogo. É uma demonstração de padrões: os ataques são selecionados e o personagem é reposicionado entre trechos para mostrar as faixas seguras; não representa uma partida humana completa. Não foi ativada proteção extra nessa captura.

Amostra de atualização e desenho durante a captura: média de 10,37 ms por quadro; percentil 95 de 17,87 ms. O vídeo virtual não garante a mesma taxa nos computadores do grupo.

## Entrega e limites

Os 79 testes também passaram no projeto extraído do ZIP final, usando Pygame 2.6.1. A integridade dos dois ZIPs foi conferida; o patch foi aplicado sobre uma cópia limpa do commit 524a9cc e seus arquivos foram comparados à entrega completa.

A entrega completa deve ser extraída em pasta nova e conferida com os testes. A atualização de dificuldade é relativa ao commit 524a9cc80b34899133aeef3842e0b811c7441554; consulte COMO_ATUALIZAR_DIFICULDADE.md antes de aplicar sobre trabalho de colegas. O patch permite verificar conflitos antes da aplicação e não exige baixar as artes outra vez.

O grupo ainda precisa jogar com teclado físico, avaliar dificuldade e volumes, testar instalação nos três computadores, gravar o vídeo de apresentação e concluir créditos/histórico de IA. A validação local não equivale a testes remotos ou integração à main.
