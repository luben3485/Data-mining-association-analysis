class FPtreeNode:
    def __init__(self,name,count,parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.link = None
        self.children = {}
    def add(self,count):
        self.count += count
    def disp(self,ind=1):
        print(' '*ind,self.name,' ',self.count)
        for child in self.children.values():
            child.disp(ind+1)

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
            #subSet.append(frozenset([item]))
            subSet.append(item)
            current += 1
        else:
            #subSet.append(frozenset([item]))
            subSet.append(item)
    dataSet.append(subSet)
    return dataSet


def create(dataSet,minSupport=0.5):
    totalLength = len(dataSet)

    Table={}
    for data in dataSet:
        for item in data:
            if not item in Table:
                Table[item] = 1
            else:
                Table[item] += 1
    #print('\n')
    #print(Table)
    #print("Table's length: %s" % len(Table))

    for key in list(Table.keys()):
        if Table[key]/totalLength < minSupport:
            del(Table[key])
    freqItemSet=set(Table.keys())

    #print(freqItemSet)
    #print (Table)
    #print ("Table's length: %s" % len(Table))
    if len(freqItemSet) == 0:
        return None,None
    else:
        for key in Table:
            Table[key]=[Table[key],None]
    #print(Table)
    
    retTree=FPtreeNode('Null',1,None) #root
    
    for data in dataSet:
        localD={}
        for item in data:
            if item in freqItemSet:
                localD[item]=Table[item][0]
        if len(localD)>0:
            #print(localD.items())
            orderedItems=[v[0] for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)]
            #print(orderedItems)
            connect(orderedItems,retTree,Table,1)

    #print(orderedDataSet)
    return retTree,Table


def connect(items,inTree,Table,count):
    if items[0] in inTree.children:
        inTree.children[items[0]].add(count)
    else:
        inTree.children[items[0]]=FPtreeNode(items[0],count,inTree)
        if Table[items[0]][1]==None:
            Table[items[0]][1]=inTree.children[items[0]]
        else:
            updateTable(Table[items[0]][1],inTree.children[items[0]])
    if len(items) > 1:
        connect(items[1::],inTree.children[items[0]],Table,count)
        
        
def updateTable(node,targetNode):
    while (node.link!=None):
        node=node.link
    node.link=targetNode

def findFrequency(inTree,Table,minSupport,preFix,freqList):
    #print(Table.items())
    L=[v[0] for v in sorted(Table.items(),key=lambda p:p[0])]
    
    for basePat in L:
        newFreqSet=preFix.copy()
        newFreqSet.add(basePat)
        freqList.append(newFreqSet)
        conPattBases=findPrePath(basePat,Table[basePat][1])
        myCondTree,myHead=create(conPattBases,minSupport)
        
        if myHead!=None:
            findFrequency(myCondTree,myHead,minSupport,newFreqSet,freqList)
            
def listParent(leafNode,prePath):
    if leafNode.parent!=None:
        prePath.append(leafNode.name)
        listParent(leafNode.parent,prePath)
        
        
def findPrePath(basePat,treeNode):
    condPats={}
    while treeNode!=None:
        prePath=[]
        listParent(treeNode,prePath)
        
        if len(prePath)>1:
            condPats[frozenset(prePath[1:])]=treeNode.count
        treeNode=treeNode.link
        
    return condPats

if __name__ =='__main__': 
    dataSet = loadDataSet('data.txt')
    retTree,Table = create(dataSet,0.5)
    #retTree.disp()
    #print(dataSet)

    freqItems=[]
    findFrequency(retTree,Table,0.5,set([]),freqItems)
    print('frequency items:')
    for item in freqItems:
        print(item)