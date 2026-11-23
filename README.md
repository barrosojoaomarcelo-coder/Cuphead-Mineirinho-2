# Mineirinho

Jogo estudantil de ação lateral em **Python + Pygame**, inspirado nas lutas contra chefes de Cuphead e nos personagens de Mineirinho.

**Criadores: Davi, Moisés e João Marcelo.** A equipe desenvolve e revisa o projeto com auxílio de IA, conforme [USO_DE_IA.md](USO_DE_IA.md).

**Repositório:** [Cuphead-Mineirinho-2](https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2).

![Menu do Mineirinho](docs/preview.png)

**[Divisão da equipe, arquivos e branches](DIVISAO_DA_EQUIPE.md)** · [Como trabalhar com Git](CONTRIBUTING.md) · [Revisões para a entrega](TAREFAS_ATE_SEGUNDA.md)

## Como executar

Use Python 3.12, versão usada na validação local. Baixe ou clone o projeto inteiro, abra um terminal na pasta de main.py e execute:

```sh
python -m pip install -r requirements.txt
python main.py
```

No Windows, também pode abrir **INICIAR_WINDOWS.bat**. Ele cria .venv e instala o Pygame; precisa de internet na primeira instalação. O iniciador aceita Python 3.10 a 3.13 e prefere 3.12. Se seu comando for python3, substitua python por python3.

## Ordem da aventura

**Tela inicial → introdução → Pirâmide → Comilão → Dragão → encerramento.**

| Seleção no menu | Chefe e cenário | Formas e ataques |
| --- | --- | --- |
| 1 | Olho da Pirâmide, ruínas e lago roxo | Pirâmide com serpentes, morcegos e anéis; depois dois olhos com lasers horizontais, cruzados, em losango e refletidos |
| 2 | Chefe Comilão, vale rochoso | Corpo com raios e língua; depois boca gigante, combos e ondas de espinhos |
| 3 | Dragão Vermelho, castelo | Corpo com fogo variado; depois cabeça gigante e mudança do dia para a noite |

Selecione **1 e INICIAR JOGO** para jogar a campanha desde a introdução. Selecionar 2 ou 3 abre diretamente aquela fase para treino. Enter avança após uma vitória; ao vencer o dragão, volta ao menu. Cada fase começa com três vidas; R repete a fase atual. As duas formas pertencem à mesma luta.

## Tiros, dificuldade e pimenta

As três fases têm **velocidade base de tiro de 1350 pixels/s**, um pouco abaixo dos 1450 do dragão anterior. A cadência continua em 12 tiros/s no dragão e 20 tiros/s nos demais chefes. O dragão tem 480 pontos de vida internos; Comilão e Pirâmide têm 800. Não há barra de vida dos chefes: as formas e os ataques mostram a evolução.

Os padrões difíceis, avisos e espaços de esquiva foram preservados. O dragão continua com dez famílias de ataques e quatro níveis internos, baseados no ZIP difícil enviado pelo grupo. A auditoria do material original está em [AUDITORIA_DRAGAO_ZIP.md](docs/AUDITORIA_DRAGAO_ZIP.md); a velocidade do pão foi ajustada depois, a pedido do grupo.

A **pimenta** aparece após seis segundos de combate e fica disponível por cinco. Ao coletar, por oito segundos a cadência aumenta 1,5 vez e a velocidade aumenta 1,25 vez, para 1687,5 pixels/s. O dano não muda. Pausa e transformação congelam os temporizadores; morte, vitória, reinício e saída limpam o bônus. A próxima coleta aparece após 20 segundos.

## Controles

| Ação | Teclado |
| --- | --- |
| Mover | A / D ou setas |
| Pular | Espaço ou Z; segure para saltar mais alto |
| Atirar | J ou X; pode segurar |
| Mirar para cima / diagonal | W ou seta para cima; combine com A / D |
| Agachar | S ou seta para baixo |
| Dash / esquiva | Shift ou K |
| Pausar / voltar | P ou Esc |
| Reiniciar fase atual | R |
| Ativar / silenciar som | M |
| Selecionar fase no menu | Esquerda / direita ou 1 / 2 / 3 |
| Confirmar / avançar | Enter |
| Ajuda | H ou COMO JOGAR na pausa |
| Tela cheia | F11 |
| Sair | Fechar janela ou Esc na tela inicial |

A pausa oferece RETORNAR, REINICIAR, COMO JOGAR e MENU. A partida também pausa ao perder o foco da janela. Na seleção inicial, Enter com foco em uma fase primeiro foca INICIAR; confirme novamente para jogar.

Há suporte a controle: analógico esquerdo/direcional move; botão inferior pula/confirma; esquerdo ou RB/R1 atira; direito ou LB/L1 usa dash; superior mira para cima; Start/Options pausa. Conectar/desconectar é reconhecido durante o jogo; desconectar o controle ativo pausa a partida. Os mapas de controles genéricos ficam em controle.py. Não há modo multijogador ou controles de toque.

## Som e preferências

O tiro usa volume base de **8%**, o impacto de tiro 12% e os outros efeitos 40%. Música fica em 20% e baixa para 12% durante falas, que usam um canal reservado a 95%. Isso impede que a sequência de tiros corte as vozes. Os valores de mixagem ficam em config.py; o volume ouvido também depende dos arquivos e do computador.

Preferências e recorde ficam fora do código, na pasta de dados **Mineirinho** do usuário. A preferência de som da pasta antiga é lida se ainda não houver uma nova. O recorde usa uma identificação de regras diferente após a mudança da arma. MINEIRINHO_SAVE_DIR permite escolher outra pasta.

## Divisão do trabalho

| Criador / branch | Responsabilidade | Arquivos principais |
| --- | --- | --- |
| Moisés / moises | Movimento, colisões, ataques, dificuldade e integração da pimenta | config.py, sprites.py, engine.py, attacks.py, boss_attacks.py, comilao.py, piramide.py, piramide_attacks.py, poder_pimenta.py |
| Davi / davi | Recursos, animações, desenho e áudio | assets.py, animation.py, scene.py, audio.py, assets/, CREDITOS.md |
| João Marcelo / cajarelo | Janela, entradas, menus, instalação e integração | main.py, tela_inicial.py, pausa_menu.py, controle.py, requirements.txt, INICIAR_WINDOWS.bat, documentação |

**Davi fez a parte de som e animações, conforme informado pelo grupo em 23/11/2026.** Moisés acompanha regras, dificuldade e integrações; João Marcelo acompanha menus, ordem das fases e entrega. A base e as artes assistidas por IA estão discriminadas abaixo. Contribuições e evidências constam em [DIVISAO_DA_EQUIPE.md](DIVISAO_DA_EQUIPE.md); o fechamento por pessoa está em [TAREFAS_ATE_SEGUNDA.md](TAREFAS_ATE_SEGUNDA.md).

## Código e testes

O loop principal usa pygame.init(), Clock.tick(FPS), eventos, atualização e desenho. Imagens e sons são carregados uma vez. Os personagens e projéteis usam Sprites e Groups; colisões usam Rect e clipline. A estrutura principal está explicada em [ARQUITETURA.md](docs/ARQUITETURA.md) e [GUIA_DA_AULA.md](docs/GUIA_DA_AULA.md), com as partes que vão além do handout.

```sh
python -m unittest discover -s tests -v
```

Esses testes usam os chefes, sprites e recursos reais com dispositivos virtuais SDL. Os scripts antigos de qa usam dublês para testes isolados e devem rodar em processos separados. Resultados e limites em [VALIDACAO.md](docs/VALIDACAO.md).

Para abrir uma fase diretamente:

```sh
python main.py --stage 1
python main.py --stage 2
python main.py --stage 3
```

Os números seguem o menu: 1 Pirâmide, 2 Comilão, 3 Dragão. Para salvar uma imagem de abertura: python main.py --frames 5 --screenshot abertura.png.

## Apresentação e créditos

**Vídeo de apresentação pendente:** o grupo precisa gravar a versão final e incluir aqui um link acessível ao professor.

Inspiração: [Cuphead, da Studio MDHR](https://cupheadgame.com/), e Mineirinho. Não foram usados sprites oficiais de Cuphead. Artes recebidas, artes geradas com IA, sons e pendências de procedência estão em [CREDITOS.md](CREDITOS.md). Prompts das novas artes: [Comilão](docs/ARTES_COMILAO.md) e [Pirâmide](docs/ARTES_PIRAMIDE.md).

## Declaração de uso de IA

Uma parte substancial do código foi gerada, adaptada ou refatorada com auxílio de Codex/ChatGPT: motor e chefes em Python/Pygame, menus e integrações, testes e documentação. Novas artes do Comilão e da Pirâmide também foram geradas por IA a partir das referências do grupo. O uso por arquivo, a procedência dos recursos e os limites da validação estão em [USO_DE_IA.md](USO_DE_IA.md).

[Histórico completo informado pela equipe](https://chatgpt.com/share/e/6b0448e9-8114-83e9-8f44-5879332642e9) · [Anexo e confirmação de acesso do professor](ANEXO_IA.md).

Moisés confirmou que o histórico está completo e o professor tem acesso; a checagem automática encontrou uma tela de login. Os integrantes são responsáveis por compreender e revisar todo o material entregue e confirmar a orientação sobre ferramenta institucional. As fontes ainda pendentes estão em CREDITOS.md. Vídeo e testes em computadores reais continuam no checklist da equipe.
