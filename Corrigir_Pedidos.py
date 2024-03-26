import psycopg2
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Função para conectar ao banco de dados
def conectar_banco(banco, senha):
    try:
        conexao = psycopg2.connect(
            database=banco,
            user="postgres",
            password=senha,
            host="localhost",
            port="5432",
        )
        return conexao
    except psycopg2.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados {banco}: {e}")
        return None

# Função para corrigir os pedidos na base de dados
def corrigir_pedidos(conexao, pedidos):
    try:
        cursor = conexao.cursor()
        for pedido_id in pedidos:
            cursor.execute(f"SELECT corrigir_pedidos(ARRAY[{pedido_id}])")
        conexao.commit()
        logging.info("Pedidos corrigidos com sucesso.")
    except psycopg2.Error as e:
        conexao.rollback()
        logging.error(f"Erro ao corrigir pedidos: {e}")

# Função principal
def main():
    banco = "Atalaia"
    senha = input("Digite a senha do banco: ")
    conexao = conectar_banco(banco, senha)

    if conexao:
        logging.info("Conectado ao banco de dados %s", banco)
        try:
            numeros_pedidos = input("Digite os números dos pedidos a serem corrigidos (separados por vírgula): ")
            pedidos = [int(pedido.strip()) for pedido in numeros_pedidos.split(",")]
            corrigir_pedidos(conexao, pedidos)
        except ValueError:
            logging.error("Formato inválido para números de pedidos.")
        conexao.close()
    else:
        logging.error("Erro ao conectar ao banco de dados %s", banco)

if __name__ == "__main__":
    main()
