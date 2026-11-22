# Divisão e prazos — três fases

Equipe: Davi, Moisés e João Marcelo. Entrega: segunda-feira, 23/11/2026, até 12h, horário de São Paulo. Metas internas: main testada até 10h e envio conferido até 11h.

Use [TAREFAS_ATE_SEGUNDA.md](../TAREFAS_ATE_SEGUNDA.md) como checklist principal, incluindo as referências oficiais verificadas e as pendências reais.

## Moisés — regras e sprites

Branch moises. Revisar Player.update, Bread.update, GameModel.step, colisões e mudança de forma em config.py, sprites.py, engine.py, attacks.py, boss_attacks.py, comilao.py, piramide.py, piramide_attacks.py e testes.

Comparar a fase do dragão com o ZIP difícil; jogar rajadas, gigantes e sopro. Testar combos do Comilão e criaturas, anéis e rotas de laser da Pirâmide. Corrigir falhas reais e explicar o resultado no PR; ao alterar uma regra, revisar os testes. Davi revisa. Combinar mudanças de hitbox/posição com Davi.

## Davi — artes, animação e som

Branch davi. Revisar load_assets, folhas de animação, desenho e reprodução dos sons em assets.py, animation.py, scene.py, audio.py e assets/.

Jogar as três fases observando avisos e correspondência entre desenho e perigo. Conferir emissões, volumes e vidas. Completar as fontes das artes iniciais em CREDITOS.md e registrar novos recursos. João revisa. Se o acesso de Davi ainda estiver pendente, João resolve o convite e Davi aceita.

## João Marcelo — aplicação e entrega

Branch cajarelo. Revisar initialize, handle_event, update_game e draw_screen em main.py; conferir requirements.txt, INICIAR_WINDOWS.bat, README e documentação.

Testar fluxo completo, treinos, ajuda, pausa, derrota, reinício, redimensionamento e encerramento. Coordenar correções aprovadas, revisão/integração do pedido #1 à main, vídeo e entrega. Moisés revisa; cada colega continua corrigindo sua própria parte.

## Marcos de hoje e amanhã

| Momento | Resultado esperado |
| --- | --- |
| Hoje, ao começar | Trabalho local registrado; cada um baixa sua branch pessoal atualizada e testa instalação |
| Hoje, antes da rodada final | Revisão cruzada e correções necessárias documentadas |
| Hoje à noite | Encerrar novas funcionalidades; jogar com teclado físico, ouvir sons; fechar vídeo, fontes e histórico de IA |
| Segunda, 8h–10h | Integrar versão aprovada e correções à main; testar um clone novo seguindo o README |
| Segunda, 10h–11h | Conferir acesso, vídeo, endereço no Blackboard e pendências de formulários |
| Segunda, 11h–12h | Reserva para imprevistos de entrega; evitar novas funcionalidades |
| Segunda, 12h–14h | Os três participam da Feira de Jogos |

Os horários intermediários são a organização do grupo. João coordena integração/documentação; Moisés confere regras; Davi confere mídia/créditos. Todos precisam executar, compreender e revisar a versão final.

## Atualizar sem perder trabalho

Esta operação distribui a base de três fases às branches pessoais. Antes de pull, executar git status e fazer commit do trabalho pendente. Depois trocar para a branch da própria pessoa e executar git pull --ff-only origin NOME. Se divergir, revisar os históricos, executar git fetch origin e fazer merge da branch correspondente; não usar force push ou reset. Veja os comandos em [CONTRIBUTING.md](../CONTRIBUTING.md).

A main permanece aguardando o pedido #1. João coordena sua revisão e integração antes do teste final e da entrega. Sincronização e testes automáticos não substituem revisão humana nem registram autoria individual da base assistida por IA.
