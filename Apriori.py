def loadDataSet(fileName):
    f = open(fileName,'r',encoding="utf-8")
    dataSet=[]
    current = 1
    subSet = []
    for line in f.readlines():
        line=line.strip('\n')
        tmpList = line.split(' ')
        index = tmpList[0]
        item = tmpList[1]

        if int(index) != current:
            dataSet.append(subSet)
            subSet = []
            subSet.append(item)
            current += 1
        else:
            subSet.append(item)
    dataSet.append(subSet)
    return dataSet    

def createC1(dataSet):
    C1 = []
    for data in dataSet:
        for item in data:
            if not [item] in C1:
                C1.append([item])
    return [frozenset(x) for x in C1]

def createLk(dataSet,Ck,minSupport):
    countCk = {}
    for data in dataSet:
        for subSet in Ck:
            if subSet.issubset(data):
                if not subSet in countCk:
                    countCk[subSet] = 1
                else:
                    countCk[subSet] += 1
    totalNum = len(dataSet)
    Lk = []
    countLk = {}
    for key in countCk:
        support = countCk[key]/totalNum
        if support >= minSupport:
            Lk.append(key)
            countLk[key] = support
            
    return Lk,countLk

def createCk(Lk,k):
    ### input
    # type of Lk : frozenset in list  
    # e.g. [frozenset({'A'}), frozenset({'C'}), frozenset({'B'}), frozenset({'E'})]
    # type of k  : int
    ###########
    ### output
    # type of Ck : frozenset in list
    Ck = []
    Lk_len = len(Lk)
    for i in range(Lk_len):
        for j in range(i+1,Lk_len):
            tmpSet = Lk[i] | Lk[j]
            if len(tmpSet) == k and not tmpSet in Ck:
                count = 0
                for item in Lk:
                    if set(item).issubset(tmpSet):
                        count += 1
                        #print(item,tmpSet,count)
                if count == k:
                    Ck.append(tmpSet)
    
    return Ck

def apriori(dataSet,minSupport =0.5):
    L = []
    countL = []
    C1 = createC1(dataSet)
    Lk,countL1 = createLk(dataSet,C1,minSupport)
    L.append(Lk)
    countL.append(countL1)
    k = 2
    while len(L[k-2]) > 0: 
        Ck = createCk(Lk,k)
        Lk,countLk = createLk(dataSet,Ck,minSupport)
        L.append(Lk)
        countL.append(countLk)
        k += 1
    return L,countL

def generateRules(dataSet,L,countL,minConfidence=0.6):
    c = 0
    if len(L) > 2:
        M  =len(L)-1 
        for itemSet in L[-2]:
            R = []
            numR = 1
            supportM = countL[-2][itemSet]
            
            #A,B,C,... --> X
            itemList = []
            for item in itemSet:
                itemList.append(frozenset([item]))
            for subSet in itemList:
                conf = supportM / countL[M-numR-1][itemSet - subSet]    # e.g. B,C => D
                if conf >= minConfidence:
                    c += 1
                    print('Rule:' + str(itemSet -frozenset(subSet)) +'-->' + str(subSet) + ' conf:'+str(conf)+' support:'+ str(supportM))
                    R.append(frozenset(subSet))
            
            while M-numR > 1:   # e.g 3-2
                numR += 1
                R = createCk(R,numR)

                for subSet in R:
                    conf = supportM / countL[M-numR-1][itemSet - subSet]    # e.g. B => C,D
                    if conf >= minConfidence:
                        c+=1
                        print('Rule:' + str(itemSet -frozenset(subSet)) +'-->' + str(subSet) + ' conf:'+str(conf)+' support:'+ str(supportM))
                    else:
                        R.remove(frozenset(subSet))
    print(c)
                        
if __name__ =='__main__': 
    dataSet = loadDataSet('data.txt')
    L,countL = apriori(dataSet,0.2)
    generateRules(dataSet,L,countL,0.7)           