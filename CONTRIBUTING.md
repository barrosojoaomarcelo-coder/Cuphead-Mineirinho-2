# Trabalhando em equipe no GitHub

## Publicar esta base

O ZIP contém uma pasta A_Fornalha_do_Castelo_Pygame_Aula. Copie **o conteúdo dela**, incluindo .github, .gitignore e .gitattributes, para a raiz da cópia local do repositório de vocês. main.py, README.md e requirements.txt devem aparecer diretamente na raiz do GitHub, sem uma pasta extra envolvendo o projeto.

Você pode clonar pelo GitHub Desktop ou pelo terminal:

~~~sh
git clone https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-.git
cd Cuphead-Mineirinho-
~~~

Depois de copiar os arquivos e testar, publique a base com uma mensagem que identifique a adaptação:

~~~sh
git add .
git commit -m "Simplifica base Pygame com sprites e sons WAV; adaptacao com IA"
git branch -M main
git push -u origin main
~~~

Se o repositório já tiver arquivos ou commits novos, preserve o trabalho existente e revise as diferenças antes de copiar. O envio requer acesso de colaborador. Não envie o ZIP inteiro como substituto do código: o professor precisa encontrar os arquivos e o histórico de desenvolvimento.

## Uma branch por tarefa

Cada integrante usa sua própria conta e identidade de autor no Git. Antes de começar:

~~~sh
git switch main
git pull origin main
git switch -c fix/descricao-da-tarefa
~~~

Exemplos: fix/ajustar-colisao (Moisés), feat/efeito-derrota (Davi), feat/retorno-menu (João).

Faça mudanças pequenas e completas, registre o resultado e envie sua branch:

~~~sh
git add .
git commit -m "Explica a mudanca e o comportamento corrigido"
git push -u origin fix/descricao-da-tarefa
~~~

Abra um pull request para main. Explique o problema, a solução e como testar; vincule a issue. O modelo de descrição já está em .github/pull_request_template.md.

## Revisão

- Davi revisa Moisés; João revisa Davi; Moisés revisa João.
- O revisor executa o jogo e confere o comportamento alterado.
- Só incorporem quando a versão continuar abrindo e os testes apropriados passarem.
- Combinem antes de mudar a interface entre engine, scene e main.
- Não deixem toda a integração para domingo à noite.

Se houver conflito, juntem as versões com o colega responsável pelo trecho. Não substituam o trabalho de outro integrante sem entender a diferença. Não reescrevam o histórico compartilhado nem criem commits artificiais para aparentar participação.

## Antes de abrir o pull request

~~~sh
python -m unittest discover -s tests -v
python main.py
~~~

Além dos testes automatizados, jogue uma partida com a mudança. Sons, dificuldade, clareza das animações e conforto dos controles precisam de avaliação humana.

## Contribuições e IA

A base foi adaptada com auxílio de IA. A divisão dos arquivos indica responsabilidades futuras. Registrem a origem dos trechos externos, as interações relevantes e as modificações de cada integrante em USO_DE_IA.md e nos próprios pull requests, conforme as regras da disciplina.
