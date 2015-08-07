import math
import datetime
from queue import Queue
import sys
import multiprocessing
import copy
import functools

#imports training data from the relevant file
def importData(argUserKeyMat, argFileName):
    with open(argFileName, 'r') as lFile:
        for line in lFile:
            data = line.strip('\n').split(',')
            if int(data[1]) not in argUserKeyMat:
                argUserKeyMat[int(data[1])] = {int(data[0]): float(data[2])}
            else:
                argUserKeyMat[int(data[1])][int(data[0])] = float(data[2])

#obtains the mean rating of each user
def getMean(argUserKeyMat, argMean):
    for user in argUserKeyMat:
        argMean[user] = 0
        for movie in argUserKeyMat[user]:
            argMean[user] += argUserKeyMat[user][movie]/len(argUserKeyMat[user])

#predict the rating of the movie using collaborative filtering
#print the error for predicted rating for a given movie and user
#and return the Absolute Mean Error and the Root Mean Squared Error
def predictRating(argMovUsrRat, argUserKeyMat, argMean):
        for i in range(len(argMovUsrRat)-1):
            argMovUsrRat[i] = int(argMovUsrRat[i])
        argMovUsrRat[2] = float(argMovUsrRat[2]) 
	#initialize local variables
        p = 0
        weightMat = {}
        user = argMovUsrRat[1]
	#calculate the weights for each user
        for i in argUserKeyMat:
            if not i == user:
                numerator = 0
                denom1 = 0
                denom2 = 0
                for movie in argUserKeyMat[i]:
                    if movie in argUserKeyMat[user]:
                        numerator+=(argUserKeyMat[user][movie] - argMean[user])*(argUserKeyMat[i][movie] - argMean[i])
                        denom1 += pow((argUserKeyMat[user][movie] - argMean[user]),2)
                        denom2 += pow((argUserKeyMat[i][movie] - argMean[i]),2)
                if denom1 != 0 and denom2 != 0:
                    weight  = (numerator/math.pow(denom1*denom2, 1/2))
                    weightMat[i] = weight
	#predict the rating!
        normInv = 0
        for otherUsrs in weightMat:
            normInv +=  abs(weightMat[otherUsrs])
            if argMovUsrRat[0] in argUserKeyMat[otherUsrs]:
                p+= weightMat[otherUsrs]*(argUserKeyMat[otherUsrs][argMovUsrRat[0]]-argMean[otherUsrs])
        norm = 1/normInv
        p = p*norm
        p+= argMean[int(argMovUsrRat[1])]
	#so finally, p holds the predicted rating
        ErrorAM = abs(p - argMovUsrRat[2])
        ErrorRMS = math.pow(p - argMovUsrRat[2], 2)
        print("Movie = ",argMovUsrRat[0], "User = ", argMovUsrRat[1], "Error = ", p - argMovUsrRat[2])
        return([ErrorAM, ErrorRMS])
    
#run algorithm on testing data, get the error metrics
def test(argTestFileName, argUserKeyMat, argMean):
    lineList = []
    numLines = 0
    #Initialize a pool of five intrepid processes that will do your bidding!
    pool = multiprocessing.Pool(processes=5)
    with open(argTestFileName, 'r') as testFile:
        for line in testFile:
            lineList.append(line.strip('\n').split(','))
            numLines += 1
    ErrorAM = 0
    ErrorRMS = 0
    #Because the pool can only take one argument that will keep changing
    predictRatingP = functools.partial(predictRating, argUserKeyMat = argUserKeyMat, argMean = argMean)
    eAeRnT = pool.map(predictRatingP, lineList)
    #Sum up the treacherous errors
    for i in eAeRnT:
        ErrorAM += i[0]
        ErrorRMS += i[1]
    ErrorAM = ErrorAM/numLines
    ErrorRMS = math.pow(ErrorRMS/numLines, 1/2)
    return [ErrorAM, ErrorRMS]

#everything in here's self-explanatory
def main():     
    userKeyMat = {}
    importData(userKeyMat, sys.argv[1])
    weightMat = {}
    mean = {}
    getMean(userKeyMat, mean)
    output = test(sys.argv[2], userKeyMat, mean)
    print("Absolute Mean Error = ",output[0])
    print("Root Mean Square Error = ",output[1])

if __name__ == "__main__":
    main()
