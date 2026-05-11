with open('index.html', 'r') as f:
    content = f.read()
with open('/tmp/relatorio.html', 'r') as f:
    dados = f.read()
novo = content.replace('<!-- DADOS_GERADOS -->', dados)
with open('index.html', 'w') as f:
    f.write(novo)
print('index.html atualizado com sucesso')