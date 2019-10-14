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


from apyori import apriori

if __name__ =='__main__': 
    dataSet = loadDataSet('data.txt')
    association_rules = apriori(dataSet, min_support=0.2, min_confidence=0.5, min_lift=1, max_length=3) 
    association_results = list(association_rules)
    print(len(association_results))
    for item in association_results:
        
        pair = item[0] 
        items = [x for x in pair]
        if len(items) > 1:
            string = ""
            for i in range(len(items)-1):
                string = string + str(items[i] + ' ')
            
            print("Rule: " + string + " -> "+ items[-1] + ' conf:' +  str(item[2][0][2]) + ' support :' + str(item[1]) + ' lift: ' + str(item[2][0][3]))