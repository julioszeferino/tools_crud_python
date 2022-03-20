import redis


def gera_id():
    try:
        conn = conectar()

        chave = conn.get('chave')

        if chave:
            chave = conn.incr('chave')
            return chave
        else:
            conn.set('chave', 1)
            return 1

    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível gerar a chave. {e}')


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = redis.Redis(host='localhost', port=6379)
    return conn


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    conn.connection_pool.disconnect()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    
    try:
        # buscando as chaves
        dados = conn.keys(pattern='produtos:*')

        if len(dados) > 0:
            print('Listando produtos...')
            print('--------------------')
            for chave in dados:
                # para cada uma das chaves, retorno o valor
                produto = conn.hgetall(chave)

                print(f"ID: {str(chave, 'utf-8', 'ignore')}")
                # o dado vem no formato string binaria
                print(f"Produto: {str(produto[b'nome'], 'utf-8', 'ignore')}")
                print(f"Preco: {str(produto[b'preco'], 'utf-8', 'ignore')}")
                print(f"Estoque: {str(produto[b'estoque'], 'utf-8', 'ignore')}")
                print('------------------------')
        else:
            print('Não existem produtos cadastrados.')
    
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível listar os produtos. {e}')

    desconectar(conn)


def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()

    nome: str = input('Informe o nome do produto: ')
    preco: float = float(input('Informe o preco do produto: '))
    estoque: int = int(input('Informe a quantidade em estoque: '))

    # definindo o valor
    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    # definindo a chave
    chave = f'produtos:{gera_id()}'

    try:
        res = conn.hmset(chave, produto)

        if res:
            print(f'O produto {nome} foi inserido com sucesso.')
        else:
             print('Não foi possível inserir o produto')
    
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inserir o produto. {e}')

    desconectar(conn)


def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()

    chave: str = str(input('Informe a chave do produto: '))

    # validando se a chave existe
    valid = conn.keys(pattern='produtos:*')
    valid1 = [str(nome, 'utf-8', 'ignore') for nome in valid]

    if chave not in valid1:
        print(f'Chave Inválida: {chave}.Não foi possível atualizar o produto.')
        desconectar(conn)
    else:
        # atualizando os dados
        nome: str = input('Informe o novo nome do produto: ')
        preco: float = float(input('Informe o novo preco do produto: '))
        estoque: int = int(input('Informe a nova quantidade em estoque: '))

        # definindo o novo valor
        produto = {"nome": nome, "preco": preco, "estoque": estoque}

        try:
            res = conn.hmset(chave, produto)

            if res:
                print(f'O produto {nome} foi atualizado com sucesso.')

        except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível atualizar o produto. {e}')

    desconectar(conn)

    

def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()

    chave: str = str(input('Informe o código do produto: '))

    try:
        res = conn.delete(chave)

        if res == 1:
            print('Produto excluído com sucesso.')
        else:
            print(f'Não foi possível excluir o produto com chave {chave}')

    except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível deletar o produto. {e}')


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
