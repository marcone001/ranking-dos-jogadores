# ranking-dos-jogadores

Guia de Uso do Sistema de Ranking de Jogadores

Este projeto importa dados de jogadores de um arquivo CSV, salva em um banco SQLite, gera um ranking ordenado e salva uma página HTML com o ranking.

Como usar
1. Preparar os arquivos

Tenha o arquivo CSV com os dados dos jogadores (exemplo: jogadores.csv).

O arquivo CSV deve conter colunas na ordem: nome, nível, pontuação.

2. Rodar o script Python

No terminal, execute o script:

python main.py


Quando solicitado, digite o nome do arquivo CSV (exemplo: jogadores.csv) e pressione Enter.

3. O que acontece?

O banco de dados SQLite (ranking.db) será criado ou atualizado.

Os dados do CSV serão importados para o banco.

O ranking dos jogadores será exibido no terminal, ordenado pela pontuação.

O arquivo ranking.html será gerado com o ranking em formato de tabela estilizada.

4. Visualizar o ranking

Abra o arquivo ranking.html gerado no navegador (basta clicar duas vezes no arquivo).

Visualize o ranking formatado com as três primeiras posições destacadas.

5. Atualizar o ranking

Atualize o arquivo CSV com novos dados.

Execute novamente o script main.py para gerar o ranking atualizado.

Requisitos

Python 3.x

Biblioteca padrão (csv, sqlite3, etc.) — não requer instalações extras
