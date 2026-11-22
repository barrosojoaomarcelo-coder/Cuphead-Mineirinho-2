# Atualização de dificuldade dos três chefes

A correção parte da edição com três chefes, commit 524a9cc80b34899133aeef3842e0b811c7441554 da branch codex/fase-2-comilao. O dragão mantém todos os ataques da versão difícil anterior. Os três chefes passam de 480 para 800 acertos, compensando os tiros a 20/s; as lutas deixam de terminar cedo. Três vidas, controles, avisos e faixas de fuga continuam disponíveis.

## Para jogar

Extraia Cuphead_Mineirinho_3_Chefes_Dificil.zip em uma pasta nova. Com Python instalado, abra INICIAR_WINDOWS.bat. Use os botões de treino para testar Comilão ou Pirâmide diretamente. O recorde da edição anterior é separado deste perfil; a preferência de som é mantida.

## Para atualizar uma cópia existente

O ZIP Atualizacao_Dificuldade_3_Chefes contém arquivos/ com os caminhos originais e dificuldade.patch. Não é preciso baixar as imagens outra vez se a edição com três chefes já está completa.

1. Registrem o trabalho pendente com commit e confiram git status.
2. Criem uma branch com git switch -c feat/ajuste-dificuldade.
3. Na raiz do projeto, executem git apply --check CAMINHO/dificuldade.patch.
4. Se a verificação passar, executem git apply CAMINHO/dificuldade.patch. Se houver conflito, comparem os arquivos com o colega; não forcem nem substituam trabalho pendente.
5. Executem python -m unittest discover -s tests -q e joguem as três fases.
6. Enviem a branch e abram um pull request. Se a correção já estiver incorporada à branch compartilhada, tragam essa versão com merge em vez de aplicar novamente o patch.

Moisés revisa a dificuldade em config.py; Davi confere a leitura dos avisos e o som; João Marcelo confere instalação, menus e a sequência completa. Os detalhes da comparação e os limites dos testes estão em docs/DIFICULDADE_E_ANIMACAO.md e docs/VALIDACAO.md.
