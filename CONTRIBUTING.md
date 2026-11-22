# Git em equipe — Cuphead-Mineirinho-2

Repositório: https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2.

Esta operação distribui a base com três fases para as branches pessoais moises, davi e cajarelo, preservando seus históricos. A main continua aguardando revisão e integração do [pedido #1](https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2/pull/1), preparado em codex/fase-2-comilao. Até essa integração, baixar apenas a main pode trazer a versão antiga. Não misturem commits do repositório anterior.

## Baixar uma vez

~~~sh
git clone https://github.com/barrosojoaomarcelo-coder/Cuphead-Mineirinho-2.git
cd Cuphead-Mineirinho-2
python -m pip install -r requirements.txt
~~~

Depois escolham sua branch conforme a seção seguinte. Cada integrante usa sua própria conta e identidade no Git.

## Atualizar a branch pessoal

**Antes de trocar de branch ou baixar alterações, executem git status.** Se houver arquivos modificados ou novos, revisem e façam commit do trabalho que deve ser preservado na branch atual. Não apaguem os commits locais; se a atualização recusar por divergência, sigam a orientação abaixo. Não substituam uma pasta de trabalho pelo conteúdo de um ZIP para tentar sincronizá-la.

Com o trabalho registrado e a pasta limpa, usem o bloco da própria pessoa.

Moisés:

~~~sh
git status
git switch moises
git pull --ff-only origin moises
~~~

Davi:

~~~sh
git status
git switch davi
git pull --ff-only origin davi
~~~

João Marcelo:

~~~sh
git status
git switch cajarelo
git pull --ff-only origin cajarelo
~~~

Se git switch informar que a branch não foi encontrada, executem git fetch origin e tentem novamente. Confirmem no GitHub se a sincronização da branch foi concluída.

Se pull --ff-only recusar por divergência, isso protege os commits locais: **não usem force push nem reset**. Confiram git status, registrem o trabalho pendente, executem git fetch origin e revisem os dois históricos com o colega. Só depois façam merge da branch remota correspondente. Exemplo para Moisés:

~~~sh
git log --oneline --left-right HEAD...origin/moises
git merge origin/moises
~~~

Davi troca moises por davi; João troca por cajarelo. Se houver conflito, comparem os dois trechos com a pessoa responsável, preservem as duas contribuições, retirem as marcações e testem antes de concluir o commit do merge. Não escolham um lado inteiro sem revisar.

## Trabalhar, testar e enviar

Moisés cuida das regras; Davi, do desenho e som; João, dos menus e entrega. Combinem antes de editar o mesmo arquivo. A lista concreta está em [TAREFAS_ATE_SEGUNDA.md](TAREFAS_ATE_SEGUNDA.md).

~~~sh
python -m unittest discover -s tests -v
python main.py
git status
~~~

Revisem as diferenças, adicionem somente os arquivos da tarefa com git add CAMINHO_DO_ARQUIVO e façam git commit -m "Descreve a mudança e seu resultado". Substituam os exemplos pelos arquivos e mensagens reais. Depois enviem pela branch pessoal:

~~~sh
git push origin moises
~~~

Davi usa git push origin davi; João usa git push origin cajarelo. Não enviem .venv, senhas, preferências pessoais, caches nem um ZIP no lugar do código. Registrem contribuições reais, sem criar commits só para aparentar participação.

## Integrar a versão final à main

1. João coordena a revisão do pedido #1 e sua integração à main antes da entrega. Os três precisam executar e compreender a versão final; sincronizar branches não comprova revisão humana.
2. As correções posteriores passam por pull request para main, com explicação do problema, da mudança e dos testes. Davi revisa Moisés; João revisa Davi; Moisés revisa João.
3. Depois que a main receber a base e outras correções, cada um traz essa versão para sua branch pessoal: com trabalho registrado e pasta limpa, executa git fetch origin e git merge origin/main, confere os testes e envia sua branch.
4. João confere um clone novo da main, seguindo apenas o README. É essa versão final que precisa estar acessível no endereço entregue ao professor.

A base foi preparada com auxílio de IA. Cada um deve compreender o código e registrar suas próprias alterações em USO_DE_IA.md. Se o convite de Davi continuar pendente, João precisa resolvê-lo e Davi precisa aceitar; sincronizar a branch remota não concede acesso à conta.
