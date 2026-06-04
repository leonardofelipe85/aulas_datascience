import psycopg2

# CONEXÃO

def conectar(): 

     conexao =  psycopg2.connect(
        host = "localhost", 
        database = "postgres", 
        user = "postgres",
        password = "123" 

)

     print("Conexão realizada com sucesso!")
     return conexao 



# Criar tabela 

def criar_tabela():
     conexao = conectar()
     cursor = conexao.cursor()
     cursor.execute("""
                    
      CREATE TABLE IF NOT EXISTS campanhas (
                    
       id SERIAL PRIMARY KEY,
       campanha VARCHAR(100), 
       plataforma VARCHAR(50), 
       ctr FLOAT, 
       gasto FLOAT,
       data_registro DATE DEFAULT CURRENT_DATE

      );                            
                                              
             
     """)
    
     conexao.commit()

     print("Tabela criada com sucesso")

     cursor.close()
     conexao.close()

# INSERIR CAMPANHA 

def inserir_campanha(campanha, plataforma, ctr, gasto): 
     
     conexao = conectar()
     cursor = conexao.cursor()
     cursor.execute("""
                    
    
       INSERT INTO campanhas
       (campanha, plataforma, ctr, gasto)   
                    
        VALUES (%s, %s, %s, %s)
""", (campanha, plataforma, ctr, gasto))
     
     conexao.commit()

     print("Campanha inserida com sucesso")

     cursor.close()
     conexao.close()

#LISTAR CAMPANHA 

def listar_campanha(): 
     conexao = conectar()
     cursor = conexao.cursor()
     cursor.execute("SELECT * FROM campanhas ORDER BY id ASC")
     campanhas = cursor.fetchall()
     
     
     print("\n CAMPANHAS CADASTRADAS:\n")

     for cp in campanhas: 
# Mostra a linha do banco e adiciona a data formatada ao lado para conferência       

          print(f" {cp} | Data do Registro: {cp[5]}")

     print()
               
     
     cursor.close()
     conexao.close()

# UPDATE CAMPANHA

def atualizar_ctr(id_campanha, novo_ctr):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""

        UPDATE campanhas

        SET ctr = %s

        WHERE id = %s

    """, (novo_ctr, id_campanha))

    conexao.commit()

    print("CTR atualizado com sucesso!")

    cursor.close()
    conexao.close()

    # DELETE CAMPANHA

def deletar_campanha(id_campanha):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""

        DELETE FROM campanhas

        WHERE id = %s

    """, (id_campanha,))

    conexao.commit()

    print("Campanha deletada com sucesso!")

    cursor.close()
    conexao.close()

# DIRETRIZES DE EXECUÇAO (MOMENTO DE PRÁTICA)

if __name__ == "__main__": 
     print("--- INICIANDO TESTE DO SISTEMA DE TRÁFEGO---")

     # Passo A: Cria a tabela limpa com a nova coluna de data
criar_tabela()
    
    # Passo B: Insere o seu dado de teste
inserir_campanha("Black Friday", "Meta Ads", 3.2, 1200.0)
    
    # Passo C: Lista para conferirmos o nascimento do dado com o carimbo do tempo
listar_campanha()
    
    # Passo D: Aplica a atualização no ID 1 para testar o UPDATE
atualizar_ctr(1, 8.5)
    
# Passo E: Mostra o resultado final com o dado atualizado e na ordem correta
listar_campanha()

           