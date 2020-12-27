#!/usr/bin/python3

'''
start_block_number: 11243754 (1605197144)
end_block_number: 11291000 (1605822429)
'''

import csv
import numpy as np


def getUSDTValue(symbol, principal):
    ETHPrice = 618.15
    WBTCPrice = 24340.70
    KNCPrice = 0.83
    MKRPrice = 534.47
    BZRXPrice = 0.1644
    LINKPrice = 11.49
    YFIPrice = 23302
    UNIPrice = 3.46
    AAVEPrice = 76.93
    COMPPrice = 136.08
    LRCPrice = 0.1515

    if symbol == 'ETH':
        return principal * ETHPrice
    elif (symbol == 'WBTC'):
        return principal * WBTCPrice
    elif (symbol == 'LEND'):
        print("lend is removed")
        return 0
    elif (symbol == 'KNC'):
        return principal * KNCPrice
    elif (symbol == 'MKR'):
        return principal * MKRPrice
    elif (symbol == 'BZRX'):
        return principal * BZRXPrice
    elif (symbol == 'LINK'):
        return principal * LINKPrice
    elif (symbol == 'YFI'):
        return principal * YFIPrice
    elif (symbol == 'UNI'):
        return principal * UNIPrice
    elif (symbol == 'AAVE'):
        return principal * AAVEPrice
    elif (symbol == 'COMP'):
        return principal * COMPPrice
    elif (symbol == 'LRC'):
        return principal * LRCPrice
    elif (symbol == 'USDT' or symbol == 'USDC' or symbol == 'DAI'):
        return principal
    else:
        raise ValueError("unhandled symbol", symbol)


filePath = './week16.csv'
num_lines = sum(1 for line in open(filePath))
with open(filePath, newline='') as csvfile:

    transactions = csv.reader(csvfile, delimiter=',')
    next(transactions)  # skip header

    # Tom if you are going to change below you have to rerun sql
    lastWeekRewardBlock = 1608233705 # block 11472580
    thisWeekRewardBlockEnd = 1608832073 # block 11517746

    prevUserAddress = 0
    prevBlockTime = 0

    totalPrincipalSumUntillLastWeekInUSDT = 0

    totalPrincipalSumOverTimeFromLastWeekInUSDT = 0

    overallResults = []

    #Prices in USDT

	# useraddress,loantoken,tokensymbol,block_time,index,paymenttype,newprincipaldecimal

    for row in transactions:
        useraddress = row[0]
        loantoken = row[1]
        tokensymbol = row[2]
        block_time = int(row[3])
        index = row[4]
        paymenttype = row[5]
        newprincipaldecimal = np.around(float(row[6]), decimals=5)

        if (prevUserAddress != useraddress or num_lines == transactions.line_num):  # count last result as well

            # totalPrincipalSumUntillLastWeekInUSDT = np.around(
            #     totalPrincipalSumUntillLastWeekInUSDT, decimals=2)

            # if (totalPrincipalSumUntillLastWeekInUSDT > 0):
            if (totalPrincipalSumOverTimeFromLastWeekInUSDT > 0 or totalPrincipalSumUntillLastWeekInUSDT > 0):
                # this week user didn't have any action but he has principal from last week
                timeBetweenActions = thisWeekRewardBlockEnd - block_time
                totalPrincipalSumOverTimeFromLastWeekInUSDT = totalPrincipalSumOverTimeFromLastWeekInUSDT + \
                    totalPrincipalSumUntillLastWeekInUSDT * timeBetweenActions

                print(prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT,
                    totalPrincipalSumOverTimeFromLastWeekInUSDT)
                overallResults.append(
                    [prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT, totalPrincipalSumOverTimeFromLastWeekInUSDT])
            elif (totalPrincipalSumOverTimeFromLastWeekInUSDT > 0):
                # extend untill end of the week
                timeBetweenActions = thisWeekRewardBlockEnd - block_time
                totalPrincipalSumOverTimeFromLastWeekInUSDT = totalPrincipalSumOverTimeFromLastWeekInUSDT + \
                    totalPrincipalSumUntillLastWeekInUSDT * timeBetweenActions

                print(prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT,
                    totalPrincipalSumOverTimeFromLastWeekInUSDT)
                overallResults.append(
                    [prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT, totalPrincipalSumOverTimeFromLastWeekInUSDT])


            prevUserAddress = useraddress
            totalPrincipalSumUntillLastWeekInUSDT = 0
            totalPrincipalSumOverTimeFromLastWeekInUSDT = 0
            prevBlockTime = block_time


        if (block_time < lastWeekRewardBlock):
            # calculating outstanding principal in the begining of the week
            if (paymenttype == 'borrow' or paymenttype == 'trade'):
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT + \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))
            else:
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT - \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))
        else:
            # calculate form last week onwards counting time as well
            if prevBlockTime < lastWeekRewardBlock:
                prevBlockTime = lastWeekRewardBlock
            
            timeBetweenActions = block_time - prevBlockTime

            if (timeBetweenActions == 0):
                timeBetweenActions = 1
            # print("wer;re here", useraddress, timeBetweenActions, totalPrincipalSumUntillLastWeekInUSDT, block_time , prevBlockTime, paymenttype, newprincipaldecimal)

            totalPrincipalSumOverTimeFromLastWeekInUSDT = totalPrincipalSumOverTimeFromLastWeekInUSDT + \
                totalPrincipalSumUntillLastWeekInUSDT * timeBetweenActions

            if (paymenttype == 'borrow' or paymenttype == 'trade'):
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT + \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))
            else:
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT - \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))




        # if (useraddress == '00000000000000000000000095494598be091c63f90543abab37fb2594ad7670'):
        #     if (block_time < lastWeekRewardBlock):
        #         print("before week", useraddress)
        #     else:
        #         print("after", useraddress)
        #     print("debug",useraddress, float(newprincipaldecimal), totalPrincipalSumUntillLastWeekInUSDT, paymenttype, totalPrincipalSumOverTimeFromLastWeekInUSDT, block_time, lastWeekRewardBlock, thisWeekRewardBlockEnd)


print("number of addresses eligible for rewards", len(overallResults))

print("calculating ALL principal over time")

totalOverTimeEverybody = 0

for row in overallResults:
    totalOverTimeEverybody = totalOverTimeEverybody + row[2]
print("totalOverTimeEverybody", totalOverTimeEverybody)


print("calculating ratios")
for row in overallResults:
    row.append(row[2]/totalOverTimeEverybody)
    # print("row", row)


print("results:")
for row in overallResults:
    # print(row[0], '{0:.4f}'.format(row[3] * 695250), '{0:.0f}'.format(row[3] * 695250 * 1000000000000000000))
    print('0x'+row[0][24:], '{0:.4f}'.format(row[3] * 695250), '{0:.0f}'.format(row[3] * 695250 * 1000000000000000000))
