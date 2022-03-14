import pyrebase


def conectar():
    """
    Função para conectar ao servidor
    """
    config = {
        "apiKey": "AAAAzE2o0lY:APA91bHJFRkSu5ahTc7FQstk4X_QvudIaPXYu0EUJXPlSK64ncrWWYVveqhMi-fuV0udpxX9IHBLxicyO6dFSiVakZfWoOVxS_vyr2PWBFZ55H7c1IToTvcZmEiqrzzP2puicPzC5elB",
        "authDomain": "https://crudpython-346dc-default-rtdb.firebaseio.com/",
        "databaseURL": "https://crudpython-346dc-default-rtdb.firebaseio.com/",
        "storageBucket": "crudpython-346dc-default-rtdb.appspot.com/"
    }

    conn = pyrebase.initialize_app(config)

    db = conn.database()

    return db


def listar():
    """
    Função para listar os produtos
    """
    db = conectar()
    produtos = db.child("produtos").get() # request

    if produtos.val():
        print('Listando produtos...')
        print('--------------------')

        for produto in produtos.each():
            print(f"ID: {produto.key()}")
            print(f"Produto: {produto.val()['nome']}")
            print(f"Preco: {produto.val()['preco']}")
            print(f"Estoque: {produto.val()['estoque']}")
            print('------------------------')
    else:
        print('Não existem produtos cadastrados.')


def inserir():
    """
    Função para inserir um produto
    """  
    db = conectar()

    nome: str = input('Informe o nome do produto: ')
    preco: float = float(input('Informe o preco do produto: '))
    estoque: int = int(input('Informe a quantidade em estoque: '))

    produto = {
        "nome": nome,
        "preco": preco,
        "estoque": estoque
    }

    # adicionando o produto a colecao produtos
    res = db.child("produtos").push(produto)

    if 'name' in res:
        print(f'O produto {nome} foi inserido com sucesso.')
    else:
        print('Não foi possível cadastrar o produto.')


def atualizar():
    """
    Função para atualizar um produto
    """
    db = conectar()

    _id: str = input('Informe o código do produto: ')

    # buscando os documentos com o id inserido na colecao produtos
    produto = db.child("produtos").child(_id).get()

    # verificando se o produto existe
    if produto.val():
        nome: str = input('Informe o novo nome do produto: ')
        preco: float = float(input('Informe o novo preco do produto: '))
        estoque: int = int(input('Informe a nova quantidade em estoque: '))

        novo_produto = {
            "nome": nome,
            "preco": preco,
            "estoque": estoque
        }

        db.child('produtos').child(_id).update(novo_produto)
        print(f'O produto {nome} foi atualizado com sucesso.')

    else:
        print('Não existem documentos para serem atualizados.')


def deletar():
    """
    Função para deletar um produto
    """  
    db = conectar()

    _id: str = input('Informe o código do produto: ')

    # buscando os documentos com o id inserido na colecao produtos
    produto = db.child("produtos").child(_id).get()

    # verificando se o produto existe
    if produto.val():
        db.child("produtos").child(_id).remove()
        print("Produto deletado com sucesso!")
    else:
        print("Não existem produtos para o id informado.")


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
