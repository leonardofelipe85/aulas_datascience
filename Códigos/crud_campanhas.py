import psycopg2

# CONEXÃO

def conectar(): 

     conexao = psycopg2.connect(
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
       gasto FLOAT

      )                            
                                              
             
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

# EXECUTAR 

criar_tabela()

inserir_campanha(
     "Black Friday", 
     "Meta Ads", 
     3.2,
     1200
    )


#LISTAR CAMPANHA 

def listar_campanha(): 
     conexao = conectar()
     cursor = conexao.cursor()
     cursor.execute("SELECT * FROM campanhas")
     campanhas = cursor.fetchall()
     
     
     print("\n CAMPANHAS CADASTRADAS:\n")

     for campanha in campanhas: 

        print(campanha)

        cursor.close()
        conexao.close()

listar_campanha()           