# Como acrescentar a terceira fase

Esta atualização foi preparada para a versão difícil com Comilão do repositório Cuphead-Mineirinho-2, commit e6a50a641ec8695ac4b2df7c527809268f147042. Mantém dragão e Comilão antes da Pirâmide. Os dois levels pedidos são as duas formas da terceira luta.

Este guia descreve a primeira integração da fase 3. Se você já baixou a edição com três chefes e quer a correção que restaura a dificuldade, use COMO_ATUALIZAR_DIFICULDADE.md. A edição atual do jogo completo já tem essa correção e os três chefes com 800 pontos de vida.

## Opção mais simples: jogo completo

Extraia o pacote completo em uma pasta nova. Não copie por cima de uma pasta onde um colega esteja trabalhando. Abra INICIAR_WINDOWS.bat ou instale requirements.txt e execute python main.py. O botão TREINAR A FASE 3 e o comando python main.py --stage 3 abrem a luta diretamente.

## Atualização em uma cópia existente

O pacote de atualização contém somente arquivos novos ou alterados, mantendo os mesmos caminhos da raiz. Antes de copiar, registrem suas mudanças numa branch. Não substituam alterações do colega sem revisar.

1. Confiram git status e terminem o commit de alterações pendentes.
2. Criem uma branch: git switch -c feat/integrar-fase-3.
3. Comparem os arquivos da atualização com os locais. Se a base ainda é o commit indicado acima, copiem os arquivos da pasta arquivos/ para os mesmos caminhos da raiz do projeto.
4. Se alguém já mudou esses arquivos, usem o patch fase3.patch em vez de substituir tudo. Com uma cópia limpa da base, executem git apply --check CAMINHO/fase3.patch; somente se passar, executem git apply CAMINHO/fase3.patch. O patch inclui as imagens e preserva os caminhos. Se a verificação falhar, revisem as diferenças com o colega; não forcem a aplicação.
5. Executem python -m unittest discover -s tests -v e python main.py --stage 3.
6. Confiram também a sequência completa e abram um pull request.

## Pontos de integração no código

- piramide.py: Piramide, PyramidSide, Servant, EnergyRing e PyramidLaser. O segundo corpo usa a vida do primeiro; não há duas barras ou dois totais de vida.
- piramide_attacks.py: avisos, invocações, anéis e cinco famílias de laser. Os pontos do aviso são os mesmos usados no disparo.
- assets.py: carrega as seis imagens novas de assets/piramide-*.png e assets/servo-*.png. A pirâmide usa 4 colunas × 3 linhas; olhos e criaturas, 3 × 2.
- engine.py: acrescenta o cenário de índice 2 a STAGES, cria os dois corpos e o grupo minions, avança após o Comilão e atualiza colisões/limpeza.
- main.py: botão de treino da fase 3 e argumento --stage; identifica o novo perfil de recordes.
- scene.py: cenário roxo, avisos, criaturas, passagem após o Comilão e encerramento. A barra de vida dos chefes foi retirada.
- config.py e sprites.py: tiros a 20/s e 1800 pixels/s, preservando a cadência em 30/60/120 atualizações por segundo.

## Conferência jogando

Na primeira forma, destrua as criaturas e pule os anéis baixos; os altos passam sobre o personagem no chão. Na segunda, observe os traços e as faixas verdes antes do laser. Use A/D para mirar para o lado desejado; os dois olhos recebem dano. Ao perder metade da vida, o chefe se transforma e todos os ataques antigos somem. R repete esta fase com três vidas; a vitória final retorna ao menu por Enter.

Regras: Moisés. Artes/avisos: Davi. Menus/integração: João Marcelo. A base e as artes foram preparadas com auxílio de IA; registrem suas contribuições próprias.
