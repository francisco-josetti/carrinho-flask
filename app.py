from flask import Flask, render_template, request, redirect, url_for, session, flash

# Criar a aplicação Flask
app = Flask(__name__)

# Chave secreta para sessões (em produção, use uma chave mais segura)
app.secret_key = 'sua_chave_secreta_aqui'

# Configuração dos produtos (simulando um banco de dados)
app.config['PRODUTOS'] = {
    1: {
        'id': 1, 
        'nome': 'Farinha de trigo', 
        'preco': 7.00, 
        'imagem_url': 'https://www.jmacedo.com.br/wp-content/uploads/2022/03/jmacedo-brandini-farinha-de-frigo-tradicional-1.jpg'
    },
    2: {
        'id': 2, 
        'nome': 'Uva sem sementes', 
        'preco': 2.00, 
        'imagem_url': 'https://www.raizs.com.br/_next/image?url=https://static.raizs.com.br/products/0/a/5/e/0a5eb5ebd9b38a2e485f726a9cec9670a3f472b1_Sustentaveis_uvavitoria.jpg&w=1920&q=75'
    },
    3: {
        'id': 3, 
        'nome': 'Caderno do Batman', 
        'preco': 40.00, 
        'imagem_url': 'https://img.kalunga.com.br/fotosdeprodutos/140176d_1.jpg'
    },
    4: {
        'id': 4, 
        'nome': 'Roupa', 
        'preco': 70.00, 
        'imagem_url': 'https://static.vecteezy.com/ti/fotos-gratis/t2/51347563-a-sobrecarga-visao-do-mulher-casual-roupas-foto.jpg'
    },
}

# Rota principal - Lista de produtos
@app.route('/')
def index():
    produtos = app.config['PRODUTOS']
    return render_template('index.html', produtos=produtos)

# Rota para adicionar produto ao carrinho
@app.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    produtos = app.config['PRODUTOS']
    
    # Recuperar carrinho da sessão (ou criar lista vazia)
    carrinho = session.get('carrinho', [])
    
    # Adicionar produto ao carrinho
    carrinho.append(produtos[produto_id])
    
    # Salvar carrinho na sessão
    session['carrinho'] = carrinho
    
    # Mensagem de feedback
    flash('Produto adicionado ao carrinho!')
    
    return redirect(url_for('index'))

# Rota para visualizar o carrinho
@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    
    # Calcular total
    total = sum(item['preco'] for item in carrinho)
    
    return render_template('carrinho.html', carrinho=carrinho, total=total)

# Rota para remover produto do carrinho
@app.route('/remover/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    
    # Procurar e remover produto
    for produto in carrinho:
        if produto['id'] == produto_id:
            carrinho.remove(produto)
            session['carrinho'] = carrinho
            flash('Produto removido do carrinho!')
            break
    else:
        flash('Produto não encontrado no carrinho.')
    
    return redirect(url_for('carrinho'))

#Limpar carrinho
@app.route('/limpar_carrinho', methods=['POST'])
def limpar_carrinho():
    session.pop('carrinho', None)
    flash('Carrinho esvaziado')
    return redirect(url_for('carrinho'))

# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)