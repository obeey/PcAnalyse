'''

'''

# import matplotlib
import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
# from numpy import loadtxt
import time
from functools import reduce

totalStart = time.time()

# date,bid,ask = np.loadtxt('GBPUSD1d.txt', unpack=True,
#                              delimiter=',',
#                              converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')})


readFile = open('D:/金长江网上交易/金长江网上交易财智版/T0002/export/SH#600012.txt')
lines = readFile.readlines()
lines = lines[4:-1]
readFile.close()

# lineLen = (len(lines)*2)//3
# lineLen = len(lines) //10
# lines = lines[-lineLen:]

date, ask, hi, lo, bid, vol = np.loadtxt(lines, unpack=True,
                                         # delimiter='\t',
                                         converters={0: mdates.bytespdate2num('%Y/%m/%d')},
                                         # converters={0:mdates.charpdate2num(' %Y/%m/%d')},
                                         # skiprows = 2
                                         # usecols=(1,2,3,4,5,6)
                                         )


def percentChange(startPoint, currentPoint):
    try:
        x = ((float(currentPoint) - startPoint) / abs(startPoint)) * 100.00
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.0001


def patternStorage(date, avgLine):
    '''
    The goal of patternFinder is to begin collection of %change patterns
    in the tick data. From there, we also collect the short-term outcome
    of this pattern. Later on, the length of the pattern, how far out we
    look to compare to, and the length of the compared range be changed,
    and even THAT can be machine learned to find the best of all 3 by
    comparing success rates.'''

    if 36 > len(avgLine): return None

    startTime = time.time()

    x = len(avgLine) - 30
    y = 5
    # currentStance = 'none'
    patternList = []

    while y < x:
        pattern = []

        sp = avgLine[y]
        p1 = percentChange(sp, avgLine[y + 1])
        p2 = percentChange(sp, avgLine[y + 2])
        p3 = percentChange(sp, avgLine[y + 3])
        p4 = percentChange(sp, avgLine[y + 4])
        p5 = percentChange(sp, avgLine[y + 5])
        p6 = percentChange(sp, avgLine[y + 6])
        p7 = percentChange(sp, avgLine[y + 7])
        p8 = percentChange(sp, avgLine[y + 8])
        p9 = percentChange(sp, avgLine[y + 9])
        p10 = percentChange(sp, avgLine[y + 10])

        p11 = percentChange(sp, avgLine[y + 11])
        p12 = percentChange(sp, avgLine[y + 12])
        p13 = percentChange(sp, avgLine[y + 13])
        p14 = percentChange(sp, avgLine[y + 14])
        p15 = percentChange(sp, avgLine[y + 15])
        p16 = percentChange(sp, avgLine[y + 16])
        p17 = percentChange(sp, avgLine[y + 17])
        p18 = percentChange(sp, avgLine[y + 18])
        p19 = percentChange(sp, avgLine[y + 19])
        p20 = percentChange(sp, avgLine[y + 20])

        p21 = percentChange(sp, avgLine[y + 21])
        p22 = percentChange(sp, avgLine[y + 22])
        p23 = percentChange(sp, avgLine[y + 23])
        p24 = percentChange(sp, avgLine[y + 24])
        p25 = percentChange(sp, avgLine[y + 25])
        p26 = percentChange(sp, avgLine[y + 26])
        p27 = percentChange(sp, avgLine[y + 27])
        p28 = percentChange(sp, avgLine[y + 28])
        p29 = percentChange(sp, avgLine[y + 29])
        p30 = percentChange(sp, avgLine[y + 30])

        outcomeRange = avgLine[y - 5:y]
        # currentPoint = avgLine[y]
        currentPoint = sp

        try:
            avgOutcome = reduce(lambda x, y: x + y, outcomeRange) / len(outcomeRange)
        except Exception as e:
            print(str(e))
            avgOutcome = 0
        futureOutcome = percentChange(currentPoint, avgOutcome)

        '''
        print 'where we are historically:',currentPoint
        print 'soft outcome of the horizon:',avgOutcome
        print 'This pattern brings a future change of:',futureOutcome
        print '_______'
        print p1, p2, p3, p4, p5, p6, p7, p8, p9, p10
        '''

        pattern.append(p1)
        pattern.append(p2)
        pattern.append(p3)
        pattern.append(p4)
        pattern.append(p5)
        pattern.append(p6)
        pattern.append(p7)
        pattern.append(p8)
        pattern.append(p9)
        pattern.append(p10)

        pattern.append(p11)
        pattern.append(p12)
        pattern.append(p13)
        pattern.append(p14)
        pattern.append(p15)
        pattern.append(p16)
        pattern.append(p17)
        pattern.append(p18)
        pattern.append(p19)
        pattern.append(p20)

        pattern.append(p21)
        pattern.append(p22)
        pattern.append(p23)
        pattern.append(p24)
        pattern.append(p25)
        pattern.append(p26)
        pattern.append(p27)
        pattern.append(p28)
        pattern.append(p29)
        pattern.append(p30)

        patternList.append((date[y], pattern, futureOutcome))

        # patternAr.append(pattern)
        # performanceAr.append(futureOutcome)

        y += 1

    endTime = time.time()
    print(len(patternList))
    # print (len(patternAr))
    # print (len(performanceAr))
    print('Pattern storing took:', endTime - startTime)

    return patternList


def currentPattern(avgLine):
    # mostRecentPoint = avgLine[-1]

    patForRec = []

    sp = avgLine[0]

    cp1 = percentChange(sp, avgLine[1])
    cp2 = percentChange(sp, avgLine[2])
    cp3 = percentChange(sp, avgLine[3])
    cp4 = percentChange(sp, avgLine[4])
    cp5 = percentChange(sp, avgLine[5])
    cp6 = percentChange(sp, avgLine[6])
    cp7 = percentChange(sp, avgLine[7])
    cp8 = percentChange(sp, avgLine[8])
    cp9 = percentChange(sp, avgLine[9])
    cp10 = percentChange(sp, avgLine[10])

    cp11 = percentChange(sp, avgLine[11])
    cp12 = percentChange(sp, avgLine[12])
    cp13 = percentChange(sp, avgLine[13])
    cp14 = percentChange(sp, avgLine[14])
    cp15 = percentChange(sp, avgLine[15])
    cp16 = percentChange(sp, avgLine[16])
    cp17 = percentChange(sp, avgLine[17])
    cp18 = percentChange(sp, avgLine[18])
    cp19 = percentChange(sp, avgLine[19])
    cp20 = percentChange(sp, avgLine[20])

    cp21 = percentChange(sp, avgLine[21])
    cp22 = percentChange(sp, avgLine[22])
    cp23 = percentChange(sp, avgLine[23])
    cp24 = percentChange(sp, avgLine[24])
    cp25 = percentChange(sp, avgLine[25])
    cp26 = percentChange(sp, avgLine[26])
    cp27 = percentChange(sp, avgLine[27])
    cp28 = percentChange(sp, avgLine[28])
    cp29 = percentChange(sp, avgLine[29])
    cp30 = percentChange(sp, avgLine[30])

    patForRec.append(cp1)
    patForRec.append(cp2)
    patForRec.append(cp3)
    patForRec.append(cp4)
    patForRec.append(cp5)
    patForRec.append(cp6)
    patForRec.append(cp7)
    patForRec.append(cp8)
    patForRec.append(cp9)
    patForRec.append(cp10)
    patForRec.append(cp11)
    patForRec.append(cp12)
    patForRec.append(cp13)
    patForRec.append(cp14)
    patForRec.append(cp15)
    patForRec.append(cp16)
    patForRec.append(cp17)
    patForRec.append(cp18)
    patForRec.append(cp19)
    patForRec.append(cp20)
    patForRec.append(cp21)
    patForRec.append(cp22)
    patForRec.append(cp23)
    patForRec.append(cp24)
    patForRec.append(cp25)
    patForRec.append(cp26)
    patForRec.append(cp27)
    patForRec.append(cp28)
    patForRec.append(cp29)
    patForRec.append(cp30)

    return patForRec

def graphRawFX():
    fig = plt.figure(figsize=(10, 7))
    ax1 = plt.subplot2grid((40, 40), (0, 0), rowspan=40, colspan=40)
    ax1.plot(date, bid)
    ax1.plot(date, ask)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.grid(True)
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date, 0, (ask - bid), facecolor='g', alpha=.3)

    plt.subplots_adjust(bottom=.23)
    plt.show()


def patternRecognition(patForRec, patternAr):
    plotPatAr = []
    patFound = 0

    for codeDate, eachPattern, outCome in patternAr:
        sim1 = 100.00 - abs(percentChange(eachPattern[0], patForRec[0]))
        sim2 = 100.00 - abs(percentChange(eachPattern[1], patForRec[1]))
        sim3 = 100.00 - abs(percentChange(eachPattern[2], patForRec[2]))
        sim4 = 100.00 - abs(percentChange(eachPattern[3], patForRec[3]))
        sim5 = 100.00 - abs(percentChange(eachPattern[4], patForRec[4]))
        sim6 = 100.00 - abs(percentChange(eachPattern[5], patForRec[5]))
        sim7 = 100.00 - abs(percentChange(eachPattern[6], patForRec[6]))
        sim8 = 100.00 - abs(percentChange(eachPattern[7], patForRec[7]))
        sim9 = 100.00 - abs(percentChange(eachPattern[8], patForRec[8]))
        sim10 = 100.00 - abs(percentChange(eachPattern[9], patForRec[9]))

        sim11 = 100.00 - abs(percentChange(eachPattern[10], patForRec[10]))
        sim12 = 100.00 - abs(percentChange(eachPattern[11], patForRec[11]))
        sim13 = 100.00 - abs(percentChange(eachPattern[12], patForRec[12]))
        sim14 = 100.00 - abs(percentChange(eachPattern[13], patForRec[13]))
        sim15 = 100.00 - abs(percentChange(eachPattern[14], patForRec[14]))
        sim16 = 100.00 - abs(percentChange(eachPattern[15], patForRec[15]))
        sim17 = 100.00 - abs(percentChange(eachPattern[16], patForRec[16]))
        sim18 = 100.00 - abs(percentChange(eachPattern[17], patForRec[17]))
        sim19 = 100.00 - abs(percentChange(eachPattern[18], patForRec[18]))
        sim20 = 100.00 - abs(percentChange(eachPattern[19], patForRec[19]))

        sim21 = 100.00 - abs(percentChange(eachPattern[20], patForRec[20]))
        sim22 = 100.00 - abs(percentChange(eachPattern[21], patForRec[21]))
        sim23 = 100.00 - abs(percentChange(eachPattern[22], patForRec[22]))
        sim24 = 100.00 - abs(percentChange(eachPattern[23], patForRec[23]))
        sim25 = 100.00 - abs(percentChange(eachPattern[24], patForRec[24]))
        sim26 = 100.00 - abs(percentChange(eachPattern[25], patForRec[25]))
        sim27 = 100.00 - abs(percentChange(eachPattern[26], patForRec[26]))
        sim28 = 100.00 - abs(percentChange(eachPattern[27], patForRec[27]))
        sim29 = 100.00 - abs(percentChange(eachPattern[28], patForRec[28]))
        sim30 = 100.00 - abs(percentChange(eachPattern[29], patForRec[29]))

        howSim = (sim1 + sim2 + sim3 + sim4 + sim5 + sim6 + sim7 + sim8 + sim9 + sim10
                  + sim11 + sim12 + sim13 + sim14 + sim15 + sim16 + sim17 + sim18 + sim19 + sim20
                  + sim21 + sim22 + sim23 + sim24 + sim25 + sim26 + sim27 + sim28 + sim29 + sim30) / 30.00

        if howSim > 80:
            patdex = patternAr.index(eachPattern)
            patFound = 1
            xp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                  29, 30]
            #############

            plotPatAr.append((codeDate, eachPattern, outCome))
            return plotPatAr

'''
    if patFound == 1:
        fig = plt.figure(figsize=(10, 6))

        for eachPatt in plotPatAr:
            futurePoints = patternAr.index(eachPatt)

            if performanceAr[futurePoints] > patForRec[9]:
                pcolor = '#24bc00'
            else:
                pcolor = '#d40000'

            plt.plot(xp, eachPatt)
            ####################
            plt.scatter(35, performanceAr[futurePoints], c=pcolor, alpha=.4)
        realOutcomeRange = allData[toWhat + 20:toWhat + 30]
        realAvgOutcome = reduce(lambda x, y: x + y, realOutcomeRange, 0) / len(realOutcomeRange)
        realMovement = percentChange(allData[toWhat], realAvgOutcome)
        plt.scatter(40, realMovement, c='#54fff7', s=25)
        plt.plot(xp, patForRec, '#54fff7', linewidth=3)
        plt.grid(True)
        plt.title(
            'Pattern Recognition.\nCyan line is the current pattern. Other lines are similar patterns from the past.\nPredicted outcomes are color-coded to reflect a positive or negative prediction.\nThe Cyan dot marks where the pattern went.\nOnly data in the past is used to generate patterns and predictions.')
        plt.show()
'''

dataLength = int(bid.shape[0])
print('data length is', dataLength)

allData = ((bid + ask) / 2)

toWhat = 40

# while toWhat < dataLength:
#    avgLine = ((bid+ask)/2)
#    avgLine = avgLine[:toWhat]

# if __name__ == '__main':
avgLine = ((bid + ask) / 2)

patternAr = []
performanceAr = []
patForRec = []

# avgOutcome = reduce(lambda x, y: x + y, outcomeRange) / len(outcomeRange)


patternStorage()
currentPattern()
patternRecognition()
totalEnd = time.time() - totalStart
print('Entire processing took:', totalEnd, 'seconds')
#    toWhat += 1

