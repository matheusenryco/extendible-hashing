##Implementação completa de Hashing Extensível

Este projeto faz parte como trabalho da disciplina de **Organização e Recuperação de Dados**, do curso de **Engenharia de Software** da **Universidade Estadual de Maringá**, em Maringá, Paraná, Brasil.

O projeto implementa um sistema de Hashing Extensível completo, com as seguintes funcionalidades:

* **Operações de Manipulação de Chaves**
    * **Inserção:** Adiciona novas chaves à estrutura, com tratamento para impedir a inserção de chaves duplicadas.
    * **Busca:** Verifica eficientemente se uma chave existe e localiza seu bucket.
    * **Remoção:** Exclui chaves existentes da estrutura de dados.

* **Gerenciamento Dinâmico da Estrutura**
    * **Divisão de Buckets (Split):** Quando um bucket atinge sua capacidade máxima, seu conteúdo é redistribuído para um novo bucket, e os ponteiros do diretório são atualizados.

    * **Duplicação de Diretório:** O diretório dobra de tamanho automaticamente quando a profundidade de um bucket a ser dividido alcança a profundidade global.

    * **Combinação de Buckets (Merge):** Após a remoção de uma chave, o sistema tenta juntar "buddy buckets" (pares de buckets) se o número combinado de chaves não exceder a capacidade máxima.

    * **Redução de Diretório:** Após uma fusão bem-sucedida, o sistema verifica se o diretório pode ser reduzido pela metade, diminuindo a profundidade global.

* **Gerenciamento e Interface**
    * **Inicialização e Gerenciamento:** O sistema pode criar uma nova estrutura do zero ou carregar uma existente. Todas as alterações são salvas ao final da execução nos arquivos binários.

    * **Interface por Linha de Comando:** O programa é totalmente controlado por argumentos no terminal para executar operações e diagnósticos.

    * **Funções de Diagnóstico:** Ferramentas para imprimir o estado atual do diretório e o conteúdo detalhado dos buckets.

## Como Executar

O programa é controlado via linha de comando, utilizando flags para acionar as diferentes funcionalidades.

#### 1. Execução de operações (`-e`)
Esta é a principal funcionalidade do programa. Ela processa um arquivo de texto que contém uma sequência de
operações de inserção, busca e remoção.

A execução do arquivo de operações será acionada pela linha de comando, no seguinte formato:

**Python complete_hash.py -e arquivo operacoes.txt**

#### Formato do arquivo de operações    
O arquivo de operações terá um comando por linha, consistindo em um caractere identificador da operação seguido
de um espaço e a chave (um número inteiro).
    * i <chave>: Insere a chave no hashing. Não será permitida a inserção de chaves duplicadas.
    * b <chave>: Busca pela chave, informando se foi encontrada e em qual bucket ela está.
    * r <chave>: Remove a chave do hashing.

A seguir é exemplificado o formato de um arquivo de operações.
<pre> ```txt i 20 i 4 i 12 i 20 b 12 r 4 b 4 r 99 ``` </pre>

Com base no arquivo de operações mostrado acima, o programa deverá apresentar a seguinte saída:

<pre> ``` Inserção da chave 20: Sucesso. Inserção da chave 4: Sucesso. Inserção da chave 12: Sucesso. Inserção da chave 20: Falha – Chave duplicada. Busca pela chave 12: Chave encontrada no bucket 2. Remoção da chave 4: Sucesso. Busca pela chave 4: Chave não encontrada. Remoção da chave 99: Falha – Chave não encontrada. ``` </pre>

#### 2. Impressão do diretório (`-pd`)
Essa funcionalidade exibe o estado atual do diretório. A impressão do diretório também será acessada via linha de comando, no seguinte formato:

**Python complete_hash.py -pd**

Sempre que ativada, essa funcionalidade apresentará na tela o conteúdo de todas as células do diretório, além das seguintes informações: (a) profundidade; (b) tamanho atual; e (c) número total de buckets referenciados.

### 3. Impressão dos buckets (`-pb`)
Essa funcionalidade exibe o conteúdo dos buckets ativos no arquivo buckets.dat. Ela também será acessada via linha de comando, no seguinte formato:
**Python complete_hash.py -pb**