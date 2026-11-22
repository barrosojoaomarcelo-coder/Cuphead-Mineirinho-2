# Divisão de trabalho — Davi, Moisés e João Marcelo

Entrega: segunda-feira, 23/11/2026, até 12h, horário de São Paulo. A lista para marcar a revisão está em [TAREFAS_ATE_SEGUNDA.md](TAREFAS_ATE_SEGUNDA.md); os marcos estão também em [docs/DIVISAO_E_PRAZOS.md](docs/DIVISAO_E_PRAZOS.md).

| Integrante | Branch pessoal | Responsabilidade | Arquivos principais |
| --- | --- | --- | --- |
| Moisés (@mguedesjr) | moises | Movimento, tiros, dano, colisões e dificuldade dos três chefes | config.py, sprites.py, engine.py, attacks.py, boss_attacks.py, comilao.py, piramide.py, piramide_attacks.py e testes |
| Davi (@davimoreiraesteves-beep) | davi | Artes, animações, efeitos, avisos e som | assets.py, animation.py, scene.py, audio.py, assets/ e CREDITOS.md |
| João Marcelo (@barrosojoaomarcelo-coder) | cajarelo | Menus, introdução, transições, instalação, integração e entrega | main.py, INICIAR_WINDOWS.bat, requirements.txt, README e documentação |

## Revisão de cada pessoa

- **Moisés:** comparar e jogar o dragão frente ao ZIP difícil recebido; conferir pulo/agachamento, gigantes e sopro; verificar combos do Comilão, anéis e lasers da Pirâmide. Conferir três vidas, dano dos tiros, transformação e reinício; corrigir falhas reais e manter os testes.
- **Davi:** conferir animações dos três chefes e do protagonista, origem dos tiros/raios/língua, clareza dos avisos e volumes. Completar a procedência das artes iniciais pendente nos créditos.
- **João Marcelo:** testar menu → introdução → Dragão → Comilão → Pirâmide → encerramento, treinos, ajuda, pausa, derrota e reinício. Conferir instalação nos computadores do grupo, vídeo e documentação; coordenar integração da versão aprovada à main.

Revisão cruzada planejada: Davi revisa Moisés; João revisa Davi; Moisés revisa João. Cada um registra correções, testes e revisões reais. A base e as artes assistidas por IA não são apresentadas como autoria individual anterior dos integrantes.

## Branches e entrega

Esta operação sincroniza moises, davi e cajarelo com a base de três fases. A main continua com o [pedido #1 aberto](https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2/pull/1) para revisão e integração coordenadas por João. **Atualizar as branches pessoais não conclui a entrega na main.**

Antes de baixar, confiram git status e registrem o trabalho pendente. Depois usem git switch NOME_DA_BRANCH e git pull --ff-only origin NOME_DA_BRANCH. Se houver divergência, revisem os históricos e façam fetch/merge conforme [CONTRIBUTING.md](CONTRIBUTING.md), sem force push ou reset.

Continuam por confirmar pelo grupo: revisão com teclado físico e sons; contribuições/revisões dos três; vídeo acessível; histórico/anexo de IA; procedência das artes iniciais; versão final na main e endereço correto no Blackboard. Nenhum desses itens é considerado concluído só por geração de código, testes automáticos ou sincronização de branches.
