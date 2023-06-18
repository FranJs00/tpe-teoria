from Huffman import Huffman
import math
import random



# Se movieron funciones fuera de la clase al no tener relacion directa con Huffman
EPSILON = 0.0005
PRUEBAS_MINIMAS = 10000

def entropy(prob):
    return sum(-p * math.log2(p) for p in prob)

def perfomance(avgLength, entropy):
    return entropy/avgLength

def calculateAvgAndStdDeviation(cumulative_prob):
    pruebas = 0
    suma = 0
    media = 0.0
    media_anterior = -1.0
    suma_cuadrada = 0.0
    while(pruebas < PRUEBAS_MINIMAS or abs(media-media_anterior) > EPSILON):
        r = random.random()
        for item in cumulative_prob.items():
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

def cumulativeProb(probs):
    aux = dict([a,float(x)] for a,x in probs.items())
    aux2 = dict(sorted(aux.items(), key=lambda item: item[1]))
    suma = 0.0
    cumulative_prob = {}
    for item in aux2.items():
        cumulative_prob[str(item[0])] = suma
        suma = suma + item[1]
    return cumulative_prob

h = Huffman()

h.loadFile('signal1.txt')
h.buildTree()
h.encode()


print("a)")
print(entropy(h.prob.values()))
print("b)")
print(h.avgLength())
print("c)")
h.getLenghts()
print("d)")
print(perfomance(h.avgLength(), entropy(h.prob.values())))
print("e)")
calculateAvgAndStdDeviation(cumulativeProb(h.prob))
