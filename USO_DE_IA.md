# Registro de uso de IA — Mineirinho

Atualizado em 23/11/2026. Criadores: Davi, Moisés e João Marcelo.

## Declaração de escopo

Uma parte substancial do código deste projeto foi gerada, adaptada ou refatorada com auxílio de Codex/ChatGPT. O uso inclui a adaptação do jogo inicial de HTML/JavaScript para Python/Pygame, a organização em módulos, a implementação e integração dos chefes, recursos de interface, testes e documentação. As novas artes indicadas abaixo também tiveram geração por IA. A equipe definiu a proposta, enviou referências e pedidos de mecânica e é responsável por compreender, revisar e validar o resultado.

Não foi medido um percentual confiável de autoria humana/IA por função; não se atribuem percentuais inventados. A divisão entre integrantes descreve áreas de contribuição e revisão, e não transforma a base gerada por IA em código originalmente escrito por uma única pessoa.

## Fonte e histórico completo

- Ferramentas registradas: Codex/ChatGPT e geração de imagens integrada ao ambiente.
- [Histórico completo informado pelo grupo](https://chatgpt.com/share/e/6b0448e9-8114-83e9-8f44-5879332642e9).
- [Anexo de IA: índice do histórico e confirmação de acesso](ANEXO_IA.md).

Moisés confirmou, em 23/11/2026, que o link contém o histórico completo utilizado e que o professor tem acesso. Na checagem automática, o endereço apresentou uma tela de login; seu conteúdo não foi lido independentemente nesta revisão. A confirmação de completude e acesso é uma declaração da equipe. O anexo contém o endereço do histórico, não uma transcrição reconstruída ou inventada.

O grupo deve confirmar a adequação das ferramentas utilizadas à orientação sobre IA institucional da [página do projeto](https://insper.github.io/DesignDeSoftware/projeto/#plugins-de-ia-generativa-iag). Registrar o histórico e dar acesso ao professor não substitui essa orientação.

## Materiais e uso realizado

| Material | Como a IA foi usada | Papel no jogo e revisão necessária |
| --- | --- | --- |
| main.py, config.py, engine.py, sprites.py, attacks.py, boss_attacks.py | Adaptação/refatoração do motor e integração das regras solicitadas pelo grupo | Janela, estados, movimento, tiros, colisões e perfil difícil do dragão; a equipe precisa explicar o fluxo completo |
| comilao.py, piramide.py, piramide_attacks.py | Implementação assistida a partir das referências e esboços fornecidos | Formas, criaturas, língua, anéis e lasers; conferir avisos, trajetos e esquivas |
| assets.py, animation.py, scene.py, audio.py | Geração/refatoração de carregamento, animação, desenho e reprodução de áudio | Reutilizar recursos carregados, desenhar sem alterar a lógica e reservar canais de música/voz |
| tela_inicial.py, pausa_menu.py, controle.py, poder_pimenta.py | Recursos assistidos por IA recebidos na main e integrados ao motor | Menu, pausa, joystick e bônus temporário; fontes adicionais estão no histórico informado |
| tests/, qa/ | Geração e atualização de verificações automatizadas | tests usa chefes/recursos reais; qa inclui dublês e deve rodar separadamente; limites em docs/VALIDACAO.md |
| README, demais documentos, INICIAR_WINDOWS.bat e configuração do projeto | Preparação e revisão assistidas | Explicações, instruções de execução, divisão, créditos e checklist; a equipe confirma informações pessoais e de entrega |
| Novas artes do Comilão e da Pirâmide | Geração de imagens a partir de esboços, capturas e protagonista fornecidos pelo grupo | Prompts e recursos em docs/ARTES_COMILAO.md e docs/ARTES_PIRAMIDE.md |
| WAV de assets/sounds | Exportados da síntese produzida na adaptação anterior assistida por IA | Efeitos/trilha antigos; não são sons extraídos de Cuphead |
| OGG de assets/audio e mídia embutida do menu | Integração de recursos recebidos; fontes/cortes registrados no projeto | Consultar assets/audio/ORIGEM_DOS_AUDIOS.json e CREDITOS.md; não se presume autoria ou licença externa |
| Artes iniciais do ZIP do grupo | Recebidas como base; ferramenta e autoria originais não foram estabelecidas por esta revisão | Completar a procedência pendente em CREDITOS.md |

## Participação da equipe

| Integrante | Contribuição ou evidência registrada | Conferência final |
| --- | --- | --- |
| Moisés | Definições e pedidos de mecânica/dificuldade; integração de som/interface registrada no commit 2b764c8; acompanhamento da adaptação assistida | Regras, colisões, vidas, esquivas e conformidade do registro de IA |
| Davi | Som e animações, conforme declaração do grupo por Moisés em 23/11/2026 | Conferir o resultado nos computadores reais e identificar arquivos, fontes e evidências do trabalho feito |
| João Marcelo | Ajustes de menu e ordem dos chefes registrados nos commits a40d6d9, 1e11577 e 863115e | Execução, vídeo, documentação e envio da versão final |

A contribuição declarada de Davi é registrada sem atribuir a ele commits feitos por outra conta ou autoria exclusiva das artes/código gerados por IA. Os arquivos relacionados à sua área incluem audio.py, animation.py, assets.py, scene.py e assets/. Evidências adicionais reais podem ser acrescentadas pelo grupo.

## Cronologia resumida

| Data | Etapa |
| --- | --- |
| 21/11/2026 | Adaptação assistida do ZIP HTML/JavaScript para Python/Pygame |
| 22/11/2026 | Simplificação do motor para Sprites/Groups, Comilão, dificuldade do dragão, animações e implementação da Pirâmide |
| 23/11/2026 | Main com ordem Pirâmide → Comilão → Dragão, som/voz, menu, pausa, controle e pimenta; revisão do nome Mineirinho, créditos, velocidade e volume dos tiros |
| 23/11/2026 | Revisão documental: 75 docstrings acrescentadas, instruções antigas de integração corrigidas, histórico de IA organizado e contribuição de Davi registrada conforme informação do grupo |

A referência à Pirâmide como terceira fase nos documentos históricos descreve sua criação. A ordem atual do menu é Pirâmide → Comilão → Dragão. O jogo atual tem três fases completas e não exibe barra de vida dos chefes.

## Verificação e responsabilidade

A versão de jogo anterior a esta revisão documental passou por 85 testes automatizados com os chefes e recursos reais, também no ZIP extraído. A revisão de docstrings foi comparada por análise da estrutura Python para preservar a execução; os resultados atualizados ficam em docs/VALIDACAO.md. Testes com dispositivos virtuais não certificam instalação, som ouvido, controle físico ou dificuldade humana nos computadores do grupo.

Os três integrantes devem compreender o código entregue, inclusive os trechos assistidos por IA. Revisão humana, contribuições reais, vídeo e confirmações no Blackboard estão discriminados em TAREFAS_ATE_SEGUNDA.md.
