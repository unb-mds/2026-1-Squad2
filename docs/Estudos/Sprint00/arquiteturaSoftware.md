Fundamentos  de  Arquitetura  de  Software  
1.  O  que  é  Arquitetura  de  Software?  
A  arquitetura  de  software  é  a  estrutura  fundamental  de  um  sistema.  Ela  orienta  como  o  
software
 
é
 
construído,
 
como
 
ele
 
evolui
 
e
 
se
 
adapta,
 
definindo
 
padrões,
 
tecnologias,
 
camadas
 
de
 
aplicação
 
e
 
fluxos
 
de
 
comunicação.
 
É  de  extrema  importância  pensar  na  arquitetura  desde  o  "dia  zero"  do  projeto.  Escolhas  
arquitetônicas
 
erradas
 
no
 
início
 
podem
 
resultar
 
em
 
custos
 
altíssimos,
 
lentidão
 
nos
 
processos
 
e
 
muito
 
retrabalho
 
no
 
futuro.
 
Arquitetura  vs.  Design  de  Software:  É  muito  comum  confundir  esses  dois  termos.  A  
diferença
 
principal
 
é
 
o
 
foco:
 
●  Arquitetura:  Foca  em  alto  nível,  definindo  como  os  componentes  de  um  sistema  
interagem
 
entre
 
si
.
 ●  Design:  Concentra-se  nos  detalhes  de  implementação  desses  componentes,  
focando
 
em
 
algoritmos,
 
estruturas
 
de
 
dados
 
e
 
padrões
 
de
 
projeto
 
dentro
 
do
 
código
 
e
 
tecnologias.
 
 
2.  Padrões  de  Arquitetura  em  Foco  
Existem  diversas  abordagens  para  construir  um  sistema  (em  camadas,  orientado  a  eventos,  
etc.).
 
Abaixo,
 
focamos
 
nos
 
três
 
modelos
 
essenciais
 
para
 
o
 
nosso
 
escopo
 
de
 
estudo:
 
MVC,
 
SOA
 
e
 
Microsserviços.
 
A.  Model-View-Controller  (MVC)  (+simples,   -  escalável,  recomendado)  
O  MVC  é  um  padrão  clássico  e  amplamente  utilizado  que  foca  na  separação  de  
responsabilidades
 
dentro
 
do
 
código
 
de
 
uma
 
aplicação.
 
Ele
 
divide
 
o
 
sistema
 
em
 
três
 
componentes
 
que
 
interagem
 
entre
 
si:
 
●  Model  (Modelo):  É  o  coração  da  aplicação.  Gerencia  os  dados,  as  regras  de  
negócio,
 
basicamente
 
o
 
banco
 
de
 
dados.
 ●  View  (Visão):  É  a  interface  de  usuário  (o  front-end).  É  a  parte  responsável  por  exibir  
os
 
dados
 
formatados
 
na
 
tela
 
para
 
quem
 
está
 
usando
 
o
 
sistema.
 ●  Controller  (Controlador):  É  o  intermediário.  Ele  recebe  as  requisições  (cliques,  
digitações)
 
do
 
usuário
 
na
 
View,
 
solicita
 
as
 
operações
 
necessárias
 
ao
 
Model
 
e,
 
com
 
a
 
resposta,
 
atualiza
 
a
 
View.
 
Exemplo  prático:  Em  um  catálogo  de  filmes,  quando  o  usuário  clica  em  "Ver  Categorias",  a  
requisição
 
bate
 
no
 
Controller.
 
O
 
Controller
 
pede
 
ao
 
Model
 
para
 
buscar
 
a
 
lista
 
de
 
categorias
 

no  banco  de  dados.  O  Model  retorna  os  dados  brutos,  o  Controller  os  formata  e  envia  para  a  
View,
 
que
 
renderiza
 
o
 
HTML
 
na
 
tela
 
do
 
usuário.
 
B.  Arquitetura  Orientada  a  Serviços  (SOA)(+  complexo,  +  escalável)  
A  SOA  (Service-Oriented  Architecture)  é  uma  abordagem  de  nível  corporativo .  A  ideia  é  
criar
 
componentes
 
de
 
software
 
focados
 
em
 
recursos
 
de
 
negócios
 
(chamados
 
de
 
"serviços")
 
com
 
o
 
objetivo
 
principal
 
de
 
reutilização
 
por
 
diversas
 
aplicações
 
diferentes
 
dentro
 
de
 
uma
 
mesma
 
empresa.
 
●  Como  funciona:  Na  SOA,  os  serviços  costumam  ser  maiores  e  muitas  vezes  
compartilham
 
os
 
mesmos
 
bancos
 
de
 
dados
 
corporativos.
 
Eles
 
se
 
comunicam
 
quase
 
sempre
 
através
 
de
 
um
 
barramento
 
centralizado
 
chamado
 
ESB
 
(Enterprise
 
Service
 
Bus)
.
 
O
 
ESB
 
é
 
responsável
 
por
 
rotear
 
e
 
traduzir
 
as
 
mensagens
 
entre
 
serviços
 
construídos
 
em
 
linguagens
 
diferentes.
 ●  Exemplo  prático:  Uma  grande  rede  de  hospitais  tem  um  sistema  para  o  RH,  outro  
para
 
gestão
 
de
 
pacientes
 
e
 
outro
 
para
 
o
 
financeiro.
 
Em
 
vez
 
de
 
criar
 
uma
 
tela
 
de
 
login
 
separada
 
para
 
cada
 
um,
 
a
 
equipe
 
cria
 
um
 
único
 
"Serviço
 
de
 
Autenticação"
 
(SOA)
 
centralizado.
 
Todos
 
os
 
sistemas
 
da
 
empresa
 
usam
 
o
 
ESB
 
para
 
consultar
 
esse
 
mesmo
 
serviço.
 ●  Desvantagens:  O  ESB  pode  se  tornar  um  "ponto  único  de  falha"  e  um  gargalo  de  
desempenho.
 
Se
 
o
 
barramento
 
cair,
 
as
 
comunicações
 
da
 
empresa
 
inteira
 
param.
 
C.  Microsserviços  (++complexidade,  ++  escalabilidade)  
A  arquitetura  de  microsserviços  é  considerada  uma  evolução  do  modelo  SOA,  idealizada  
para
 
o
 
ambiente
 
de
 
computação
 
em
 
nuvem
 
(Cloud).
 
Em
 
vez
 
de
 
focar
 
em
 
reutilização
 
corporativa,
 
os
 
microsserviços
 
pegam
 
uma
 
única
 
aplicação
 
e
 
a
 
dividem
 
em
 
partes
 
extremamente
 
pequenas,
 
independentes
 
e
 
focadas
 
em
 
tarefas
 
únicas.
 
●  Como  funciona:  Diferente  da  SOA,  os  microsserviços  não  usam  um  ESB  central  
pesado.
 
Eles
 
se
 
comunicam
 
de
 
forma
 
direta
 
e
 
leve
 
através
 
de
 
APIs
 
(geralmente
 
RESTful).
 
A
 
regra
 
de
 
ouro
 
aqui
 
é
 
o
 
desacoplamento
:
 
cada
 
microsserviço
 
deve
 
ter
 
o
 
seu
 
próprio
 
banco
 
de
 
dados
 
isolado.
 
Mesmo
 
que
 
isso
 
gere
 
alguma
 
duplicação
 
de
 
dados,
 
garante
 
que
 
um
 
serviço
 
não
 
derrube
 
o
 
outro.
 ●  Exemplo  prático:  Em  um  aplicativo  de  delivery  (como  iFood),  você  teria  um  
microsserviço
 
independente
 
apenas
 
para
 
o
 
"Carrinho",
 
outro
 
para
 
o
 
"Catálogo
 
de
 
Restaurantes"
 
e
 
outro
 
para
 
o
 
"Pagamento".
 
Se
 
for
 
sexta-feira
 
à
 
noite
 
e
 
o
 
tráfego
 
do
 
"Catálogo"
 
explodir,
 
você
 
pode
 
colocar
 
mais
 
servidores
 
(escalar)
 
apenas
 
para
 
o
 
microsserviço
 
de
 
Catálogo,
 
sem
 
precisar
 
gastar
 
recursos
 
escalando
 
o
 
serviço
 
de
 
Pagamento.
 ●  Vantagens:  Escalabilidade  independente,  velocidade  de  deploy  (atualizar  um  
serviço
 
não
 
exige
 
parar
 
o
 
sistema
 
todo)
 
e
 
altíssima
 
resiliência.
 
 