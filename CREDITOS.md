# Créditos e referências

## Criadores de Mineirinho

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

## Novas artes do Comilão — 22/11/2026

Referência do personagem: Chefe Comilão, de Mineirinho, indicado pelo grupo. O grupo forneceu dois desenhos próprios de formas/ataques e uma captura como referência de cenário. Cuphead é referência de combate e apresentação.

assets/comilao-corpo.png, assets/comilao-boca.png e assets/vale-comilao.png foram gerados pela ferramenta de imagens integrada do Codex/ChatGPT, a partir dessas referências. Não são sprites oficiais extraídos dos jogos. Os prompts e a função de cada referência estão em docs/ARTES_COMILAO.md. Raios, língua e espinhos são desenhados pelo Pygame. A equipe deve conferir as regras da disciplina para declarar e usar esse material.

## Versão difícil e novas animações

Regras da fase 1 adaptadas de A_Fornalha_do_Castelo_Boss_Dificil.zip, fornecido pelo grupo em 22/11/2026; a autoria externa do conteúdo recebido deve ser confirmada pelo grupo. assets/comilao-corpo-animado.png e assets/comilao-boca-animada.png foram gerados pela ferramenta integrada de imagens do Codex/ChatGPT a partir das folhas anteriores. Prompts em docs/ARTES_COMILAO.md. Nenhum sprite oficial de Cuphead foi extraído. Efeitos de alongamento, compressão, rastros, estrelas e nuvem são desenhados pelo Pygame.

## Fase 3 — Olho da Pirâmide

Nome descritivo adotado para esta implementação. O grupo forneceu duas capturas do cenário/chefe, dois esboços de formas e ataques e uma imagem dos seres invocados. As seis artes novas em assets/piramide-*.png e assets/servo-*.png foram geradas pela ferramenta integrada de imagens do Codex/ChatGPT, usando essas referências e a arte do protagonista para manter o estilo. Os prompts estão em docs/ARTES_PIRAMIDE.md. Lasers e anéis são desenhados pelo Pygame. Não foram extraídos sprites oficiais dos jogos de referência.

## Áudio integrado e revisão — 23/11/2026

Os arquivos assets/audio/tema_mineirinho.ogg, dano_ai.ogg e pimentinha.ogg já estavam no commit 2b764c8 recebido da main. As fontes, cortes e hashes fornecidos estão em assets/audio/ORIGEM_DOS_AUDIOS.json. Esta revisão preserva esses arquivos e reduz somente a mixagem dos tiros/impactos antigos; não estabelece nova autoria nem licença dos áudios. A equipe deve completar a procedência e as permissões aplicáveis.
