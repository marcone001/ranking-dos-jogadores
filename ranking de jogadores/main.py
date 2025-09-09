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

# Mostrar ranking ordenado
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

# Programa principal
def main():
    print("=== Sistema de Ranking de Jogadores (SQLite) ===")
    nome_arquivo = input("Digite o nome do arquivo CSV (ex: jogadores.csv): ")

    # Criar banco e tabela
    conexao = criar_banco()

    # Limpar tabela antes de importar novamente
    conexao.execute("DELETE FROM jogadores")
    conexao.commit()

    # Importar dados
    importar_csv_para_sqlite(conexao, nome_arquivo)

    # Exibir ranking
    exibir_ranking(conexao)

    conexao.close()

if __name__ == "__main__":
    main()