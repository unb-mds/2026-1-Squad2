import sys, json, os
from collections import defaultdict

dados = json.load(sys.stdin)
contagem = defaultdict(lambda: {'abertas': 0, 'fechadas': 0})

for i in dados:
    if i.get('assignee'):
        user = i['assignee']['login']
        if i['state'] == 'open':
            contagem[user]['abertas'] += 1
        else:
            contagem[user]['fechadas'] += 1

for user, d in contagem.items():
    print(f'<tr><td>{user}</td><td>{d["abertas"]}</td><td>{d["fechadas"]}</td></tr>')