#!/usr/bin/python3
import sys
import cv2 as cv
import numpy as np
import random


def MeanSquaredError(matrizA, matrizB):

    return np.square(np.subtract(matrizA, matrizB)).mean()

def NormalizesMatrix(matriz):

    Max, Min = matriz.max(), matriz.min()
    return (matriz - Min)/(Max - Min)

def GetRealImaginary(imagem):

    I = cv.imread(imagem, cv.IMREAD_GRAYSCALE)
    if I is None:
        print('Error opening image')
        return -1
    
    rows, cols = I.shape

    crop_img = I[2:rows - 2, 2:cols - 2]

    I = crop_img
    m = cv.getOptimalDFTSize( rows )
    n = cv.getOptimalDFTSize( cols )

    padded = cv.copyMakeBorder(I, 0, m - rows, 0, n - cols, cv.BORDER_CONSTANT, value=[0, 0, 0])
    
    planes = [np.float32(padded), np.zeros(padded.shape, np.float32)]

    complexI = cv.merge(planes)

    cv.dft(complexI, complexI)

    cv.split(complexI, planes)

    #SE NÃO QUISER MOSTRAR A TRANSFORMADA COMENTA DAQUI PRA BAIXO

    cv.magnitude(planes[0], planes[1], planes[0])

    magI = planes[0]
    
    matOfOnes = np.ones(magI.shape, dtype=magI.dtype)

    cv.add(matOfOnes, magI, magI)

    cv.log(magI, magI)
    
    magI_rows, magI_cols = magI.shape
    
    magI = magI[0:(magI_rows & -2), 0:(magI_cols & -2)]

    cx = int(magI_rows/2)
    cy = int(magI_cols/2)
    q0 = magI[0:cx, 0:cy]
    q1 = magI[cx:cx+cx, 0:cy]
    q2 = magI[0:cx, cy:cy+cy]
    q3 = magI[cx:cx+cx, cy:cy+cy]

    tmp = np.copy(q0)

    magI[0:cx, 0:cy] = q3
    magI[cx:cx + cx, cy:cy + cy] = tmp

    tmp = np.copy(q1)   
    magI[cx:cx + cx, 0:cy] = q2
    magI[0:cx, cy:cy + cy] = tmp
    
    cv.normalize(magI, magI, 0, 1, cv.NORM_MINMAX)
    cv.imshow("transformada", magI)
    cv.waitKey()

    return planes

def Calculate():

    acerto = 0

    randomNumber = random.randint(1, 10)

    for x in range (1, 41):

        lista = list()
        #print("orl_faces/s" + str(x) + "/" + str(randomNumber) + ".pgm")
        mainImage = GetRealImaginary(imagem = "orl_faces/s" + str(x) + "/" + str(randomNumber) + ".pgm")
        mainReal = NormalizesMatrix(mainImage[0])
        mainImaginary = NormalizesMatrix(mainImage[1]) 
        
        for i in range(1, 41):

            listaTwo = list()
           
            for j in range (1, 11):
                
                if(j == randomNumber):
                    break
                secondImg = GetRealImaginary(imagem = "orl_faces/s" + str(i) + "/" + str(j) + ".pgm")
                mse =  MeanSquaredError(mainImaginary, NormalizesMatrix(secondImg[1]))
                listaTwo.append(mse)

            lista.append(listaTwo)
        menorLinha = 0
        menorValor = 999999999999
        contador = 1

        for linha in lista:
            for coluna in linha:
                if coluna < menorValor :
                    menorValor = coluna
                    menorLinha = contador
            contador = contador + 1
        #print(menorLinha)
        if(x == menorLinha):
            acerto = (acerto + 1)

    return((acerto/40)*100)

def Run(randomNumber):

    lista = list()

    for x in range(1, 41):
        
        mainImage = GetRealImaginary(imagem = "orl_faces/s" + str(x) + "/" + str(randomNumber) + ".pgm")
        mainReal = NormalizesMatrix(mainImage[0])
        mainImaginary = NormalizesMatrix(mainImage[1])
        menorMseCount = 0
        menorMse = 999999999999999
        contador = 1

        for i in range(1, 11):

            if(i != randomNumber):

                secondImg = GetRealImaginary(imagem = "orl_faces/s" + str(x) + "/" + str(i) + ".pgm")
                mse = MeanSquaredError(mainReal, NormalizesMatrix(secondImg[0]))
                
                if(mse < menorMse):
                    menorMse = mse
                    menorMseCount = contador
                contador = contador + 1

        lista.append(menorMseCount)
    
    return lista

def Compare(lista, randomNumber):

    acerto = 0

    for x in range(1, 41):

        mainImage = GetRealImaginary(imagem = "orl_faces/s" + str(x) + "/" + str(randomNumber) + ".pgm")
        mainReal = NormalizesMatrix(mainImage[0])
        mainImaginary = NormalizesMatrix(mainImage[1])
        mseMenor = 99999999
        contador = 1
        mseMenorCount = 0

        for j in range(1, 41):

            #print("orl_faces/s" + str(j) + "/" + str(lista[j]) + ".pgm")
            secondImg = GetRealImaginary(imagem = "orl_faces/s" + str(j) + "/" + str(lista[j - 1]) + ".pgm")
            mse = MeanSquaredError(mainReal, NormalizesMatrix(secondImg[0]))
         
            if(mse < mseMenor):
                mseMenor = mse
                mseMenorCount = contador
            contador = contador + 1
        if(x == mseMenorCount):
            print("A imgem " + str(x) + "bateu com o " + str(mseMenorCount))
            acerto = (acerto + 1)
    
    return (acerto/40)*100

def main(argv):

    print(Calculate())
    #randomNumber = random.randint(1 , 10)
    #lista = Run(randomNumber)
    #print(lista)
    #print(Compare(lista, randomNumber))

if __name__ == "__main__":
    main(sys.argv[1:])