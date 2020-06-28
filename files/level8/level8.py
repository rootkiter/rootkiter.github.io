#!/bin/python
###############################################
# File Name : realcode.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2020-06-25 20:56:22 CST
###############################################

'''
 0  2 12 jmp    off_36
 3  1  3 if (reg_2  == 0) : reg_15 += nextsize
 4  2 12 jmp    off_8
 6  1  2 reg_15  = pop()
 8  2 11 push reg_2 ; reg_2  += -1
10  2  7 reg_4   = reg_0 *reg_3
12  2  7 reg_5   = reg_1 *reg_9
14  2  5 reg_4   = reg_4 +reg_5
16  2  9 reg_4   = reg_4 %reg_6
18  1  1 push reg_4
19  2  7 reg_4   = reg_0 *reg_7
21  2  7 reg_5   = reg_1 *reg_8
23  2  5 reg_4   = reg_4 +reg_5
25  2  9 reg_1   = reg_4 %reg_6
27  1  2 reg_0   = pop()
28  2 11 push reg_15; reg_15 += -27
30  2 11 push reg_15; reg_15 += -29
32  1  2 reg_2   = pop()
33  1  3 if (reg_6  == 0) : reg_15 += nextsize
34  1  2 reg_15  = pop()
36  2 13 reg_0   = 5
38  2 13 reg_1   = 6
40  2 13 reg_3   = 3
42  2 13 reg_7   = 7
44  2 13 reg_8   = 8
46  2 13 reg_9   = 9
48  9 14 reg_6   = 99999999999999997
57  2 13 reg_2   = 127
59  2 11 push reg_15; reg_15 += -58  # the real exit
61  1  0 exit
'''

def calc(r0, r1):
    r0tmp = (r0 * 3 + r1 * 9) % 99999999999999997
    r1tmp = (r0 * 7 + r1 * 8) % 99999999999999997
    return r0tmp, r1tmp

def Factorial(count, r0, r1):
    for i in range(1, count+1)[::-1]:
        r0, r1 = calc(r0, r1)
        r0, r1 = Factorial(i-1, r0, r1)
    return r0, r1

if __name__=='__main__1':
    print("--->",  Factorial(127, 5, 6))

    #for i in range(1, 10):

def getRealResult(matrix, vlist):
    r0 = (matrix[0][0] * vlist[0] + matrix[0][1] * vlist[1]) % 99999999999999997
    r1 = (matrix[1][0] * vlist[0] + matrix[1][1] * vlist[1]) % 99999999999999997
    return r0, r1

def MatrixMul(matrix1, matrix2):
    tmp = [[1, 1], [1, 1]]
    tmp[0][0] = (matrix1[0][0] * matrix2[0][0] + matrix1[0][1] * matrix2[1][0]) % 99999999999999997
    tmp[0][1] = (matrix1[0][0] * matrix2[0][1] + matrix1[0][1] * matrix2[1][1]) % 99999999999999997
    tmp[1][0] = (matrix1[1][0] * matrix2[0][0] + matrix1[1][1] * matrix2[1][0]) % 99999999999999997
    tmp[1][1] = (matrix1[1][0] * matrix2[0][1] + matrix1[1][1] * matrix2[1][1]) % 99999999999999997
    return tmp

def MatrixMap():
    bmatrix = [[3, 9], [7, 8]]
    return {
        1: bmatrix,
        2: MatrixMul(bmatrix, bmatrix),
    }

def SquareMapMatrix():
    baseMatrix = MatrixMap()
    squareMatrix = {}
    squareMatrix[0] = baseMatrix[1]
    squareMatrix[1] = baseMatrix[2]
    for i in range(2, 128):
        squareMatrix[i] = MatrixMul(squareMatrix[i-1], squareMatrix[i-1])
    return squareMatrix

def FactorialMatrix( times ):
    squareMatrix = SquareMapMatrix()
    reslist = squareMatrix[0]
    for i in range(1, times):
        reslist = MatrixMul(reslist, squareMatrix[i])
    return reslist

if __name__=='__main__':
    r0, r1 = (getRealResult(FactorialMatrix(127), [5, 6]))
    key = str(r0)+ str(r1)
    print(key)



