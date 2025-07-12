## pseudocodigo slide 05 ##

from dataclasses import dataclass

TAM_MAX_BUCKET = 2  # colocando o tamanho máximo do bucket como 2

class Bucket:
    def __init__(self, profundidade):
        self.prof: int = profundidade #armazena a profundidade do bucket
        self.cont = 0
        self.chaves = []

class Diretorio:
    def __init__(self):
        self.refs: list = [] #lista de referencia(RRN) aos buckets
        self.prof_dir: int = 0