# Créditos e referências

## Equipe

Davi, Moisés e João Marcelo.

## Inspiração

Cuphead, da Studio MDHR: https://cupheadgame.com/.

A referência indicada pelo grupo é a luta contra chefes, a combinação de tiros e esquivas e a apresentação cartunesca. Este é um projeto estudantil independente.

## Origem da base

A versão inicial foi adaptada de A_Fornalha_do_Castelo_codigo (3).zip, fornecido pelo grupo. O motor original estava em dist/engine.mjs, e a apresentação/entrada/som em dist/game.mjs. Esta edição simplifica a versão Python produzida anteriormente, preservando as artes e a primeira luta.

Referência de organização: handout de Pygame de Design de Software do Insper: https://insper.github.io/DesignDeSoftware/pygame/handout/. Foram usados os conceitos de sprites, grupos, carregamento de recursos e loop; não foi copiado o jogo Asteroids do tutorial.

## Recursos visuais — completar pelo grupo

| Recurso | Origem do arquivo recebido | Autoria, ferramenta, link ou licença a confirmar |
| --- | --- | --- |
| assets/player/*.webp | ZIP do grupo | Pendente |
| assets/dragon-base.webp e dragon-head.webp | ZIP do grupo | Pendente |
| assets/castle-day.webp e castle-night.webp | ZIP do grupo | Pendente |
| assets/bread.webp e protagonist.webp | ZIP do grupo | Pendente |

A procedência individual das artes não foi estabelecida pelo ZIP. O grupo deve registrar geração por IA ou fontes externas quando aplicável. Não foi atribuída uma licença geral ao material recebido.

## Áudio

Os 14 WAV em assets/sounds foram exportados dos efeitos e da pequena trilha sintetizada na adaptação Python anterior, produzida com auxílio de IA. Eles não foram extraídos de Cuphead. O código desta versão apenas os carrega por pygame.mixer.Sound e os reproduz. Davi pode substituir os arquivos mantendo os nomes, ajustando volumes e registrando as novas fontes.

## Bibliotecas e IA

Pygame 2.6.1: https://www.pygame.org/. A biblioteca é instalada por requirements.txt e não é distribuída dentro deste pacote.

A adaptação e a simplificação foram produzidas com auxílio de Codex/ChatGPT. O grupo deve completar o histórico e a declaração de uso em USO_DE_IA.md.
