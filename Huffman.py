from collections import Counter
import heapq
import math
import random

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
        self.entropy = 0
        self.huff_avg_len = 0
        self.code_total_legth = 0
        self.source_code_size = 0
        self.cumulative_prob = {}

    def loadFile(self, file):
        with open(file, 'r') as f:
            data = f.read()
        self.raw_data = data.replace("\n", " ").split(" ")

        self.__calculateSignalSize()
        self.__calculate_probability_distribution()
        self.__createCumulativeProb()

    def __createCumulativeProb(self):
        aux = dict([a,float(x)] for a,x in self.prob.items())
        aux2 = dict(sorted(aux.items(), key=lambda item: item[1]))
        suma = 0.0
        for item in aux2.items():
            self.cumulative_prob[str(item[0])] = suma
            suma = suma + item[1]

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
        self.__calculateCodeTotalLength()

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
    
    def calculateEntropy(self):
        self.__calculateEntropy(self.root)

    def __calculateEntropy(self,node):
        if(node is None):
            return
        self.__calculateEntropy(node.left)
        self.__calculateEntropy(node.right)
        if(self.isLeaf(node)):
            node_prob = self.prob[node.symbol]
            self.entropy += (math.log2(node_prob)*(-node_prob))

    def getEntropy(self):
        print(f"Entropia: {self.entropy}")
        
    def calculateHuffmanAvgLength(self):
        self.__calculateHuffmanAvgLength(self.root)

    def __calculateHuffmanAvgLength(self,node):
        if(node is None):
            return
        self.__calculateHuffmanAvgLength(node.left)
        self.__calculateHuffmanAvgLength(node.right)
        if(self.isLeaf(node)):
            self.huff_avg_len += (self.prob[node.symbol] * len(self.codes[node.symbol]))

    def getHuffmanAvgLength(self):
        print(f"Longitud media: {self.huff_avg_len}\nDiferencia con Entropia: {abs(self.entropy-self.huff_avg_len)}")

    def getCodePerformance(self):
        perform = self.entropy/self.huff_avg_len
        print(f"Rendimiento: {perform}")

    def __calculateCodeTotalLength(self):
        for c in self.codes:
            self.code_total_legth += len(c)

    def __calculateSignalSize(self):
        source = [eval(i) for i in self.raw_data]
        sup = max(source)
        base = math.ceil(math.log2(sup))
        self.source_code_size = len(self.raw_data) * base

    def getLenghts(self):
        print(f"Longitud cod huffman: {self.code_total_legth} bits")
        print(f"Longitud original: {self.source_code_size} bits")
        print("Tasa compresion: {:.1f}".format(self.source_code_size/self.code_total_legth))

    def calculateAvgAndStdDeviation(self):
        pruebas = 0
        suma = 0
        media = 0.0
        media_anterior = -1.0
        suma_cuadrada = 0.0
        while(pruebas < PRUEBAS_MINIMAS or abs(media-media_anterior) > EPSILON):
            r = random.random()
            for item in self.cumulative_prob.items():
                if(r < item[1]):
                    suma += int(item[0])
                    suma_cuadrada += pow(int(item[0]),2)
                    break
            pruebas += 1
            media_anterior = media
            media = suma/pruebas
        
        media_cuadrada = suma_cuadrada/pruebas
        varianza = media_cuadrada - pow(media,2)
        desvio = math.sqrt(varianza)

        print("Media: {:.3f}".format(media))
        print("Desvio std: {:.3f}".format(desvio))