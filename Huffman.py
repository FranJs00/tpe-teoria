from collections import Counter
import heapq

class HuffmanNode:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

    def __lt__(self, other):
        return self.freq < other.freq


class Huffman():
    def __init__(self):
        self.raw_data = ''
        self.codes = {}
        self.prob = {}
        self.root = None

    def loadFile(self, file):
        with open(file, 'r') as f:
            data = f.read()
        self.raw_data = data.replace("\n", " ").split(" ")

        self.calculate_probability_distribution()

    def calculate_probability_distribution(self):
        count = Counter(self.raw_data)
        total_values = len(self.raw_data)
        relative_frequency = {value: occurrences / total_values for value, occurrences in count.items()}

        sum_frequencies = sum(relative_frequency.values())
        probability_distribution = {value: frequency / sum_frequencies for value, frequency in relative_frequency.items()}

        self.prob = probability_distribution

        # print(self.prob)
        # print(dict(sorted(self.prob.items())))

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
        self._printNodes(self.root)

    def _printNodes(self, node, val = ''):
        newVal = val + str(node.huff)
    
        if(node.left):
            self._printNodes(node.left, newVal)
        if(node.right):
            self._printNodes(node.right, newVal)
    

        if(not node.left and not node.right):
            print(f"{node.symbol} -> {newVal}")

    def isLeaf(self, root):
        return root.left is None and root.right is None
    
    def encode(self):
        self._encode(self.root)

    def _encode(self, node, string = ''):
        if node is None:
            return
        if self.isLeaf(node):
            self.codes[node.symbol] = string if len(string) > 0 else '1'
        self._encode(node.left, string + '0')
        self._encode(node.right, string + '1')

    
    def saveFile(self, file):
        data = ''
        for i in self.raw_data:
            data += self.codes.get(i)
        with open(file, 'w') as f:
            f.write(data)
    