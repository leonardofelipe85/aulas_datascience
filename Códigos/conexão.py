import psycopg2

try:
    # Conectando ao banco de dados usando a nova regra de confiança
    conexao = psycopg2.connect(
        host="localhost",
        database="postgres",  # Banco padrão que já vem criado
        user="postgres",
        password="123"        # Qualquer senha funciona agora que está em trust
    )

    cursor = conexao.cursor()
    
    # Executa o comando SQL para pedir a versão do sistema
    cursor.execute("SELECT version();")
    versao = cursor.fetchone()
    
    print("\n[SUCESSO] Python e pgAdmin estão conversando perfeitamente!")
    print(f"Versão ativa do Banco: {versao[0]}\n")

    cursor.close()
    conexao.close()

except Exception as erro:
    print(f"\n[ERRO] Falha na conexão: {erro}\n")