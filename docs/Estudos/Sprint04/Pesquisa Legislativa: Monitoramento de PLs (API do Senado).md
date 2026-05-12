
# 🏛️ Pesquisa Legislativa: Monitoramento de PLs (API do Senado)

Este documento detalha o funcionamento da extração de dados da API de Dados Abertos do Senado Federal para o monitoramento de projetos de lei relacionados aos direitos das mulheres, feminicídio e violência doméstica.

## 🎯 Objetivo da Pesquisa
O foco é identificar proposições legislativas que alterem o Código Penal ou tratem de Direitos Humanos, utilizando filtros temáticos e palavras-chave específicas para garantir a relevância dos dados.

---

## 🔍 1. Listagem e Descoberta de Projetos

Para encontrar novos projetos ou atualizações, utilizamos o endpoint de pesquisa de processos.

**URL de Consulta:** `https://legis.senado.leg.br/dadosabertos/processo`

### Parâmetros Padrões Utilizados:
| Parâmetro | Valores Exemplo | Descrição |
| :--- | :--- | :--- |
| `sigla` | `PL`, `PLP` | Filtra por Projetos de Lei Ordinária e Complementar. |
| `termo` | `mulher`, `feminicídio` | Palavras-chave buscadas na ementa e indexação. |
| `codAssuntoGeral` | `130`, `143` | IDs para Direito Penal e Direitos Humanos/Minorias. |
| `numdias` | `1` | Filtra apenas processos atualizados nas últimas 24h (ideal para automação). |

### Exemplo de Implementação (Python):
```python
import requests
import json

url = "https://legis.senado.leg.br/dadosabertos/processo"
termos_busca = ["mulher", "feminicídio", "violência contra mulher"]
assunto_geral = [130, 143]
siglas = ["PL", "PLP"]

headers = {"Accept": "application/json"}

for termo in termos_busca:
    for sigla in siglas:
        for assunto in assunto_geral:
            params = {
                "termo": termo,
                "codAssuntoEspecifico": assunto,
                "sigla": sigla,
              #  "numdias": 1  Remova ou comente para ver todo o histórico
            }
            
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                dados = response.json()
                # Processar os IDs encontrados aqui
                print(json.dumps(dados, indent=4, ensure_ascii=False))
            else:
                print(f"Erro {response.status_code} na busca de {termo}")
```

---

## 📄 2. Detalhamento de um PL Específico

Após obter o ID de um processo na listagem, utilizamos o endpoint de detalhamento para extrair informações ricas para estatísticas (Autor, Gênero, Partido, Status).

**URL de Consulta:** `https://legis.senado.leg.br/dadosabertos/processo/{id}?v=1`

### Script de Extração de Dados Essenciais:
O JSON retornado pela API é extenso e aninhado. A função abaixo "achata" os dados para facilitar o uso em bancos de dados ou gráficos.

```python
import requests
import json

def extrair_dados_essenciais(projeto):
    """Limpa o JSON confuso do Senado para campos legíveis."""
    # Navega nas camadas de autuações e situações
    autuacoes = projeto.get("autuacoes", [{}])[0]
    situacoes = autuacoes.get("situacoes", [])
    informes = autuacoes.get("informesLegislativos", [])
    
    status_atual = situacoes[-1].get("descricao", "Sem status") if situacoes else "Sem status"
    
    return {
        "identificacao": projeto.get("identificacao"),
        "autor": projeto.get("documento", {}).get("resumoAutoria"),
        "ementa": projeto.get("conteudo", {}).get("ementa"),
        "explicacao": projeto.get("conteudo", {}).get("explicacaoEmenta"),
        "status_atual": status_atual,
        "tramitando": projeto.get("tramitando"),
        "casa_iniciadora": projeto.get("siglaCasaIniciadora"),
        "link_pdf": projeto.get("documento", {}).get("url"),
        "total_movimentacoes": len(informes)
    }

# Exemplo de uso
id_exemplo = 8047634
url_detalhe = f"https://legis.senado.leg.br/dadosabertos/processo/{id_exemplo}?v=1"

response = requests.get(url_detalhe, headers={"Accept": "application/json"})
if response.status_code == 200:
    dados_limpos = extrair_dados_essenciais(response.json())
    print(json.dumps(dados_limpos, indent=4, ensure_ascii=False))
```

---

## 🛠️ Tecnologias e Dependências
* **Linguagem:** Python 3.x
* **Biblioteca de Requests:** `pip install requests`
* **Formato de Saída:** JSON / Dicionário Python