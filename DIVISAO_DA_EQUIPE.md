# Divisão de trabalho — Davi, Moisés e João Marcelo

Entrega: segunda-feira, 23/11/2026, até 12h, horário de São Paulo. Esta divisão está também no README e, com prazos detalhados, em docs/DIVISAO_E_PRAZOS.md.

| Integrante | Branch pessoal existente | Área de responsabilidade | Arquivos principais |
| --- | --- | --- | --- |
| Moisés (@mguedesjr) | moises | Regras, dificuldade, movimento, tiros, colisões e ataques dos três chefes | config.py, sprites.py, engine.py, attacks.py, boss_attacks.py, comilao.py, piramide.py, piramide_attacks.py e testes das regras |
| Davi (@davimoreiraesteves-beep) | davi | Artes, animação, efeitos visuais, avisos e som | assets.py, animation.py, scene.py, audio.py e assets/ |
| João Marcelo (@barrosojoaomarcelo-coder) | cajarelo | Página inicial, introdução, entradas, passagem entre fases, instalação e entrega | main.py, INICIAR_WINDOWS.bat, requirements.txt e documentação |

## Tarefas de revisão desta versão

- Moisés: jogar as rajadas baixas/altas, as duas bolas gigantes e os combos do Comilão e as faixas de fuga da Pirâmide; ajustar os números em boss_attacks.py se necessário; manter os testes passando e explicar suas alterações.
- Davi: conferir as 12 poses de cada forma, o alinhamento do olho/língua, o tempo dos avisos e o volume; completar os créditos das artes recebidas e registrar suas melhorias.
- João Marcelo: testar menu → história → dragão → Comilão → Pirâmide → encerramento, treino direto, pausa, derrota e reinício; conferir instalação nos três computadores e coordenar vídeo/README/entrega.

Revisores: Davi revisa Moisés; João revisa Davi; Moisés revisa João. Cada um registra contribuições próprias reais. A base e as novas animações foram preparadas com auxílio de IA; a atribuição de responsabilidade não é declaração de autoria anterior.

## Como começar sem perder alterações

A versão nova está na branch codex/fase-2-comilao, no pedido de revisão #1. Após a revisão e a integração desse pedido à main, cada um atualiza a sua branch trazendo a main com merge, conforme CONTRIBUTING.md. Não usem force push nem substituam arquivos do colega para resolver um conflito. Se já há alterações locais, registrem e enviem antes de trocar de branch.

## Terceira fase

A terceira fase agora é o Olho da Pirâmide, com duas formas. Moisés revisa invocações, anéis, vida compartilhada e colisões dos cinco padrões de laser; Davi revisa poses, efeitos, cenário e leitura dos avisos; João revisa a passagem após o Comilão, o treino direto e o encerramento. Cada integrante deve jogar e registrar suas contribuições reais.
