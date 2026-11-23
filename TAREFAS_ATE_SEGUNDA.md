# Revisão e entrega até segunda-feira

Equipe: Moisés, Davi e João Marcelo. Prazo: **23/11/2026 até 12h**, horário de São Paulo. Todos os itens ficam pendentes até serem conferidos pelo responsável.

## Situação da base e das branches

A main recebida no commit 2b764c8 já contém as três fases, pimenta, pausa, controle e novos sons. A revisão de 23/11 ajusta Mineirinho, créditos de criadores, volume, tiros nas três fases e fluxo do menu. Ordem atual: introdução → Pirâmide → Comilão → Dragão → encerramento. Cada colega deve trazer a main aprovada para sua branch por merge, preservando seus commits; não substituir a pasta de trabalho.

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

- [ ] Testar menu → introdução → Pirâmide → Comilão → Dragão → encerramento; conferir treinos diretos das fases 2 e 3.
- [ ] Testar ajuda, pausa/retomada, perda de foco, derrota, reinício da fase atual, redimensionamento e fechamento.
- [ ] Conferir instalação nos computadores do grupo usando apenas o README/iniciador; corrigir instruções ou defeitos encontrados.
- [ ] Revisar a atualização atual da main e integrar correções dos colegas; testar um clone novo depois.
- [ ] Gravar/publicar vídeo curto do jogo funcionando e incluir endereço acessível no README; ele continua marcado como pendente na base examinada.
- [ ] Reunir o histórico/anexo de IA com os colegas e completar o link pendente em USO_DE_IA.md; cada pessoa registra suas alterações reais.
- [ ] Conferir acesso do professor e envio do endereço correto no Blackboard; verificar se proposta e acompanhamentos já foram enviados.
- [ ] Revisar Davi e pedir a revisão de Moisés sobre suas próprias correções.

Arquivos: main.py, requirements.txt, INICIAR_WINDOWS.bat, README e documentação. Cada colega continua responsável pelo conteúdo de sua parte.

## Agenda de fechamento

| Quando | Meta do grupo |
| --- | --- |
| Segunda, até 10h | Rodada de jogo nos três computadores; revisar sons, pimenta, controles e dificuldade |
| Segunda, 10h–11h | Correções necessárias integradas; clone novo, README, vídeo, fontes e histórico de IA conferidos |
| Segunda, 11h–12h | Conferir acesso e enviar o repositório antes do limite; reserva para imprevistos |
| Segunda, 12h–14h | Participação dos três na Feira de Jogos, conforme a agenda já registrada pelo grupo |

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
