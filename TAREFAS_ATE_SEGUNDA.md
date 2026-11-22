# Revisão e entrega até segunda-feira

Equipe: Moisés, Davi e João Marcelo. Prazo: **23/11/2026 até 12h**, horário de São Paulo. Todos os itens ficam pendentes até serem conferidos pelo responsável.

## Situação da base e das branches

O jogo reúne introdução, Dragão, Comilão, Pirâmide e encerramento. Esta operação distribui a base de três fases para moises, davi e cajarelo, preservando seus históricos. A main continua aguardando a revisão e integração do [pedido #1](https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2/pull/1). João coordena essa integração antes da entrega; os colegas revisam e testam.

Antes de baixar, executem git status e registrem com commit o trabalho pendente. Depois troquem para sua branch e usem git pull --ff-only origin NOME. Se divergir, revisem os históricos antes de fazer fetch/merge; não usem force push ou reset. Os comandos de cada pessoa estão em [CONTRIBUTING.md](CONTRIBUTING.md).

## Moisés — branch moises

- [ ] Comparar e jogar o dragão frente ao ZIP difícil: quantidade/velocidade dos ataques, avisos, gigantes, sopro, rajadas baixas/altas e transformação.
- [ ] Conferir três vidas, dano dos tiros, pulo, agachamento e dash nas três fases; verificar uma solução de esquiva para cada ataque.
- [ ] Jogar combos do Comilão; conferir criaturas, anéis, vida compartilhada e trajetos de laser da Pirâmide.
- [ ] Executar os testes; corrigir falhas reais e explicar causa, resultado e validação no PR.
- [ ] Explicar entrada → movimento/tiro → colisão → dano ao grupo; revisar as mudanças de João.

Arquivos: config.py, sprites.py, engine.py, attacks.py, boss_attacks.py, comilao.py, piramide.py, piramide_attacks.py e testes. Davi revisa as alterações de Moisés.

## Davi — branch davi

- [ ] Conferir animações e legibilidade: emissões dos tiros/raios/língua, criaturas, avisos e marcas de perigo.
- [ ] Ouvir trilha e efeitos no computador real, ajustar volumes se necessário e testar o botão de som.
- [ ] Conferir textos, avisos e vidas em janela menor e tela cheia; combinar mudanças de posição com Moisés.
- [ ] Completar CREDITOS.md: origem do jogador/protagonista, dragão, castelos e pão continua pendente na base examinada; registrar também recursos novos e ferramentas.
- [ ] Registrar defeitos e melhorias reais, com revisão de João; revisar as mudanças de Moisés.
- [ ] Se ainda faltar acesso, resolver o convite com João e aceitá-lo antes de enviar alterações.

Arquivos: assets.py, animation.py, scene.py, audio.py, assets/ e CREDITOS.md.

## João Marcelo — branch cajarelo

- [ ] Testar menu → introdução → Dragão → Comilão → Pirâmide → encerramento; conferir treinos diretos das fases 2 e 3.
- [ ] Testar ajuda, pausa/retomada, perda de foco, derrota, reinício da fase atual, redimensionamento e fechamento.
- [ ] Conferir instalação nos computadores do grupo usando apenas o README/iniciador; corrigir instruções ou defeitos encontrados.
- [ ] Coordenar revisão do pedido #1 e integração da versão aprovada e das correções à main; testar um clone novo depois.
- [ ] Gravar/publicar vídeo curto do jogo funcionando e incluir endereço acessível no README; ele continua marcado como pendente na base examinada.
- [ ] Reunir o histórico/anexo de IA com os colegas e completar o link pendente em USO_DE_IA.md; cada pessoa registra suas alterações reais.
- [ ] Conferir acesso do professor e envio do endereço correto no Blackboard; verificar se proposta e acompanhamentos já foram enviados.
- [ ] Revisar Davi e pedir a revisão de Moisés sobre suas próprias correções.

Arquivos: main.py, requirements.txt, INICIAR_WINDOWS.bat, README e documentação. Cada colega continua responsável pelo conteúdo de sua parte.

## Agenda de fechamento

| Quando | Meta do grupo |
| --- | --- |
| Hoje, primeira rodada | Cada pessoa baixa sua branch, executa o jogo e anota problemas da própria área |
| Hoje, antes da rodada final | Correções necessárias revisadas entre colegas; evitar ampliar o escopo |
| Hoje à noite | Jogar com teclado físico, ouvir sons e fechar vídeo, fontes e histórico de IA |
| Amanhã, 8h–10h | Main com versão aprovada; clone novo funciona seguindo apenas o README |
| Amanhã, 10h–11h | Conferir repositório, vídeo, acesso e entrega no Blackboard |
| Amanhã, 11h–12h | Reserva para imprevistos; concluir o envio antes do limite |
| Amanhã, 12h–14h | Os três participam da Feira de Jogos |

## Conferência conjunta

- [ ] A main contém as três fases aprovadas; não apenas as branches pessoais.
- [ ] Instalação, sons e dificuldade avaliados por pessoas nos computadores reais.
- [ ] Derrota, vitória, transformação, transição e reinício foram jogados e conferidos.
- [ ] Contribuições e revisões reais dos três estão registradas; a base gerada com IA está identificada.
- [ ] README, vídeo, fontes e histórico/anexo foram completados.
- [ ] O endereço entregue aponta para este repositório e o professor consegue acessá-lo.
- [ ] Todos conseguem explicar a lógica e suas decisões, incluindo o código assistido por IA.

## Referências verificadas

A [página oficial](https://insper.github.io/DesignDeSoftware/projeto/) confirma a entrega às 12h de 23/11 e a coleta do código no GitHub nesse horário. Pede endereço no Blackboard e README com identificação, execução e vídeo acessível. Também trata de créditos, declaração e histórico de IA, ferramenta institucional e compreensão do código. Conferir com o professor dúvidas sobre essas orientações. A Feira exige a presença da equipe.

O [handout](https://insper.github.io/DesignDeSoftware/pygame/handout/) é a referência para estudar loop, recursos, Sprites, Groups, colisões, sons, animações e estados. O projeto também espera aprender recursos além da aula. Três chefes são o escopo escolhido pelo grupo. A divisão, os testes propostos e os horários intermediários deste checklist são nossa organização de trabalho, não exigências adicionais do professor.

Páginas conferidas em 22/11/2026. Testes automáticos e sincronização de branches não comprovam que os itens humanos desta lista já foram concluídos.
