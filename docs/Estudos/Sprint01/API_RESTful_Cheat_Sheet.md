# API RESTful Cheat Sheet

## O que é REST?

**REST (Representational State Transfer)** não é uma tecnologia, linguagem ou pacote, mas sim um **estilo de arquitetura** para sistemas web. Uma API é considerada RESTful quando segue estes princípios fundamentais:

- **Cliente-Servidor:** O frontend (cliente) e o backend (servidor) são totalmente separados. O cliente foca na interface e o servidor no armazenamento e regras de negócio.
- **Stateless (Sem Estado):** O servidor não guarda "memória" de requisições passadas do cliente. Cada requisição deve conter todas as informações (como tokens de autenticação) necessárias para ser processada de forma independente.
- **Baseado em Recursos:** Tudo na API é tratado como um "recurso" (ex: usuários, deputados, projetos de lei) e é acessado através de URLs padronizadas.
- **Interface Uniforme:** Uso semântico e correto dos métodos HTTP (GET para buscar, POST para criar, etc.) e retorno de dados em formatos universais, como o JSON.

---

## 1. Métodos HTTP (O que você quer fazer?)

| Método  | Ação (CRUD) | Descrição                                                     | É Idempotente?* |
|---------|-------------|---------------------------------------------------------------|-----------------|
| GET     | Read        | Recupera dados de um servidor. Nunca deve alterar o estado.   | Sim             |
| POST    | Create      | Envia dados para o servidor criar um novo recurso.            | Não             |
| PUT     | Update      | Substitui completamente um recurso existente pelos novos dados. | Sim           |
| PATCH   | Update      | Aplica modificações parciais a um recurso existente.          | Não             |
| DELETE  | Delete      | Remove um recurso específico do servidor.                     | Sim             |

> *\* **Idempotência:** Fazer a mesma requisição várias vezes tem o mesmo efeito no servidor que fazer apenas uma vez.*

---

## 2. HTTP Status Codes (O que aconteceu?)

### 2xx: Sucesso

- `200 OK` — Requisição bem-sucedida.
- `201 Created` — Recurso criado com sucesso.
- `204 No Content` — Sucesso, mas sem corpo de resposta.

### 4xx: Erro do Cliente

- `400 Bad Request` — Sintaxe inválida ou dados faltando no corpo.
- `401 Unauthorized` — Falta de autenticação ou token inválido.
- `403 Forbidden` — Autenticado, mas sem permissão para a ação.
- `404 Not Found` — O endpoint ou recurso não existe.

### 5xx: Erro do Servidor

- `500 Internal Server Error` — Erro no código do backend (crash).
- `503 Service Unavailable` — Servidor offline/sobrecarregado.

---

## 3. Passagem de Parâmetros e Headers

- **Path Parameters (Rota):** Identificam um recurso específico. Ex: `/deputados/123`
- **Query Parameters (Consulta):** Usados para filtros e paginação. Ex: `/deputados?siglaUf=SP&pagina=1`
- **Content-Type:** Diz ao servidor o formato do corpo da mensagem (geralmente `application/json`).
- **Authorization:** Envia credenciais de acesso (Ex: `Bearer eyJhbGci...`).

---

## Exemplos Práticos (Criação e Consumo)

### Python

#### 1. Criando uma API (com FastAPI)

```python
# Instalação: pip install fastapi uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/deputados/{id_deputado}")
def obter_deputado(id_deputado: int):
    return {
        "id": id_deputado,
        "nome": "João da Silva",
        "partido": "Tech"
    }

# Rodar o servidor: uvicorn nome_do_arquivo:app --reload
```

#### 2. Consumindo uma API (com `requests`)

```python
# Instalação: pip install requests
import requests

url = "https://dadosabertos.camara.leg.br/api/v2/deputados/204554"
response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    info = dados['dados']
    print(f"Nome civil: {info['nomeCivil']}")
else:
    print(f"Falha na requisição. Status: {response.status_code}")
```

### JavaScript (Node.js / Frontend)

#### 1. Criando uma API (com Express.js)

```javascript
// Instalação: npm install express
const express = require('express');
const app = express();

app.use(express.json()); // Permite ler JSON no corpo da requisição

app.post('/api/v1/projetos', (req, res) => {
    const novoProjeto = req.body;

    res.status(201).json({
        mensagem: "Projeto cadastrado com sucesso!",
        projeto: novoProjeto
    });
});

app.listen(3000, () => console.log('API rodando na porta 3000'));
```

#### 2. Consumindo uma API (com `Fetch API`)

```javascript
async function buscarDeputado() {
    const url = "https://dadosabertos.camara.leg.br/api/v2/deputados/204554";

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

        const json = await response.json();
        console.log(`Nome: ${json.dados.ultimoStatus.nome}`);

    } catch (error) {
        console.error("Falha ao buscar dados:", error);
    }
}

buscarDeputado();
```

### Java (Consumo Nativo)

#### Consumindo com `HttpClient` (Java 11+)

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ConsumoApi {
    public static void main(String[] args) throws Exception {
        String url = "https://dadosabertos.camara.leg.br/api/v2/deputados?itens=1";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Accept", "application/json")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println("Status: " + response.statusCode());
        System.out.println("Body: " + response.body());
    }
}
```
