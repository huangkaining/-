import numpy
import math
def excludeoutlier(orilist):
    p = []
    for i in orilist:
        p.append(i['consume_number'])
    cnt = 0
    for i in p:
        cnt+=i
    average = cnt/len(p)
    cnt2 = 0
    for i in p:
        cnt2+= (i-average) * (i - average)
    if len(p) > 1:
        s = math.sqrt( cnt2 / (len(p) - 1))
    else:
        s = math.sqrt(cnt2 / (len(p)))
    ans = []
    for i in p:
        if abs(i - average) < 3*s:
                ans.append(i)
    return ans

def average(orilist):
    p = []
    p.extend(orilist)
    cnt = 0
    for i in p:
        cnt += i
    if len(p) > 0:
        return round(int(cnt/len(p)),2)
    else:
        return 0

from numpy import *

#载入数据，清洗数据保存为矩阵形式
def loadDataSet(filename):
    fr = open(filename)
    lines = fr.readlines()
    dataMat = []
    for line in lines:
        result = line.strip().split()
        fltline = list(map(float,result))
        dataMat.append(fltline)
    return dataMat


#向量计算距离
def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA-vecB,2)))


# 给定数据集构建一个包含k个随机质心的集合，
def randCent(dataSet,k):
    n = shape(dataSet)[1] # 计算列数

    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j]) #取每列最小值
        #print(list(dataSet[:,j]))
        rangeJ = float(max(dataSet[:,j])-minJ)
        centroids[:,j] = minJ + rangeJ*random.rand(k,1) # random.rand(k,1)构建k行一列，每行代表二维的质心坐标
        #random.rand(2,1)#产生两行一列0~1随机数
    return centroids
#minJ + rangeJ*random.rand(k,1)自动扩充阵进行匹配，实现不同维数矩阵相加,列需相同
def kMeans(dataSet,k,distMeas = distEclud,creatCent = randCent):
    m = shape(dataSet)[0] # 行数
    clusterAssment = mat(zeros((m,2))) # 建立簇分配结果矩阵，第一列存索引，第二列存误差
    centroids = creatCent(dataSet,k) #聚类点
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf # 无穷大
            minIndex = -1 #初始化
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:]) # 计算各点与新的聚类中心的距离
                if distJI < minDist: # 存储最小值，存储最小值所在位置
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i,0] != minIndex:
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A== cent)[0]]
            # nonzeros(a==k)返回数组a中值不为k的元素的下标
            centroids[cent,:] = mean(ptsInClust,axis=0) # 沿矩阵列方向进行均值计算,重新计算质心
    return centroids,clusterAssment

#dataMat = mat([[1],[5],[3],[50],[55]])
def Kmean(orilist):
    #print('orlist:',orilist)
    dataMat = mat(orilist.copy())
    '''for i in orilist:
        p = []
        p.append(i)
        dataMat.append(p)'''
    #print('dataMat:',dataMat)
    myCentroids,clustAssing = kMeans(dataMat,3)
    ans = []
    for i in myCentroids:
        p = numpy.nan_to_num(i.tolist())[0]
        ans.extend(p)
    #anslist = numpy.nan_to_num(ans.tolist())
    print(ans)
    return ans
