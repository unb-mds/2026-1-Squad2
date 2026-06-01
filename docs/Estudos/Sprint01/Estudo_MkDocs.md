# MkDocs

## Estudo sobre o MkDocs

## 1. O que é

O **MkDocs** é um gerador de sites estáticos criados para a documentação de projetos. Ele transforma arquivos escritos em Markdown em um site HTML organizado e web.

Ele é escrito em Python e usa um arquivo de configuração YAML (`mkdocs.yml`) para organizar a documentação.

O MkDocs permite criar:

- Documentação técnica
- Documentação de projetos
- Manuais de sistemas
- Documentação de APIs
- Documentação acadêmica

## 2. Importância da documentação

A documentação é indispensável para garantir que outras pessoas entendam e consigam manter o projeto, principalmente quando membros da equipe não estão disponíveis. Quando não se tem a documentação, pode gerar dificuldade na continuidade das tarefas e compreensão do funcionamento do sistema.

O MkDocs surge justamente para:

- Facilitar a documentação de projetos Python
- Organizar documentação técnica
- Melhorar a manutenção do código
- Compartilhar aprendizados da equipe
- Criar documentação profissional de forma rápida

## 3. Como o MkDocs funciona

O fluxo de funcionamento do MkDocs é assim:

> Markdown → MkDocs → HTML → Site de documentação

Você escreve arquivos `.md`, configura o `mkdocs.yml`, e o MkDocs gera automaticamente o site.

**Principais características:**

- Usa Markdown
- Gera site estático
- Navegação automática
- Busca integrada
- Atualização automática
- Deploy simples

## 4. Estrutura de um projeto MkDocs

```
meu-projeto/
│
├── docs/
│   ├── index.md
│   ├── requisitos.md
│   ├── mkdocs.md
│
└── mkdocs.yml
```

A pasta `docs` contém todas as páginas da documentação.

## 5. Instalação do MkDocs

**Pré-requisitos:**

- Python instalado
- pip instalado
- terminal

**Como instalar:**

No bash:

```bash
pip install mkdocs
```

```bash
mkdocs new meu-projeto
```

```bash
cd meu-projeto
```

## 6. Como visualizar o site localmente

Para rodar localmente:

```bash
mkdocs serve
```

O site normalmente é exibido em:

```
http://127.0.0.1:8000
```

## 7. O arquivo de configuração mkdocs.yml

Esse arquivo define:

- Nome do site
- Menu
- Tema
- Plugins
- Navegação

**Exemplo:**

```yaml
site_name: Documentação do Projeto

nav:
  - Home: index.md
  - Requisitos: requisitos.md
  - MkDocs: mkdocs.md

theme:
  name: material
```

O tema **"Material for MkDocs"** é o mais usado. Esse tema adiciona:

- Menu lateral
- Busca
- Dark mode
- Responsivo
- Navegação moderna

```bash
pip install mkdocs-material
```

```yaml
theme:
  name: material
```

## 8. Criar páginas

As páginas são criadas com Markdown dentro da pasta `docs`.

**Exemplo:**

`index.md`

```markdown
# Documentação do Projeto

Bem vindo à documentação.

## Conteúdo

- Requisitos
- Arquitetura
- API
```

## 9. Menu lateral no MkDocs

Menu lateral configurado no `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Estudos:
      - Requisitos: requisitos.md
      - MkDocs: mkdocs.md
```

## 10. Gerando o site

Para gerar o site final:

```bash
mkdocs build
```

Será criada uma pasta `site/`, nela terá o site pronto para a publicação.

## 11. Vantagens e desvantagens

**Vantagens:**

- Fácil de usar
- Usa Markdown
- Layout profissional
- Navegação automática
- Busca integrada
- Deploy rápido
- Integração com GitHub
- Ideal para documentação técnica

**Desvantagens:**

- Não gera conteúdo dinâmico
- Precisa Python
- Customização avançada exige plugins

---

**Links usados:**

- <https://medium.com/data-hackers/documentando-projetos-python-com-mkdocs-c34d654192f0>
- <https://www.mkdocs.org/>
- <https://squidfunk.github.io/mkdocs-material/>
- <https://realpython.com/python-project-documentation-with-mkdocs/>
