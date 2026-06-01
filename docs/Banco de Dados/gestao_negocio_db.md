
# Gestão de Negócio do Banco de Dados

A extração, tratamento e armazenamento dos dados referentes aos Projetos de Lei (PLs), Tramitações, Autores e Parlamentares no Mapa L.I.L.A.S é gerenciada por um conjunto de três camadas de serviços no backend (localizados em `backend/app/services`): **Clients**, **Normalizer** e **Collector**.

Esses arquivos trabalham em conjunto para garantir que os dados provenientes da Câmara dos Deputados e do Senado Federal sejam consultados, limpos, padronizados e salvos corretamente no banco de dados.

Abaixo, detalhamos a responsabilidade e o funcionamento de cada um desses arquivos.

---

## 1. Clients (`camara_client.py` e `senado_client.py`)

Os clients são estritamente responsáveis pela **comunicação com as APIs externas**.

**Principais características:**

* **Responsabilidade Única:** Fazer requisições HTTP e retornar o JSON bruto fornecido pelas APIs. Eles não salvam no banco de dados e não realizam transformações complexas de modelos de dados.

* **Configuração Base:** Contêm as URLs base, `TIMEOUT`, paginação (no caso da Câmara) e as **palavras-chave** da pesquisa (ex: `"feminicídio"`, `"violência doméstica"`, `"direitos da mulher"`), além das siglas (ex: `"PL"`, `"PLP"`, `"PLS"`).

* **Funções principais:**

    * Pesquisar matérias/proposições ativas.

    * Buscar detalhes de uma matéria específica.

    * Buscar autores e tramitações de uma matéria.

    * Buscar dados detalhados de parlamentares (com cache simples em memória, `_cache_deputados` e `_cache_senadores`, para evitar chamadas duplicadas às APIs externas).

* **Tratamento de Erros Base:** Em caso de indisponibilidade da API, eles capturam as exceções de conexão (`requests.exceptions.RequestException`) e evitam a quebra do sistema retornando listas ou dicionários vazios para a camada superior.

    ```python

    try:

        resp = requests.get(url, params=params, timeout=TIMEOUT)

        resp.raise_for_status()

        return resp.json()

    except requests.exceptions.RequestException as exc:

        logger.warning("API indisponível [%s]: %s", url, exc)

        return None

    ```

---

## 2. Normalizer (`normalizer.py`)

O `normalizer.py` atua como a **camada de transformação de dados**. Ele recebe as respostas brutas ("payloads") entregues pelos clients e os converte em objetos e registros do nosso banco de dados.

**Principais características:**

* **Mapeamento para o Banco de Dados:** Ele importa os modelos SQLAlchemy (`PlCamara`, `PlSenado`, `AutoriaCamara`, `Parlamentar`, etc.) e garante que os dados extraídos das APIs "encaixem" perfeitamente no formato das tabelas.

* **Limpeza e Higienização:**

    * Possui funções como `higienizar_para_jsonb` para garantir que campos flexíveis no banco de dados (`JSONB`) recebam dicionários válidos em Python.

    * Tratamento de campos específicos, como `limpar_sexo`, que garante que as strings recebidas (que variam de formato nas APIs) virem apenas `"M"` ou `"F"`.

* **Upsert de Dados:** Utiliza a operação de `session.merge()` para garantir que um dado não seja inserido de forma duplicada. Se o registro já existir, ele é atualizado; se não, é criado (operação de "Update/Insert" ou Upsert).

    ```python

    nova_tramitacao = TramitacaoCamara(
        id_pl=id_pl,
        data_tramitacao=tramitacao.get("dataHora"),
        situacao=tramitacao.get("descricaoSituacao"),
        # ... outros campos mapeados

    )
    session.merge(nova_tramitacao) # Faz o upsert no banco

    ```

* **Estruturação Robusta (`navegar_seguro`):** As APIs do Senado e da Câmara muitas vezes retornam listas em alguns casos e dicionários em outros. O normalizer possui funções de navegação segura para extrair os campos independentemente de como a API envia a resposta (evitando o erro clássico de acessar índices em dicionários ou chaves em listas).

* **Padronização de Status para o Frontend:** As funções finais (`normalizar_status_camara` e `normalizar_status_senado`) convertem a miríade de status governamentais complicados ("Transformado em Norma Jurídica", "Retirado pelo Autor", "Arquivado Fim Legislatura") em três valores simples esperados pelo nosso frontend: `"aprovado"`, `"arquivado"` ou `"em_tramitacao"`.

---

## 3. Collector (`collector.py`)

O `collector.py` é o **orquestrador mestre**. Ele usa as ferramentas descritas acima em conjunto, coordenando o fluxo de "Extrair (Client) → Transformar (Normalizer) → Carregar (Banco)".

**Principais características:**

* **Regras de Negócio e Anti-Duplicação:**

    * Ele itera sobre todas as combinações de tipos (PL, PLP, PLS) e palavras-chave.

    * *Câmara:* Antes de inserir um PL da Câmara, o Collector busca seus autores. Se ele identificar `"Senado Federal"` na autoria, ele **ignora e descarta o PL**. Isso porque um PL do Senado já será capturado pelo coletor do Senado, evitando assim que PLs que transitam entre as duas casas sejam duplicados.

      ```python

      ignorar_pl = False

      for autor in autores_raw:
          if "Senado Federal -" in autor.get("nome", ""):
              ignorar_pl = True
              break

      if ignorar_pl:
          logger.info("Câmara — ignorando PL %s (Origem: Senado)", pl_id)
          continue

      ```

    * *Senado:* A mesma lógica é aplicada inversamente. Se a autoria indica `"Câmara dos Deputados"`, o PL é ignorado na coleta do Senado.

* **Passo a passo por PL:**

    1. Busca a lista de matérias no Client.

    2. Aplica o filtro Anti-Duplicação.

    3. Busca os dados da proposição, salva via Normalizer.

    4. Busca detalhes de Parlamentares/Autores (enriquecendo a busca), salva via Normalizer.

    5. Busca as tramitações, salva via Normalizer.

    6. Comita as mudanças no banco de dados (`session.commit()`).

* **Automação e Agendamento (Incremental):**

    * O arquivo implementa o `loop_coleta` (usando `asyncio.sleep()`), que permite que a coleta seja um processo assíncrono que roda no servidor a cada `INTERVALO_HORAS` (por padrão, 2 horas).

    * Executa apenas de forma incremental (`numdias=1` para o Senado, pegando apenas dados recentes) durante as varreduras recorrentes.