from Huffman import Huffman

h = Huffman()

h.loadFile('signal1.txt')
h.buildTree()
h.encode()
h.saveFile('test1.txt')