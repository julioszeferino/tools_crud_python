import socket
import couchdb


def conectar():
    """
    Função para conectar ao servidor
    """
    user:str = 'admin'
    password:str = 'juz'
    conn = couchdb.Server(f'http://{user}:{password}@localhost:5984')

    banco: str = 'pcouch'

    # se o banco existir na conexao
    if banco in conn:
        db = conn[banco]

        return db
    else:
        # crie o banco
        try:
            db = conn.create(banco)
            return db
        except socket.gaierror as e:
            print(f'Erro ao conectar no servidor: {e}')
        except couchdb.Unauthorized as a:
            print(f'Você não tem permissão de acesso: {a}')
        except ConnectionRefusedError as g:
            print(f'Não foi possível se conectar ao servidor: {g}')


def listar():
    """
    Função para listar os produtos
    """
    db = conectar()

    if db:
        # se existirem documentos
        if db.info()['doc_count'] > 0:
            print('Listando produtos...')
            print('--------------------')

            for doc in db:
                print(f"ID: {db[doc]['_id']}")
                print(f"Rev: {db[doc]['_rev']}")
                print(f"Produto: {db[doc]['nome']}")
                print(f"Preco: {db[doc]['preco']}")
                print(f"Estoque: {db[doc]['estoque']}")
                print('------------------------')
        else:
            print('Não existem produtos cadastrados.')
    else:
        print('Não foi possível conectar com o servidor.')


def inserir():
    """
    Função para inserir um produto
    """  
    db = conectar()

    if db:
        nome: str = input('Informe o nome do produto: ')
        preco: float = float(input('Informe o preco do produto: '))
        estoque: int = int(input('Informe a quantidade em estoque: '))

        produto = {
            "nome": nome,
            "preco": preco,
            "estoque": estoque
        }

        # adicionando o produto a colecao produtos
        res = db.save(produto)

        if res:
            print(f'O produto {nome} foi inserido com sucesso.')
        else:
            print('Não foi possível cadastrar o produto.')


def atualizar():
    """
    Função para atualizar um produto
    """
    db = conectar()

    if db:
        _id: str = input('Informe o código do produto: ')

        try:
            doc = db[_id]

            nome: str = input('Informe o novo nome do produto: ')
            preco: float = float(input('Informe o novo preco do produto: '))
            estoque: int = int(input('Informe a nova quantidade em estoque: '))

            
            doc["nome"] = nome
            doc["preco"] = preco
            doc["estoque"] = estoque
            db[doc.id] = doc

            print(f'O produto {nome} foi atualizado com sucesso.')
        
        except couchdb.http.ResourceNotFound as e:
            print(f'Produto não encontrado: {e}')
    else:
        print("Erro ao conectar ao servidor.")


def deletar():
    """
    Função para deletar um produto
    """  
    db = conectar()

    if db:
        _id: str = input('Informe o código do produto: ')

        try:
            db.delete(db[_id])  
            print("Produto deletado com sucesso!")
        except couchdb.http.ResourceNotFound as e:
            print('Não foi possível deletar o produto.')
    else:
        print("Erro ao conectar ao servidor.")


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
