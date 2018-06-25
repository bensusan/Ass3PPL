import numpy as np
import random

K = 20
L = 20
T = 10
epsilon = 0.01

def codebook(ST,SV,K,L):
    alliid=np.uniqe(ST[:,1])
    alluid = np.uniqe(ST[:, 0])
    V=np.random.uniform(low=0, high=L-1, size=(len(alliid),))
    U=np.random.uniform(low=0, high=K-1, size=(len(alluid),))
    #V=[]
    #U=[]
    #for iid in alliid:
    #    V[iid] = random.randint(0, L-1)
    #for uid in alluid:
    #    U[uid] = random.randint(0, K - 1)
    B = updateB(ST,V,U)
    t=1
    RSME=calculateRMSE(SV,U,V,B)
    prevRSME=0
    while not(t==T or abs(prevRSME-RSME)<=epsilon): # TODO what is terminate condition
        nextU = []
        for uid in alluid:
            nextU[uid] = updateU(K,ST,uid,B,V)
        U = np.array(nextU)
        B = updateB(ST,V,U)
        nextV = []
        for iid in alliid:
            nextV [iid] = updateV(L,ST,iid,B,V)
        V=np.array(nextV)
        B = updateB(ST, V, U)
        prevRSME=RSME
        RSME = calculateRMSE(SV,U,V,B)
        t = t+1
    retrun U,V,B



#Line 13
def updateB(ST,V,U):
    #########################
    Bans = np.ones((K,L),dtype=int)
    ratings = ST[:, 2]
    avagSystem = np.mean(ratings)
    Bans *= avagSystem
    iids = ST[:, 1]
    uids = ST[:, 0]
    ufunc = np.vectorize(lambda uid: U[uid])
    uids = ufunc(uids)

    vfunc = np.vectorize(lambda iid: V[iid])
    iids = vfunc(iids)
    for i in range(K):
        Iiids = (iids == i)
        for j in range(L):
            Juids=(uids == j)
            STAfterAnd=ST[np.logical_and(Iiids, Juids)]
            if not (STAfterAnd.size == 0) :
                 Bans[i][j]=np.mean(STAfterAnd)
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
def updateU(K,):
    for j in range(K):


    # TODO




#Line 12
def updateV():
    # TODO


#Line 14
def calculateRMSE(SV,U,V,B):
    nowsum=np.apply_along_axis(lambda col: (B[U[col[0]],V[col[1]]]-col[2])**2, 1, SV)
    return np.sum(nowsum)
    # sum=0
    # for uid,iid,rating in SV:
    #     sum=sum+((rating-B[U[uid]][V[iid]])**2)
    # return sum

