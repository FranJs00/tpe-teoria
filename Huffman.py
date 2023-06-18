from collections import Counter
import heapq
import os

EPSILON = 0.00005
PRUEBAS_MINIMAS = 10000

class HuffmanNode:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = '' #guarda unico bit q corresponde a la rama del nodo (0 o 1)

    def __lt__(self, other):
        return self.freq < other.freq


class Huffman():
    def __init__(self):
        self.raw_data = ''
        self.codes = {} #dict que guarda la codificacion de cada simbolo <simbolo,cod>
        self.prob = {} #dict que guarda la probabilidad de cada simbolo
        self.root = None
        self.huff_avg_len = 0
        self.code_total_legth = 0
        self.source_code_size = 0

    def loadFile(self, file):
        with open(file, 'r') as f:
            data = f.read()

        # Se guarda el peso del archivo directamente despues de leerlo en bits
        self.source_code_size = os.path.getsize(file) * 8
        self.raw_data = data.replace("\n", " ").split(" ")

        self.__calculate_probability_distribution()

    def __calculate_probability_distribution(self):
        count = Counter(self.raw_data)
        total_values = len(self.raw_data)
        relative_frequency = {value: occurrences / total_values for value, occurrences in count.items()}

        sum_frequencies = sum(relative_frequency.values())
        probability_distribution = {value: frequency / sum_frequencies for value, frequency in relative_frequency.items()}

        self.prob = probability_distribution

    def buildTree(self):
        nodes = []
        keys = list(self.prob.keys())
        values = list(self.prob.values())

        for x in range(len(self.prob)):
            heapq.heappush(nodes, HuffmanNode(values[x], keys[x]))

        while len(nodes) > 1:
            left = heapq.heappop(nodes)
            right = heapq.heappop(nodes)
            left.huff = 0
            right.huff = 1
            newNode = HuffmanNode(left.freq + right.freq, left.symbol + right.symbol, left, right)
            heapq.heappush(nodes, newNode)

        self.root = nodes[0]
    
    def printNodes(self):
        self.__printNodes(self.root)

    def __printNodes(self, node, val = ''):
        newVal = val + str(node.huff)
    
        if(node.left):
            self.__printNodes(node.left, newVal)
        if(node.right):
            self.__printNodes(node.right, newVal)
    
        if(self.isLeaf(node)):
            print(f"{node.symbol} -> {newVal}")

    def isLeaf(self, root):
        return root.left is None and root.right is None
    
    def encode(self):
        self.__encode(self.root)
        # Luego de codificar simplemente se calcula la longitud total de los codigos para la codificacion completa
        for i in self.raw_data:
            self.code_total_legth += len(self.codes.get(i))

    def __encode(self, node, string = ''):
        if node is None:
            return
        if self.isLeaf(node):
            self.codes[node.symbol] = string if len(string) > 0 else '1'
        self.__encode(node.left, string + '0')
        self.__encode(node.right, string + '1')
    
    def saveFile(self, file):
        data = ''
        for i in self.raw_data:
            data += self.codes.get(i)
        with open(file, 'w') as f:
            f.write(data)


    def avgLength(self):
        return sum([len(self.codes[i]) * self.prob[i] for i in self.codes.keys()])

    def getLenghts(self):
        print(f"Longitud cod huffman: {self.code_total_legth} bits")
        print(f"Longitud original: {self.source_code_size} bits")
        print("Tasa compresion: {:.1f}".format(self.source_code_size/self.code_total_legth))
