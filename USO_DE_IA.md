# Registro do uso de IA

## Escopo da base

Em 21/11/2026, Codex/ChatGPT foi usado para adaptar para Python/Pygame o ZIP HTML/JavaScript fornecido pelo grupo. Em 22/11/2026, a pedido do grupo, a base foi simplificada para aproximar sua organização do handout do professor.

Os arquivos Python distribuídos nesta edição foram gerados ou refatorados com auxílio de IA: main.py, config.py, sprites.py, engine.py, attacks.py, assets.py, scene.py, audio.py e tests/test_game.py. Também foram preparados com IA a documentação, o iniciador Windows, os modelos do GitHub e a configuração de testes. As imagens vieram do pacote recebido. Os WAV foram exportados dos sons sintetizados na adaptação anterior.

As alterações principais foram trocar dataclasses por construtores de Sprite, usar grupos e colisões do Pygame, remover a fila de eventos e a função de ligação do tiro, trocar síntese de áudio durante o jogo por WAV e colocar o loop principal em funções. A lógica foi separada por responsabilidade, mantendo a primeira luta.

A equipe deve revisar o material, entender suas decisões e registrar as contribuições posteriores. Os responsáveis indicados nos arquivos representam a divisão futura; não são uma declaração de autoria individual da base gerada.

## Histórico/anexo — pendente do grupo

Exportar ou disponibilizar esta conversa, incluindo os pedidos e os arquivos pertinentes, conforme as regras da disciplina. Este resumo não substitui o histórico. Conferir também as orientações institucionais sobre a ferramenta de IA autorizada.

Local ou link do histórico: **pendente de inclusão pelo grupo**.

## Próximas alterações

| Data | Integrante | Arquivos ou funções alterados | Uso de IA e revisão realizada | Histórico/anexo |
| --- | --- | --- | --- | --- |
| 22/11/2026 | Base preparada para o grupo | Simplificação descrita acima | Produzida com auxílio de Codex/ChatGPT; validação local em docs/VALIDACAO.md | Esta conversa; anexar |

Adicionar linhas com as contribuições reais. Descrever concretamente as funções geradas, compreendidas e modificadas; não inventar percentuais de autoria.

## Segunda fase — 22/11/2026

A pedido de Moisés, Codex/ChatGPT gerou comilao.py e tests/test_comilao.py, alterou engine.py, assets.py, scene.py, main.py e os testes da interface, e atualizou a documentação. Foram adicionadas a história, a passagem do dragão ao Comilão, treino direto, repetição da fase atual e uma barra de vida. As três imagens novas foram geradas pela ferramenta integrada de imagens a partir das referências do grupo (prompts em docs/ARTES_COMILAO.md). A terceira fase permanece pendente.

A base assistida não é apresentada como contribuição individual de Moisés, Davi ou João. Cada responsável deve revisar, compreender e registrar suas alterações reais. Validação: 47 testes locais aprovados, com os limites descritos em docs/VALIDACAO.md.

## Perfil difícil e animações — 22/11/2026

Codex/ChatGPT portou o perfil do ZIP difícil para boss_attacks.py/attacks.py e alterou sprites, engine, comilao, assets, scene e main. Acrescentou animation.py, testes de esquivas reais, divisão explícita na raiz e documentação do balanceamento. Duas novas folhas de 12 poses foram geradas pela ferramenta integrada de imagens. As esquivas de rajadas, gigantes, combos e chuva foram testadas sem proteção adicional. As lutas completas usam proteção somente nos testes de fluxo. Esta base continua sendo assistida por IA; cabe à equipe revisar e registrar suas contribuições reais.

## Terceiro chefe — 22/11/2026

Codex/ChatGPT implementou piramide.py e piramide_attacks.py, integrou três fases em engine/main/scene/assets, acrescentou testes e documentou a integração. Foram geradas seis artes pela ferramenta integrada de imagens a partir das referências do grupo. O jogo passou a usar 20 tiros/s a 1800 pixels/s e a ocultar a barra de vida dos chefes, conforme o pedido. A cadência mantém o restante do intervalo de tiro, e acertos simultâneos respeitam a transformação/vitória única. A equipe deve compreender e revisar o código e registrar as suas contribuições reais.

## Revisão da main — 23/11/2026

A pedido de Moisés, Codex revisou o commit 2b764c8, preservando a integração de pimenta, pausa, controle, sons e a ordem Pirâmide → Comilão → Dragão. Foram ajustados o nome para Mineirinho, o papel dos integrantes como criadores, a velocidade base dos tiros para 1350 pixels/s em todas as fases e os volumes de tiro/impacto. A introdução foi ligada ao novo menu e a conversão de cliques após redimensionar foi corrigida. Testes e documentação foram atualizados. Esta revisão não atribui contribuições individuais fictícias; o grupo deve revisar, compreender e registrar suas alterações e completar os anexos pendentes.
