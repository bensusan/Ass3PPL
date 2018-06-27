import csv

import numpy as np
import sys
import math

K = 20
L = 20
T = 4
epsilon = 0.01
global U_counter
U_counter = 0

STList = [[1,1,3],[1,3,5]]
SVList = [[2,1,3],[1,4,3],[1,3,3],[3,1,3]]
VList = [0,2,1,0,3]
BList = [[2,1,1,4],[4,5,5,5],[3,3,3,5],[2,4,3,5]]
UList = [0,3,1,2,3]
ST = np.asarray(STList, dtype=np.int)
SV = np.asarray(SVList, dtype=np.int)
B = np.asarray(BList, dtype=np.int)
V = np.asarray(VList, dtype=np.int)
U = np.asarray(UList, dtype=np.int)

def select(n, uid, B, U, V):
    my_data = np.loadtxt(open("ratings.csv", "rb"), usecols=(0,1),delimiter=',', skiprows=1)
    masked = (my_data[:,0]==uid)
    my_data = my_data[masked]
    ans=[]
    usercluster=U[uid-1]
    userexpectedrating=B[usercluster]
    while n>0:
        maxcluster=np.argmax(userexpectedrating)
        if userexpectedrating[maxcluster] == -1:
            break
        userexpectedrating[maxcluster] = -1
        reshapedV = np.reshape(V, (V.shape[0], 1))
        id = [i for i in xrange(1, len(reshapedV) + 1)]
        reshapedV = np.insert(reshapedV, 0, id, axis=1)
        mask = (reshapedV[:,1]==maxcluster)
        bestmovies = reshapedV[mask]
        mask = np.isin(bestmovies[:,0], my_data[:,1])
        bestmovies = bestmovies[np.logical_not(mask)]
        while n>0 and len(bestmovies)>0:
            ans.append(bestmovies[0][0])
            bestmovies = np.delete(bestmovies,0,0)
            n-=1
    return ans




def codebook(ST,SV,K,L):
    alliidST=np.unique(ST[:,1]).astype(int)
    alluidST = np.unique(ST[:,0]).astype(int)
    alliidSV = np.unique(SV[:,1]).astype(int)
    alluidSV = np.unique(SV[:, 0]).astype(int)

    alliid = np.unique(np.concatenate((alliidSV,alliidST),axis=0))
    alluid = np.unique(np.concatenate((alluidSV,alluidST),axis=0))
    V=np.random.randint(low=0, high=L, size=(max([alliid.max(),alliidSV.max()]),))
    U=np.random.randint(low=0, high=K, size=(max([alluid.max(),alluidSV.max()]),))

    #V=[]
    #U=[]
    #for iid in alliid:
    #    V[iid] = random.randint(0, L-1)
    #for uid in alluid:
    #    U[uid] = random.randint(0, K - 1)
    B = updateB(ST,V,U,K,L)
    t=1
    RSME=calculateRMSE(SV,U,V,B)
    prevRSME=0
    while not(t==T or abs(prevRSME-RSME)<=epsilon): # TODO what is terminate condition
        print('t is now:'+str(t))
        print('RMSE is now:' + str(RSME))
        print('previous RMSE is now:' + str(prevRSME))
        nextU = np.array(U)
        for uid in alluid:
            nextU[uid-1] = updateU(K,ST,uid,B,V)
        U = np.array(nextU)
        B = updateB(ST,V,U,K,L)
        nextV = np.array(V)
        for iid in alliid:
            nextV[iid-1] = updateV(L,ST,iid,B,V)
        V=np.array(nextV)
        B = updateB(ST, V, U,K,L)
        prevRSME=RSME
        RSME = calculateRMSE(SV,U,V,B)
        t = t+1
    print('exit while')
    reshapedU = np.reshape(U, (U.shape[0], 1))
    np.savetxt("U.csv", reshapedU, fmt='%i', delimiter=",")

    reshapedV = np.reshape(V, (V.shape[0], 1))
    np.savetxt("V.csv",reshapedV,fmt='%i',delimiter=",")

    np.savetxt("B.csv", B, delimiter=",")
    ans = select(10,1,B,U,V)
    print('got ans')
#Line 13
def updateB(ST,V,U,K,L):
    #########################
    Bans = np.ones((K,L),dtype=float)
    ratings = ST[:, 2]
    avagSystem = np.mean(ratings)
    Bans *= avagSystem
    iids = ST[:, 1].astype(int)
    uids = ST[:, 0].astype(int)
    ufunc = np.vectorize(lambda uid: U[uid-1])
    uids = ufunc(uids)

    vfunc = np.vectorize(lambda iid: V[iid-1])
    iids = vfunc(iids)
    for i in range(K):
        Iiids = (iids == i)
        for j in range(L):
            Juids=(uids == j)
            STAfterAnd=ST[np.logical_and(Iiids, Juids)]
            if not (STAfterAnd.size == 0) :
                 Bans[i][j]=np.mean(STAfterAnd[:,2])
    return Bans

    ###########################
    # BSum = np.zeros((K, L), dtype=int)
    # BCount = np.zeros((K, L), dtype=int)
    # for uid,iid,rating in ST:
    #     i=U[uid]
    #     j=V[iid]
    #     BSum[i][j]+=rating
    #     BCount[i][j]+=1
    # avagSystem=np.sum(BSum)/np.sum(BCount)
    # for i in range(K):
    #     for j in range(L):
    #         if BCount[i][j]==0:
    #             BSum[i][j]=avagSystem
    #         else:
    #             BSum[i][j]=BSum[i][j]/BCount[i][j]
    # return BSum


#Line 9
#this function will return the best cluster for uid
def updateU(K,ST,uid,B,V):
    user_ids = ST[:, 0]
    mask = (user_ids == uid)
    masked = ST[mask]   #returns an array with ratings for specific user
    bestJ = 0;
    bestSum = sys.maxint
    for j in range(K):
        # lst = []
        # for user_id,iid,rating in masked:
        #     lst.append([(rating-B[j][V[iid-1]])**2])
        #
        # arr = np.asarray(lst,dtype=np.int)
        # sum = np.sum(arr)

        nowsum = np.apply_along_axis(lambda col: (col[2] - B[j][V[int(col[1]) - 1]]) ** 2, 1, masked)
        sum = np.sum(nowsum)
        if sum<bestSum:
            bestSum = sum
            bestJ = j


    return bestJ


    #TODO




#Line 12
def updateV(L,ST,iid,B,U):
    item_ids = ST[:, 1]
    mask = (item_ids == iid)
    masked = ST[mask]   #returns an array with ratings for specific movie
    bestJ = 0;
    bestSum = sys.maxint
    for j in range(L):
        # lst = []
        # for user_id,item_id,rating in masked:
        #     lst.append([(rating-B[U[user_id-1]][j])**2])
        #
        # arr = np.asarray(lst,dtype=np.int)


        nowsum = np.apply_along_axis(lambda col: (col[2] - B[U[int(col[0]) - 1]][j]) ** 2, 1, masked)
        sum = np.sum(nowsum)
        if sum<bestSum:
            bestSum = sum
            bestJ = j


    return bestJ
    #TODO

#Line 14
def calculateRMSE(SV,U,V,B):
    nowsum = np.apply_along_axis(lambda col: (B[U[int(col[0]) - 1]][V[int(col[1]) - 1]] - col[2]) ** 2, 1, SV)
    return math.sqrt(np.mean(nowsum))
    # sum=0
    # for uid,iid,rating in SV:
    #     sum=sum+((rating-B[U[uid]][V[iid]])**2)
    # return sum


my_data = np.loadtxt("ratings.csv", delimiter=',',usecols=(0,1, 2),skiprows=95000)

np.random.shuffle(my_data)
data_length = len(my_data)
floor = int(math.floor(data_length*0.8))
ceil = int(math.ceil(data_length*0.8))
ST = my_data[:floor]
SV = my_data[ceil:]
SV = ST
codebook(ST,SV,20,20)
#select(10,1,[],[],[])