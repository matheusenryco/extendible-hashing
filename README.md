##Implementação completa de Hashing Extensível

Este projeto faz parte como trabalho da disciplina de **Organização e Recuperação de Dados**, do curso de **Engenharia de Software** da **Universidade Estadual de Maringá**, em Maringá, Paraná, Brasil.

O projeto implementa um sistema de Hashing Extensível completo, com as seguintes funcionalidades:

* **Key Manipulation Operations**
    * **Insertion:** Adds new keys to the structure, with handling to prevent duplicate key insertion.
    * **Search:** Efficiently verifies if a key exists and locates its bucket.
    * **Removal:** Deletes existing keys from the data structure.

* **Dynamic Structure Management**
    * **Bucket Splitting:** When a bucket reaches its maximum capacity, its content is redistributed to a new bucket, and directory pointers are updated.

    * **Directory Doubling:** The directory automatically doubles in size when the depth of a bucket to be split reaches the global depth.

    * **Bucket Merging:** After key removal, the system attempts to merge "buddy buckets" (bucket pairs) if the combined number of keys does not exceed maximum capacity.

    * **Redução de Diretório:** Após uma fusão bem-sucedida, o sistema verifica se o diretório pode ser reduzido pela metade, diminuindo a profundidade global.

* **Management and Interface**
    * **Initialization and Management:** The system can create a new structure from scratch or load an existing one. All changes are saved at the end of execution to binary files.

    * **Command Line Interface:** The program is fully controlled by terminal arguments to execute operations and diagnostics.

    * **Diagnostic Functions:** Tools to print the current directory state and detailed bucket contents.

## How to Run

The program is controlled via command line, using flags to trigger different functionalities.

#### 1. Execução de operações (`-e`)
Esta é a principal funcionalidade do programa. Ela processa um arquivo de texto que contém uma sequência de
operações de inserção, busca e remoção.

A execução do arquivo de operações será acionada pela linha de comando, no seguinte formato:

**Python complete_hash.py -e arquivo operacoes.txt**

#### Operations file format    
The operations file will have one command per line, consisting of an operation identifier character followed by a space and the key (an integer).
- **i <key>**: Inserts the key into the hash. Duplicate key insertion will not be allowed.
- **b <key>**: Searches for the key, informing if it was found and in which bucket it is located.
- **r <key>**: Removes the key from the hash.

Below is an example of an operations file format.
```txt
i 20
i 4
i 12
i 20
b 12
r 4
b 4
r 99
```

Based on the operations file shown above, the program should present the following output:

```txt 
> Key 20 insertion: Success. 
> Key 4 insertion: Success.
> Key 12 insertion: Success. 
> Key 20 insertion: Failed – Duplicate key.
> Search for key 12: Key found in bucket 2.
> Key 4 removal: Success.
> Search for key 4: Key not found.
> Key 99 removal: Failed – Key not found.
```

#### 2. Directory printing (`-pd`)
This functionality displays the current directory state. Directory printing is also accessed via command line, in the following format:

```txt
$ python complete_hash.py -pd
```

As an example, the program should present the following information about the directory:
```txt
----- Directory -----
dir[0] = bucket[0]
dir[1] = bucket[0]
dir[2] = bucket[1]
dir[3] = bucket[2]

Depth = 2
Current size = 4
Total buckets = 3
```

Whenever activated, this functionality will display on screen the content of all directory cells, in addition to the following information: 
- (a) depth
- (b) current size
- (c) total number of referenced buckets.

### 3. Impressão dos buckets (`-pb`)
Essa funcionalidade exibe o conteúdo dos buckets ativos no arquivo buckets.dat. Ela também será acessada via linha de comando, no seguinte formato:
**Python complete_hash.py -pb**

### DISCLAIMER
When changing the TAM_MAX_BUCKET global variable, you must delete the **diretorio.dat*** and ***buckets.dat files***. Afterwards, the hashing structure must be recreated by running the program with an operations file, for example: 

```txt
python complete_hash.py -e op60.txt. 
```

This ensures the correct functionality of all operations, including the diagnostic flags (-pd and -pb).