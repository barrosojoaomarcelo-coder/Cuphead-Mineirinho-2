# Git em equipe — Cuphead-Mineirinho-2

Repositório atual: https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2. As branches existentes são main, moises, davi e cajarelo. A fase 2 foi preparada separadamente em codex/fase-2-comilao. Não misturem commits do repositório antigo.

## Baixar uma vez

~~~sh
git clone https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2.git
cd Cuphead-Mineirinho-2
python -m pip install -r requirements.txt
~~~

## Começar uma tarefa

Primeiro terminem e enviem as alterações pendentes da branch atual; git status mostra se há arquivos ainda não registrados. Cada integrante usa sua conta e identidade no Git.

~~~sh
git switch main
git pull origin main
git switch -c feat/descricao-da-tarefa
~~~

Exemplos: Moisés feat/comilao-equilibrio, Davi feat/comilao-animacoes, João feat/fluxo-entrega. As branches pessoais existentes podem continuar sendo usadas por quem já trabalha nelas; não apaguem alterações nem usem reset para tentar sincronizar. Uma nova branch por tarefa facilita revisar apenas aquela mudança.

## Testar e enviar

~~~sh
python -m unittest discover -s tests -v
python main.py
git status
git add nome-do-arquivo.py
git commit -m "Descreve a mudança e seu resultado"
git push -u origin feat/descricao-da-tarefa
~~~

Troquem os exemplos pelos nomes reais. Confiram o que git status mostra antes de adicionar arquivos. Não enviem .venv, senhas, arquivos de preferências, caches ou o ZIP como substituto do código.

## Juntar na main sem perder trabalho

1. No GitHub, abram um pull request da sua branch para main. Expliquem a mudança e como testar.
2. Davi revisa Moisés; João revisa Davi; Moisés revisa João. O revisor baixa a branch e executa o jogo.
3. Se a main mudou, tragam as alterações para sua branch: git fetch origin e depois git merge origin/main.
4. Havendo conflito, confiram os dois trechos com o colega responsável. Removam as marcações de conflito, preservem o comportamento das duas contribuições, testem e façam um novo commit.
5. Depois da revisão e dos testes, usem Merge pull request no GitHub. A integração soma o histórico. Não usem force push na main.
6. Todos voltam à main e executam git pull origin main antes da próxima tarefa.

Moisés altera regras/colisões; Davi imagens/som/desenho; João entradas/menus/entrega. Combinem antes de editar o mesmo arquivo. A base foi preparada com auxílio de IA; cada um deve registrar contribuições próprias reais em USO_DE_IA.md. O acesso de Davi ainda deve ser resolvido com João Marcelo, se o convite continuar pendente.
