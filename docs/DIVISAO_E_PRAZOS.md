# Divisão de trabalho — versão simplificada

Equipe: Davi, Moisés e João Marcelo. Entrega: segunda-feira, 23/11/2026, até 12h, horário de São Paulo. Meta interna: versão remota conferida até 10h.

## Moisés — regras e sprites

Arquivos: config.py, sprites.py, engine.py e attacks.py.

1. Estudar Bread.update, Player.update, GameModel.step e check_collisions.
2. Conferir pulo, dash, dano e os nove padrões nas duas formas.
3. Fazer melhorias e correções reais de jogabilidade, explicando o problema e o resultado no pull request.
4. Ao mudar uma regra, revisar os testes correspondentes.

Revisor: Davi. Alterações de hitbox ou posição devem ser combinadas com quem cuida das artes.

## Davi — artes, animação e som

Arquivos: assets.py, scene.py, audio.py, assets/player/, demais imagens e assets/sounds/.

1. Estudar load_assets, load_sheet, player_pose e o desenho da interface.
2. Conferir animações, leitura dos avisos, alinhamento do tiro e volume dos WAV.
3. Fazer uma melhoria visual ou sonora real e mostrar como verificar seu resultado.
4. Completar CREDITOS.md com a procedência das artes e de novos sons.

Revisor: João Marcelo. As escolhas de animação ficam em assets.py; as regras de movimento continuam com Moisés.

## João Marcelo — aplicação e entrega

Arquivos: main.py, requirements.txt, INICIAR_WINDOWS.bat, documentação e .github/.

1. Estudar initialize, game_screen, handle_event, update_game e draw_screen.
2. Conferir início, pausa, ajuda, reinício, tela cheia e cliques com a janela redimensionada.
3. Fazer uma melhoria real no fluxo ou corrigir um problema da instalação/interface.
4. Coordenar integração, gravação do vídeo e documentação final; cada colega corrige sua própria parte.

Revisor: Moisés.

## Etapas finais a partir de domingo, 22/11

| Momento | Resultado esperado |
| --- | --- |
| Primeira hora com o novo pacote | Os três conseguem jogar; a base é publicada identificando a adaptação com IA; cada um abre uma issue. |
| Antes da rodada final de domingo | Uma contribuição real de cada integrante integrada e revisada. |
| Domingo à noite | Encerrar novas funcionalidades; jogar nos três computadores; corrigir falhas; fechar créditos, README e vídeo. |
| Segunda, 8h–10h | Baixar uma cópia nova e executar usando apenas o README. |
| Segunda, 10h–11h | Conferir versão remota, acesso do professor, vídeo e link do Blackboard. |
| Segunda, 11h–12h | Margem para imprevistos na entrega. |

Não iniciar os chefes II e III nesse intervalo. Priorizar uma luta completa e estável.

## Checklist do grupo

- [ ] Instalação e jogo conferidos nos computadores reais.
- [ ] Vitória, derrota e reinício funcionando.
- [ ] Sons ouvidos e dificuldade avaliada com pessoas.
- [ ] Contribuições e revisões dos três registradas no Git.
- [ ] Todos entendem o caminho de uma tecla até a ação desenhada.
- [ ] README com integrantes, execução e vídeo acessível.
- [ ] Créditos das artes e registro/anexo de IA completados.
- [ ] Professor com acesso e link enviado no Blackboard.

A divisão acima é uma atribuição de responsabilidades futuras. A base simplificada foi preparada com auxílio de IA; não representa autoria individual anterior dos integrantes.
