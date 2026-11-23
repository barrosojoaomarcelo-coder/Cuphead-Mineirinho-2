# Validação de Mineirinho — revisão da main

Data: 23/11/2026. Base recebida: commit 2b764c84693e205b7bc2d8d764516baeca2185a6.
Ambiente: Windows, Python 3.12.14, Pygame 2.6.1, vídeo e áudio virtuais SDL.

## Revisão documental de 23/11/2026

Base desta revisão: cee1c1b6aa155669217a26f4905d9732647fcfef. Foram acrescentadas 75 docstrings em 13 módulos, corrigidas instruções antigas sobre a main e organizados o registro de contribuições e o anexo de IA. O grupo confirmou que o histórico informado está completo e o professor tem acesso; a checagem automática do link encontrou uma tela de login.

Os 17 módulos Python da raiz foram comparados por árvore de sintaxe, desconsiderando apenas docstrings: a estrutura de execução permaneceu idêntica à base. Os links locais dos documentos revisados foram conferidos sem arquivos ausentes. Depois das alterações, os mesmos **85 testes passaram novamente**, em 27,270 segundos, sem falhas ou testes ignorados. Não são 85 testes adicionais; é a repetição da suíte existente. As verificações de qa descritas abaixo pertencem à rodada anterior e não foram repetidas nesta revisão de documentação.

## Resultado

Comando: python -m unittest discover -s tests -q

**85 testes aprovados, sem falhas ou testes ignorados**, em aproximadamente 41 segundos. São os 81 casos da base, atualizados para a interface/ordem atuais, e quatro regressões da revisão. Os testes desta pasta usam os sprites, chefes, artes e sons reais do repositório.

Foram conferidos:

- Fluxo menu → introdução → Pirâmide → Comilão → Dragão → encerramento. Nomes, próxima luta e créditos correspondem à tela exibida.
- Seleção das três fases com mouse em janelas 960×540, 1000×800 e 1600×600, incluindo margens fora da imagem. Ajuda, pausa, reinício, perda de foco, tela cheia e saída.
- Velocidade base de 1350 pixels/s nas três fases, cadência de 12/s no dragão e 20/s nos outros chefes, em 30/60/120 atualizações por segundo. Vida interna: 480 no dragão e 800 nos demais.
- Coleta real da pimenta nas três lutas, velocidade temporária de 1687,5, congelamento na pausa, expiração e reinício para 1350 com três vidas.
- Volumes carregados de tiro 8%, impacto 12% e salto 40%, com tolerância da quantização do mixer. Uma sequência de 30 pedidos de tiro preserva música e voz nos canais reservados. Silenciar interrompe a voz pendente; reativar mantém os ganhos menores.
- Colisões, dano único, três vidas, proteção após dano, dash, mudanças de forma, limpeza de ataques e vitória com projéteis reais.
- Ataques difíceis do dragão, combos/espinhos do Comilão e criaturas/anéis/lasers da Pirâmide, incluindo pulo, agachamento e corredores de fuga em 30/60/120 atualizações por segundo.
- Sem faixas superior/inferior ou barra de vida dos chefes durante a luta; somente corações do jogador.

Os testes de luta completa usam proteção prolongada apenas para conferir dano e progressão. Os testes de esquiva usam as regras normais; as rotas maiores usam o dash normal, cuja proteção termina antes do disparo do laser. Isso verifica saídas possíveis em padrões específicos, não equivale a uma campanha vencida por uma pessoa.

## Verificações isoladas de qa

Executados separadamente: qa/test_controle.py (9 testes), qa/test_engine_pimenta.py (4 testes), qa/test_scene_integrada.py e qa/test_integracao_completa.py (scripts de asserções, ambos aprovados).

Esses arquivos são anteriores à revisão e usam dublês em partes do controle, sprites, chefes ou recursos para isolar componentes. Não devem ser importados junto com a suíte real, pois substituem módulos em sys.modules. Seus resultados não foram somados aos 85 testes reais nem usados como prova de dificuldade das lutas.

## Conferência visual

Capturas geradas pelo jogo real: tela inicial, introdução narrativa, introduções e resultados dos três chefes, arena, pausa e ajuda. Inspeção do menu e encerramento confirmou Mineirinho e “Criadores: Davi, Moisés e João Marcelo”; a introdução corresponde à ordem atual. A imagem docs/preview.png foi substituída pelo menu atual.

As capturas foram preparadas para mostrar cada tela; elas não representam uma partida humana completa. Nenhum sprite ou arquivo de áudio foi substituído nesta revisão.

## Diferenças para a validação de 22/11

A main recebida acrescentou sons, pimenta, pausa, controle e a ordem Pirâmide → Comilão → Dragão. A revisão atual reduz o tiro de 1450 no dragão e 1800 nos demais para 1350, mantendo cadência, vida e padrões. Os relatórios de 22/11 registram o perfil anterior e não descrevem a velocidade atual. O nome antigo só permanece em referências a arquivos recebidos e na leitura de preferências antigas por compatibilidade.

## Limites e pendências

A verificação usa dispositivos virtuais: o grupo deve ouvir a mixagem e testar teclado/controle físicos nos três computadores. A dificuldade humana, instalação local dos colegas e desempenho na máquina da feira ainda precisam de conferência. Vídeo de apresentação, fontes pendentes, adequação das ferramentas de IA à orientação institucional e envio no Blackboard continuam na lista do grupo. O anexo de IA já referencia o histórico informado e a confirmação de acesso do professor. Pendências por pessoa em TAREFAS_ATE_SEGUNDA.md.
