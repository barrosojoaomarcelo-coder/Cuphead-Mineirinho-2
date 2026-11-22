# Validação — perfil difícil e animações

Data: 22/11/2026. Ambiente local: Windows, Python 3.12.14, Pygame 2.6.1 e vídeo/áudio virtuais do SDL.

## Resultado

Comando: python -m unittest discover -s tests -q

**58 testes aprovados**, sem falhas ou testes ignorados. São os 47 casos anteriores adaptados aos novos valores e 11 casos adicionais de dificuldade e animação.

A comparação com boss_attacks.py do ZIP fornecido confirmou os **40 parâmetros de cada um dos quatro níveis do dragão**, sem diferenças. Vida do chefe: 480, como no ZIP. A portabilidade conserva os números, mas usa o loop simples do projeto; não promete equivalência numérica quadro a quadro com o outro motor.

## Esquivas sem proteção adicional

- Rajadas horizontais: quatro níveis × duas ordens de altura × duas posições × 30/60/120 atualizações por segundo; pulo nas baixas e agachamento nas altas, mantendo três vidas.
- Duas bolas gigantes: níveis 3 e 4, duas posições, 30/60/120 atualizações por segundo; dois pulos separados, mantendo três vidas.
- Comilão: combo final de língua baixa/alta/baixa em 30/60/120 atualizações por segundo; pulo/agachamento conservam três vidas. Cada golpe tem um aviso próprio de pelo menos 0,72 s.
- Três ondas de espinhos do Comilão: quatro posições iniciais; andar para o corredor anunciado conserva três vidas.

Outros casos verificam direção fixa, volume/altura das fileiras, exclusividade da segunda bola agendada, pausa, limpeza em morte/vitória/transformação/reinício, colisão no trajeto de projétil rápido, 12 poses distintas por forma, hitbox independente da deformação e limite de 256 imagens de animação em cache. Um jogador parado perde suas três vidas no combate natural do dragão.

As lutas completas dos dois chefes continuam chegando à vitória em 30/60/120 atualizações por segundo, agora com 480 acertos. Somente esses testes de fluxo usam proteção prolongada; isso não mede dificuldade humana.

## Verificação visual e desempenho

Foram renderizados e inspecionados o menu com identificação da versão difícil, o dragão abaixando para a rajada, as duas formas do Comilão, o alinhamento dos raios/língua, a chuva e o corredor seguro. A prévia docs/comilao-animacao.gif contém 122 quadros e 12,2 segundos de execução gravada, incluindo a transformação, sem proteção de teste. O jogador terminou essa amostra com duas vidas.

Amostra local de update e desenho durante a captura: média de 9,35 ms; percentil 95 de 18,08 ms por quadro. Não é uma garantia de desempenho em outros computadores. As imagens transformadas e os flashes são reaproveitados pelo cache.

## Pacote e limites

O pacote contém 68 arquivos. O ZIP é extraído em pasta nova e todos os conteúdos são comparados por SHA-256 antes da entrega; os testes são executados também na cópia extraída.

O grupo precisa jogar com teclado físico, ouvir os volumes e testar a instalação nos três computadores. A terceira fase e o encerramento ainda estão pendentes. Os resultados são locais; atualizar uma branch não significa integrar à main nem executar testes remotos.
