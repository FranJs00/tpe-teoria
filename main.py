from Huffman import Huffman

h = Huffman()

h.loadFile('signal1.txt')
h.buildTree()
h.encode()


print("a)")
h.calculateEntropy()
h.getEntropy()
print("b)")
h.calculateHuffmanAvgLength()
h.getHuffmanAvgLength()
print("c)")
h.getLenghts()
print("d)")
h.getCodePerformance()
print("e)")
h.calculateAvgAndStdDeviation()
