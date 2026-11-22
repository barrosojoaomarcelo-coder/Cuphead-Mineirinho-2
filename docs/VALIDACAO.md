# Validação — Dragão e Chefe Comilão

Data: 22/11/2026. Ambiente local: Windows, Python 3.12.14 e Pygame 2.6.1. Vídeo/áudio virtuais do SDL.

## Resultado

Comando: python -m unittest discover -s tests -v

**47 testes aprovados, sem falhas ou testes ignorados.** Os 36 casos anteriores continuam aprovados, com as expectativas do menu atualizadas para incluir a história. Outros 11 casos verificam a fase 2 e a passagem entre cenários.

Cobertura nova: avanço somente após vitória; ausência de um terceiro chefe jogável; seis ataques sempre precedidos por aviso; direções dos raios fixadas no aviso; língua baixa causa um único dano; língua alta passa sobre jogador no chão; pulo e dash evitam a língua baixa; faixa segura dos espinhos; remoção de ataques; segunda forma; pausa; reinício na fase atual; telas; transparência das artes; separação do recorde do dragão.

As duas lutas chegaram à vitória com 360 acertos em 30, 60 e 120 atualizações por segundo. Nesses casos foi ativada proteção prolongada somente no teste: isso verifica o fluxo, não a dificuldade para uma pessoa. O jogo normal começa com três vidas.

## Verificação visual

Foram renderizados e inspecionados menu, história, dragão, corpo do Comilão, aviso dos raios, língua estendida, segunda forma e vitória da fase 2. Também foram renderizados os espinhos e seus avisos. Capturas representativas estão em docs/preview.png, docs/comilao-corpo.png e docs/comilao-boca.png.

Um roteiro adicional usou main.update_game e main.draw_screen por 180 quadros na fase 2, incluindo tiros e espinhos: média local de 15,67 ms por quadro; percentil 95 de 25,44 ms. É uma amostra local com saída de vídeo virtual, não uma garantia de desempenho em todos os computadores.

## Pacote ZIP

O pacote final contém 60 arquivos. Foi extraído em uma pasta nova; os 60 conteúdos foram comparados por SHA-256 com a pasta de origem. Os 47 testes também passaram na cópia extraída.

## Limites e pendências

A execução virtual não substitui jogar com teclado físico, ouvir volumes e avaliar dificuldade com pessoas. O grupo precisa testar nos três computadores e gravar o vídeo. O iniciador Windows requer Python e internet na primeira instalação. A terceira fase e o encerramento completo ainda não estão implementados.

Os resultados acima são locais. A publicação em uma branch não significa que o jogo foi integrado à main ou que uma verificação remota tenha sido executada.
