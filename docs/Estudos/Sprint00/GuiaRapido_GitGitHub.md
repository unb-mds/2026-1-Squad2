# Guia Rápido: Git e GitHub
> Configuração, Comandos Essenciais e Fluxo de Trabalho em Equipe

---

## 1. Instalação e Configuração

- **Windows:** Baixe e instale pelo site oficial (git-scm.com).
- **Linux:** `sudo apt install git`

**Identificação** (rode no terminal uma vez):

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

Isso vincula seus commits à sua conta do GitHub.

---

## 2. Comandos Essenciais (Terminal)

```bash
git clone [url-do-repositorio]
```
Baixa o projeto. Use apenas ao entrar no projeto.

```bash
git pull
```
Puxa as últimas atualizações. Rode sempre que for fazer algo.

```bash
git add .
```
Prepara (staging) todos os arquivos alterados.

```bash
git commit -m "feat: adiciona login"
```
Salva suas alterações localmente com uma mensagem.

```bash
git push
```
Envia seus commits locais para o GitHub.

```bash
git checkout -b [nome-da-branch]
```
Cria e muda para uma nova ramificação paralela.

---

## 3. Padrão de Commits

- `feat:` Nova funcionalidade (ex: botão novo).
- `fix:` Correção de um bug/erro.
- `docs:` Alteração na documentação (README).
- `refactor:` Melhoria no código sem alterar o que ele faz.

---

## 4. Usando o VSCode (Source Control)

Você pode fazer tudo sem digitar comandos usando a aba **Source Control** (ícone de ramificação na barra lateral esquerda ou `Ctrl+Shift+G`):

- **Staging (`git add`):** Passe o mouse sobre um arquivo modificado e clique no símbolo `+` para adicioná-lo.
- **Commit:** Digite a mensagem na caixa de texto superior e clique no botão **Commit**.
- **Push / Pull:** Clique no botão **Sync Changes** (Sincronizar Alterações) que aparece após o commit para enviar e receber código de uma vez.
- **Mudar de Branch:** Clique no nome da branch atual na barra inferior (canto esquerdo) do VSCode para criar ou trocar de branch.

---

## 5. Resolução de Conflitos (Merge Conflicts)

Acontece quando duas pessoas alteram a mesma linha de código. O Git pausará a ação e avisará sobre o conflito.

1. Abra o VSCode. Os arquivos em conflito estarão marcados em vermelho com um "C".
2. Ao abrir o arquivo, o VSCode destacará o conflito com opções clicáveis acima do código:
   - **Accept Current Change:** Mantém o SEU código.
   - **Accept Incoming Change:** Mantém o código do COLEGA.
   - **Accept Both Changes:** Mantém os dois (você precisará arrumar manualmente depois).
3. Após escolher, salve o arquivo, faça o Staging (`+`) e crie um Commit para finalizar o merge.

---

## 6. Boas Práticas da Equipe

- **Sincronize antes:** `git pull` na main evita conflitos.
- **Commits menores:** Commits pequenos e assertivos são melhores. Prefira vários pequenos do que um gigante.
- **Evite commits na main:** Crie uma branch para sua tarefa. Ao terminar, abra um **Pull Request (PR)**.

> **Regra Importante:** Se o código quebrou ou apagou algo, relaxe! O Git guarda o histórico. Avise a equipe, e não force comandos.