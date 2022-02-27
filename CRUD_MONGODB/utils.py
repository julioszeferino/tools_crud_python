from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from bson import errors as berrors


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = MongoClient(
        'localhost',
        27017)

    return conn


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    db = conn.pmongo

    try: # O try entra nesse momento porque é onde poderá haver erro e nao na conexao
        if db.produtos.count_documents({}) > 0:
            produtos = db.produtos.find()
            print('Listando produtos...')
            print('--------------------')

            for produto in produtos:
                print(f"ID: {produto['_id']}")
                print(f"Produto: {produto['nome']}")
                print(f"Preco: {produto['preco']}")
                print(f"Estoque: {produto['estoque']}")
                print('------------------------')
        else:
            print('Não existem produtos cadastrados.')

    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')

    desconectar(conn)


def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    db = conn.pmongo


    nome: str = input('Informe o nome do produto: ')
    preco: float = float(input('Informe o preco do produto: '))
    estoque: int = int(input('Informe a quantidade em estoque: '))

    try:
        db.produtos.insert_one(
            {
                "nome": nome,
                "preco": preco,
                "estoque": estoque
            }
        )
        print(f'O produto {nome} foi inserido com sucesso.')
    
    except errors.PyMongoError as e:
         print(f'Não foi possível inserir o produto. Veja o erro {e}')

    desconectar(conn)


def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    db = conn.pmongo

    _id: str = input('Informe o código do produto: ')
    nome: str = input('Informe o novo nome do produto: ')
    preco: float = float(input('Informe o novo preco do produto: '))
    estoque: int = int(input('Informe a nova quantidade em estoque: '))

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                        }
                }
            )
            if res.modified_count == 1:
                print(f'O produto {nome} foi atualizado com sucesso.')
            else:
                print('Não foi possível atualizar o produto.')
        else:
            print('Não existem documentos para serem atualizados.')
    except errors.PyMongoError as e:
        print('Erro ao acessar o banco de dados: {e}')
    except berrors.InvalidId as f:
        print('ObjectID invalido!')
    
    desconectar(conn)


    

def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()
    db = conn.pmongo

    _id: int = input('Informe o código do produto: ')

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )

            if res.deleted_count > 0:
                print("Produto deletado com sucesso!")
            else:
                print('Não foi possível deletar o produto.')
        else:
            print("Não existem produtos para serem deletados.")
    except errors.PyMongoError as e:
        print('Erro ao acessar o banco de dados: {e}')
    except berrors.InvalidId as f:
        print('ObjectID invalido!')

    desconectar(conn)



def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
