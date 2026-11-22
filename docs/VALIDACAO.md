# Validação — três chefes e terceira fase

Data: 22/11/2026. Windows, Python 3.12.14, Pygame 2.6.1 e dispositivos virtuais SDL.

## Resultado

python -m unittest discover -s tests -q

**77 testes aprovados**, sem falhas ou testes ignorados. Os 58 casos anteriores foram mantidos, com expectativas atualizadas para a existência da fase 3 e os tiros a 20/s; foram acrescentados 19 casos da Pirâmide e da integração.

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

As lutas completas dos três chefes chegam à vitória com 480 pontos de dano por pães reais, em 30/60/120 atualizações por segundo. Somente esses testes de fluxo usam proteção prolongada; não medem dificuldade humana. As regras difíceis do dragão continuam com os mesmos 40 parâmetros por nível do ZIP anterior.

## Conferência visual

Foram inspecionados menu, pirâmide base, serpentes, anéis, dois olhos, losango, reflexão e encerramento. A prévia contém 188 quadros, aproximadamente 19 segundos, capturados do jogo. É uma demonstração de padrões: os ataques são selecionados e o personagem é reposicionado entre trechos para mostrar as faixas seguras; não representa uma partida humana completa. Não foi ativada proteção extra nessa captura.

Amostra de atualização e desenho durante a captura: média de 10,37 ms por quadro; percentil 95 de 17,87 ms. O vídeo virtual não garante a mesma taxa nos computadores do grupo.

## Entrega e limites

Os 77 testes também passaram no projeto extraído do ZIP final, usando uma instalação nova do Pygame 2.6.1. A integridade dos dois ZIPs foi conferida; o patch binário foi aplicado sobre uma cópia limpa do commit anterior e seus arquivos foram comparados à entrega completa.

A entrega completa deve ser extraída em pasta nova e conferida com os testes. A atualização é relativa ao commit e6a50a641ec8695ac4b2df7c527809268f147042; consulte COMO_INTEGRAR_FASE_3.md antes de aplicar sobre trabalho de colegas. O patch inclui arquivos binários e permite verificar conflitos antes da aplicação.

O grupo ainda precisa jogar com teclado físico, avaliar dificuldade e volumes, testar instalação nos três computadores, gravar o vídeo de apresentação e concluir créditos/histórico de IA. A validação local não equivale a testes remotos ou integração à main.
