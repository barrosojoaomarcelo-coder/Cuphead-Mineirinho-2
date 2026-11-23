# Atualização de dificuldade dos três chefes

> Registro da edição de 22/11/2026. Na main atual, o jogo chama-se Mineirinho, a ordem é Pirâmide → Comilão → Dragão e a velocidade base do pão é 1350 pixels/s nas três fases. A cadência e os padrões difíceis foram preservados. Use o README da raiz para instalar/jogar a versão atual; os números e pacotes abaixo documentam a edição anterior.

A correção parte da edição de três chefes do commit 306ffd40f7c3ec1b7661129f6eb481b51d301b36, na branch codex/fase-2-comilao. O dragão volta ao perfil do ZIP enviado: 480 pontos de vida, 12 tiros/s a 1450 pixels/s e os 160 valores de ataque originais. Comilão e Pirâmide continuam com 800 pontos e 20 tiros/s a 1800 pixels/s. Três vidas, avisos e faixas de fuga continuam disponíveis.

## Para jogar

Extraia Cuphead_Mineirinho_3_Fases_Dragao_ZIP.zip em uma pasta nova. Com Python instalado, abra INICIAR_WINDOWS.bat. Use os botões de treino para testar Comilão ou Pirâmide diretamente. O recorde da edição anterior é separado deste perfil; a preferência de som é mantida.

## Para atualizar uma cópia existente

As branches pessoais davi, moises e cajarelo recebem esta edição. O caminho recomendado é atualizar sua branch pelo Git, seguindo CONTRIBUTING.md. Se estiver usando a cópia do commit indicado acima fora desse fluxo, o ZIP Atualizacao_Dragao_ZIP_3_Fases contém arquivos/ e dragao-zip.patch; as imagens não mudaram.

1. Registrem o trabalho pendente com commit e confiram git status.
2. Criem uma branch com git switch -c feat/ajuste-dificuldade.
3. Na raiz do projeto, executem git apply --check CAMINHO/dragao-zip.patch.
4. Se a verificação passar, executem git apply CAMINHO/dragao-zip.patch. Se houver conflito, comparem os arquivos com o colega; não forcem nem substituam trabalho pendente.
5. Executem python -m unittest discover -s tests -q e joguem as três fases.
6. Enviem a branch e abram um pull request. Se a correção já estiver incorporada à branch compartilhada, tragam essa versão com merge em vez de aplicar novamente o patch.

Moisés revisa a dificuldade em config.py; Davi confere a leitura dos avisos e o som; João Marcelo confere instalação, menus e a sequência completa. Os detalhes da comparação e os limites dos testes estão em docs/DIFICULDADE_E_ANIMACAO.md e docs/VALIDACAO.md.
