# 👩‍💻 Persona: A Jornalista de Dados

Com base na pesquisa inicial realizada com o nosso público-alvo (jornalistas e pesquisadores do meio político), estruturamos a **Persona** central que guiará as decisões de UX e desenvolvimento do **Mapa L.I.L.A.S**.

---

## 📌 Perfil Biográfico

**Nome Fictício:** Marina Alves  
**Idade:** 34 anos  
**Ocupação:** Jornalista Investigativa e Analista de Dados Políticos  
**Contexto:** Marina atua cobrindo pautas sobre direitos humanos e legislação na política nacional. O seu dia a dia consiste em investigar a eficácia e a movimentação de projetos de lei em Brasília.

### Personalidade
*   **Analítica:** Toma decisões embasadas em dados estatísticos e fontes oficiais.
*   **Ágil:** Precisa de informações rápidas devido à dinâmica do jornalismo (furos de reportagem).
*   **Crítica:** Cética em relação a promessas políticas vazias; ela quer ver os dados de aprovação.

---

## 🧠 Mapa Mental da Persona

Abaixo está o diagrama (Mindmap) que resume a psique da nossa Persona em relação ao domínio da plataforma:

```mermaid
graph LR
    P((👩‍💻 Marina<br/>Jornalista de Dados))
    
    P --> I{❤️ Interesses}
    I --> I1[Acesso Transparente]
    I --> I2[Métricas da Câmara e Senado]
    I --> I3[Cruzamento Regional/Partidário]
    
    P --> N{⭐ Necessidades}
    N --> N1[Dashboards em Tempo Real]
    N --> N2[Busca Textual Robusta]
    N --> N3[Exportação de Relatórios]
    
    P --> D{⚠️ Dores}
    D --> D1[Sites Gov Arcaicos]
    D --> D2[Dificuldade de Rastreio de PLs]
    D --> D3[Informação Não-Estruturada]

    %% Estilização ajustada para o modo escuro (Slate)
    classDef central fill:#7e57c2,stroke:#fff,stroke-width:3px,color:#fff,font-weight:bold;
    classDef categoria fill:#5e35b1,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold;
    classDef item fill:#311b92,stroke:#b39ddb,stroke-width:1px,color:#fff;

    class P central;
    class I,N,D categoria;
    class I1,I2,I3,N1,N2,N3,D1,D2,D3 item;
```

---

## 🎯 Aprofundamento

<div class="grid cards" markdown>

-   ❤️ **Interesses**
    ---
    * Ter acesso consolidado às bases governamentais sobre a pauta do Feminicídio.
    * Entender quais partidos e estados são mais ativos em proposições femininas.
    * Acompanhar as comissões e votações ativas semanalmente.

-   ⭐ **Necessidades e Expectativas**
    ---
    * Um portal que consolide **Senado e Câmara** em uma única pesquisa.
    * Painéis que tragam os dados mastigados e prontos para publicar (Gráficos exportáveis).
    * Notificações visuais ou filtros fáceis para leis aprovadas recentemente.

-   ⚠️ **Dores e Frustrações**
    ---
    * Gasta horas do dia acessando múltiplos sites do governo com usabilidade ruim.
    * Os textos dos projetos muitas vezes são longos e escondem as reais intenções da lei.
    * É difícil justificar suas pautas para o editor chefe sem dados visuais de impacto.

</div>

---
<sub>Pesquisa e estruturação original idealizada por **Luana Barbosa** ([@Lulu-souza](https://github.com/Lulu-souza)), adaptada para formato sem imagens para otimização da documentação.</sub>
