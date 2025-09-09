import csv
import sqlite3
import os

# Criar banco de dados e tabela
def criar_banco(nome_banco="ranking.db"):
    conexao = sqlite3.connect(nome_banco)
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nivel INTEGER NOT NULL,
            pontuacao REAL NOT NULL
        )
    """)
    conexao.commit()
    return conexao

# Importar jogadores de um CSV para o banco
def importar_csv_para_sqlite(conexao, nome_arquivo):
    cursor = conexao.cursor()
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                if len(linha) >= 3:  # nome, nível, pontuação
                    nome = linha[0].strip()
                    try:
                        nivel = int(linha[1].strip())
                        pontuacao = float(linha[2].strip())
                        cursor.execute(
                            "INSERT INTO jogadores (nome, nivel, pontuacao) VALUES (?, ?, ?)",
                            (nome, nivel, pontuacao)
                        )
                    except ValueError:
                        print(f"Atenção: linha inválida ignorada -> {linha}")
        conexao.commit()
        print(f"✅ Dados importados de {nome_arquivo} para o banco SQLite.")
    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")

# Mostrar ranking ordenado no terminal
def exibir_ranking(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, nivel, pontuacao FROM jogadores ORDER BY pontuacao DESC")
    jogadores = cursor.fetchall()

    print("\n🏆 Ranking dos Jogadores 🏆")
    print("-" * 40)

    for i, (nome, nivel, pontuacao) in enumerate(jogadores, start=1):
        if i == 1:
            medalha = "🥇"
        elif i == 2:
            medalha = "🥈"
        elif i == 3:
            medalha = "🥉"
        else:
            medalha = f"{i}."
        print(f"{medalha} {nome} (Nível {nivel}) → {pontuacao:.2f} pontos")

    return jogadores

# Gerar ranking em HTML
def salvar_ranking_html(jogadores, nome_saida="ranking.html"):
    cores = ["gold", "silver", "#cd7f32"]  # Ouro, Prata, Bronze
    try:
        with open(nome_saida, "w", encoding="utf-8") as f:
            f.write("""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Ranking de Jogadores</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; background: #f4f4f4; }
                    h1 { color: #333; }
                    table { margin: auto; border-collapse: collapse; width: 60%; }
                    th, td { border: 1px solid #ccc; padding: 10px; }
                    th { background: #333; color: white; }
                </style>
            </head>
            <body>
                <h1>🏆 Ranking dos Jogadores 🏆</h1>
                <table>
                    <tr>
                        <th>Posição</th>
                        <th>Nome</th>
                        <th>Nível</th>
                        <th>Pontuação</th>
                    </tr>
            """)
            for i, (nome, nivel, pontuacao) in enumerate(jogadores, start=1):
                if i <= 3:
                    cor = cores[i - 1]
                else:
                    cor = "white"
                f.write(f"""
                    <tr style="background:{cor};">
                        <td>{i}</td>
                        <td>{nome}</td>
                        <td>{nivel}</td>
                        <td>{pontuacao:.2f}</td>
                    </tr>
                """)
            f.write("""
                </table>
            </body>
            </html>
            """)
        print(f"\n✅ Ranking salvo em: {nome_saida}")
    except Exception as e:
        print(f"Erro ao salvar HTML: {e}")

# Programa principal
def main():
    print("=== Sistema de Ranking de Jogadores (SQLite + HTML) ===")
    nome_arquivo = input("Digite o nome do arquivo CSV (ex: jogadores.csv): ")

    # Criar banco e tabela
    conexao = criar_banco()

    # Limpar tabela antes de importar novamente
    conexao.execute("DELETE FROM jogadores")
    conexao.commit()

    # Importar dados
    importar_csv_para_sqlite(conexao, nome_arquivo)

    # Exibir ranking no terminal
    jogadores = exibir_ranking(conexao)

    # Salvar em HTML
    salvar_ranking_html(jogadores)

    conexao.close()

if __name__ == "__main__":
    main()
