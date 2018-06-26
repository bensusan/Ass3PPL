import numpy as np
import random

K = 20
L = 20
T = 10
epsilon = 0.01

# def codebook(ST,SV,K,L):
#     alliid=np.uniqe(ST[:,1])
#     alluid = np.uniqe(ST[:, 0])
#     V=np.random.uniform(low=0, high=L-1, size=(len(alliid),))
#     U=np.random.uniform(low=0, high=K-1, size=(len(alluid),))
#     #V=[]
#     #U=[]
#     #for iid in alliid:
#     #    V[iid] = random.randint(0, L-1)
#     #for uid in alluid:
#     #    U[uid] = random.randint(0, K - 1)
#     B = updateB(ST,V,U)
#     t=1
#     RSME=calculateRMSE(SV,U,V,B)
#     prevRSME=0
#     while not(t==T or abs(prevRSME-RSME)<=epsilon): # TODO what is terminate condition
#         nextU = []
#         for uid in alluid:
#             nextU[uid] = updateU(K,ST,uid,B,V)
#         U = np.array(nextU)
#         B = updateB(ST,V,U)
#         nextV = []
#         for iid in alliid:
#             nextV [iid] = updateV(L,ST,iid,B,V)
#         V=np.array(nextV)
#         B = updateB(ST, V, U)
#         prevRSME=RSME
#         RSME = calculateRMSE(SV,U,V,B)
#         t = t+1
#     retrun U,V,B
# 
# 
# 
# #Line 13
# def updateB(ST,V,U):
#     BSum=np.zeros((K, L),dtype=int)
#     BCount = np.zeros((K, L), dtype=int)
#     for uid,iid,rating in ST:
#         i=U[uid]
#         j=V[iid]
#         BSum[i][j]+=rating
#         BCount[i][j]+=1
#     avagSystem=np.sum(BSum)/np.sum(BCount)
#     for i in range(K):
#         for j in range(L):
#             if BCount[i][j]==0:
#                 BSum[i][j]=avagSystem
#             else:
#                 BSum[i][j]=BSum[i][j]/BCount[i][j]
#     return BSum

STList = [[1,1,3],[1,3,5]]
VList = [0,2,1,0,3]
BList = [[2,1,1,4],[4,5,5,5],[3,3,3,5],[2,4,3,5]]
UList = [0,3,1,2,3]
ST = np.asarray(STList, dtype=np.int)
B = np.asarray(BList, dtype=np.int)
V = np.asarray(VList, dtype=np.int)
U = np.asarray(UList, dtype=np.int)
#Line 9
#this function will return the best cluster for uid
def updateU(K,ST,uid,B,V):
    user_ids = ST[:, 0]
    mask = (user_ids == uid)
    masked = ST[mask]   #returns an array with ratings for specific user
    bestJ = 0;
    bestSum = 9223372036854775807
    for j in range(K):
        lst = []
        for user_id,iid,rating in masked:
            lst.append([(rating-B[j][V[iid-1]])**2])

        arr = np.asarray(lst,dtype=np.int)
        sum = np.sum(arr)
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
    bestSum = 9223372036854775807
    for j in range(L):
        lst = []
        for user_id,item_id,rating in masked:
            lst.append([(rating-B[U[user_id-1]][j])**2])

        arr = np.asarray(lst,dtype=np.int)
        sum = np.sum(arr)
        if sum<bestSum:
            bestSum = sum
            bestJ = j


    return bestJ
    #TODO

#Line 14
def calculateRMSE(SV,U,V,B):
    sum=0
    for uid,iid,rating in SV:
        sum=sum+((rating-B[U[uid]][V[iid]])**2)
    return sum

updateV(4,ST,1,B,U)