# API de Dados Abertos do Senado Federal

## Visão Geral

A API de Dados Abertos do Senado Federal disponibiliza informações públicas do Senado Brasileiro através de endpoints REST acessíveis via HTTP.

Documentação oficial:

* [https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html#/](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html#/)

Base URL:

```txt
https://legis.senado.leg.br/dadosabertos
```

A API permite acessar informações como:

* Senadores
* Projetos de lei
* Matérias legislativas
* Votações
* Sessões plenárias
* Discursos
* Comissões
* Mandatos
* Tramitações
* Estrutura legislativa

---

# Características da API

| Característica | Valor               |
| -------------- | ------------------- |
| Tipo           | REST API            |
| Autenticação   | Não necessita       |
| Formatos       | JSON e XML          |
| Documentação   | Swagger UI          |
| Dados          | Públicos e oficiais |
| Acesso         | Gratuito            |

---

# Estrutura Geral da API

Os endpoints seguem um padrão semelhante a:

```txt
/recurso/acao/formato
```

Exemplos:

```txt
/senador/lista/atual.json
/materia/123456.json
/comissao/lista.json
```

---

# Como Utilizar

## Requisição Básica

Exemplo utilizando navegador:

```txt
https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json
```

---

# Principais Recursos da API

# 1. Senadores

## Listar senadores em exercício

Endpoint:

```http
GET /senador/lista/atual.json
```

URL completa:

```txt
https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json
```

### Objetivo

Retorna todos os senadores atualmente em exercício.

### Exemplo de resposta

```json
{
  "ListaParlamentarEmExercicio": {
    "Parlamentares": {
      "Parlamentar": [
        {
          "IdentificacaoParlamentar": {
            "CodigoParlamentar": "4981",
            "NomeParlamentar": "Nome Exemplo",
            "SiglaPartidoParlamentar": "PL",
            "UfParlamentar": "DF"
          }
        }
      ]
    }
  }
}
```

---

## Buscar senador por código

Endpoint:

```http
GET /senador/{codigo}.json
```

Exemplo:

```txt
https://legis.senado.leg.br/dadosabertos/senador/4981.json
```

### Informações retornadas

* Nome parlamentar
* Partido
* Estado
* Mandato
* Dados pessoais públicos
* Contatos institucionais
* Histórico parlamentar

---

## Mandatos do senador

Endpoint:

```http
GET /senador/{codigo}/mandatos.json
```

Exemplo:

```txt
https://legis.senado.leg.br/dadosabertos/senador/4981/mandatos.json
```

---

## Discursos do senador

Endpoint:

```http
GET /senador/{codigo}/discursos.json
```

---

# 2. Matérias Legislativas

As matérias representam projetos de lei, PECs, requerimentos e demais documentos legislativos.

## Buscar matéria por código

Endpoint:

```http
GET /materia/{codigo}.json
```

Exemplo:

```txt
https://legis.senado.leg.br/dadosabertos/materia/123456.json
```

### Dados retornados

* Tipo da matéria
* Número
* Ano
* Ementa
* Autor
* Situação atual
* Tramitação
* Relator
* Comissão atual

---

## Pesquisa de matérias

Endpoint:

```http
GET /materia/pesquisa
```

### Possíveis usos

* Buscar projetos por palavra-chave
* Filtrar por ano
* Filtrar por autor
* Filtrar por tipo

---

# 3. Votações

## Consultar votação

Endpoint:

```http
GET /votacao/{codigo}.json
```

### Dados disponíveis

* Resultado da votação
* Votos individuais
* Senadores participantes
* Tipo de votação
* Sessão relacionada

---

# 4. Comissões

## Listar comissões

Endpoint:

```http
GET /comissao/lista.json
```

### Dados disponíveis

* Nome da comissão
* Sigla
* Tipo
* Participantes
* Presidência

---

# 5. Sessões Plenárias

A API também disponibiliza informações sobre sessões legislativas.

### Informações disponíveis

* Data
* Ordem do dia
* Participantes
* Votações realizadas
* Pronunciamentos

---

# Estrutura das Respostas JSON

A API utiliza estruturas JSON bastante aninhadas.

Exemplo simplificado:

```json
{
  "ObjetoPrincipal": {
    "SubObjeto": {
      "Lista": {
        "Item": [
          {
            "Campo": "Valor"
          }
        ]
      }
    }
  }
}
```

---

# Pontos Importantes para Desenvolvedores

## 1. Estrutura Profundamente Aninhada

Os retornos da API possuem muitos níveis.

Exemplo:

```json
{
  "ListaParlamentarEmExercicio": {
    "Parlamentares": {
      "Parlamentar": []
    }
  }
}
```

Por isso, normalmente será necessário:

* Mapear os dados
* Criar DTOs
* Fazer transformação de resposta
* Criar adaptadores

---

## 2. Padronização Parcial

Alguns endpoints possuem padrões diferentes.

Recomenda-se:

* Criar camada de abstração
* Centralizar chamadas HTTP
* Criar serviços específicos

---

## 3. Performance

Algumas respostas podem ser grandes.

Boas práticas:

* Implementar cache
* Utilizar paginação quando disponível
* Evitar chamadas repetidas
* Armazenar dados processados localmente

---

# Exemplos de Consumo

# JavaScript (Fetch API)

```javascript
fetch('https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json')
  .then(response => response.json())
  .then(data => {
    console.log(data)
  })
  .catch(error => {
    console.error(error)
  })
```

---

# Axios (JavaScript)

```javascript
import axios from 'axios'

async function buscarSenadores() {
  try {
    const response = await axios.get(
      'https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json'
    )

    console.log(response.data)
  } catch (error) {
    console.error(error)
  }
}
```

---

# Python

```python
import requests

url = 'https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json'

response = requests.get(url)

print(response.json())
```

---

# Java (Spring Boot)

```java
RestTemplate restTemplate = new RestTemplate();

String url = "https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json";

Object response = restTemplate.getForObject(url, Object.class);

System.out.println(response);
```

---

# Arquitetura Recomendada

Para aplicações profissionais, recomenda-se utilizar:

```txt
[Frontend]
     ↓
[Backend Próprio]
     ↓
[API Senado]
```

## Vantagens dessa abordagem

### Backend intermediário

Permite:

* Normalizar respostas
* Melhorar performance
* Criar cache
* Evitar chamadas excessivas
* Filtrar dados
* Criar autenticação própria
* Centralizar regras de negócio

---

# Exemplos de Projetos Possíveis

## Dashboard Legislativo

Exibir:

* Projetos em tramitação
* Votações recentes
* Atividade parlamentar
* Estatísticas políticas

---

## Sistema de Transparência

Permite:

* Monitoramento legislativo
* Acompanhamento de senadores
* Histórico de votações

---

## Aplicativos Mobile

Possibilidades:

* Alertas de projetos
* Agenda legislativa
* Notícias parlamentares

---

# Boas Práticas

## 1. Criar Serviços Isolados

Exemplo:

```txt
/services
  senadorService.js
  materiaService.js
  votacaoService.js
```

---

## 2. Criar Tipagem

TypeScript:

```typescript
interface Senador {
  codigo: string
  nome: string
  partido: string
  uf: string
}
```

---

## 3. Implementar Tratamento de Erros

Exemplo:

```javascript
try {
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error('Erro na requisição')
  }

} catch(error) {
  console.error(error)
}
```

---

# Limitações da API

## Estrutura antiga

A API não segue completamente padrões REST modernos.

---

## Respostas complexas

Os retornos possuem:

* Muitos níveis
* Chaves extensas
* Estruturas pouco padronizadas

---

## Falta de paginação clara

Alguns endpoints retornam grandes volumes de dados.

---

# Swagger UI

A documentação Swagger permite:

* Testar endpoints
* Visualizar parâmetros
* Ver modelos de resposta
* Simular requisições

Link:

```txt
https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html#/
```

---

# Fluxo de Desenvolvimento Recomendado

## Etapa 1

Explorar endpoints via Swagger.

## Etapa 2

Testar chamadas no Postman.

## Etapa 3

Criar camada de serviços.

## Etapa 4

Mapear respostas da API.

## Etapa 5

Implementar cache e otimizações.

---

# Segurança

Mesmo sendo uma API pública:

* Limite requisições
* Implemente cache
* Evite expor diretamente a API ao frontend

---

# Conclusão

A API de Dados Abertos do Senado Federal é uma solução extremamente útil para aplicações de transparência pública, análise legislativa e monitoramento político.

Apesar da estrutura relativamente complexa, a API oferece uma quantidade muito rica de informações oficiais do Senado Brasileiro.

Para aplicações profissionais, recomenda-se utilizar uma camada intermediária de backend para normalização e otimização das respostas.

---

# Links Úteis

## Swagger Oficial

[https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html#/](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html#/)

## Portal de Dados Abertos do Senado

[https://www12.senado.leg.br/dados-abertos](https://www12.senado.leg.br/dados-abertos)

## Lei de Acesso à Informação

[https://www.gov.br/acessoainformacao](https://www.gov.br/acessoainformacao)
