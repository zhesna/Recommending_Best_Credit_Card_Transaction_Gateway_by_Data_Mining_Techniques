#Zhila Esna Ashari
#Spreedly Project- February 2017
#Code for Q1

import csv
import numpy as np
import matplotlib.pyplot as plt
 
myfile=open('intern2017.csv')
datareader=csv.reader(myfile)
data=list(datareader)

nrow= len(data) #number of rows
ncol= len(data[0]) #number of columns
transaction_column = [item[4] for item in data]
transaction_types=set(transaction_column)#find out the types of transactions
transaction_types.remove('transaction_type')#just remove the header
transaction_types=list(transaction_types)

print "transaction types:",
for j in range(len(transaction_types)):
    print transaction_types[j],
print "\n"
############################################
#calculate success rate for different types of transaction

counter_transactions_GA=[0]*len(transaction_types) 
counter_transactions_GB=[0]*len(transaction_types)
counter_transaction_suceeded_GA=[0]*len(transaction_types)
counter_transaction_suceeded_GB=[0]*len(transaction_types)

for i in range(1,nrow):#over all the rows of data
    for trans in range(0,len(transaction_types)):#over different transactions
        if data[i][4]==transaction_types[trans]:
            if data[i][5]=="GA":
                counter_transactions_GA[trans]+=1
                if data[i][3]=="succeeded":
                    counter_transaction_suceeded_GA[trans] +=1
            elif data[i][5]=="GB":
                counter_transactions_GB[trans]+=1
                if data[i][3]=="succeeded":
                    counter_transaction_suceeded_GB[trans] +=1
                    
##calculate and print success rates
for trans in range(0,len(transaction_types)):
    if counter_transactions_GA[trans]!=0:
        success_rate_transaction_GA=counter_transaction_suceeded_GA[trans]/float(counter_transactions_GA[trans])
        print "GA: success_rate_transaction for ", transaction_types[trans]+"= ", success_rate_transaction_GA
    else:
        print "GA: No ", transaction_types[trans]+" transaction"
    if counter_transactions_GB[trans]!=0:
        success_rate_transaction_GB=counter_transaction_suceeded_GB[trans]/float(counter_transactions_GB[trans])
        print "GB: success_rate_transaction for ", transaction_types[trans]+"= ", success_rate_transaction_GB
    else:
        print "GB: No ", transaction_types[trans]+" transaction"
    


#############################################
#calculate monthly success rate ffor purchases

date = [item[2] for item in data]#select the epoch_date column
del(date[0])#remove header
min_date=min(date)
max_date=max(date)
num_months=int((float(max_date)-float(min_date))/2628288.0)+1 #on average a month has 30.42 days and therefore it has 30.42*24*60*60= 2628288.0 seconds
#we have total number of months during which the transactions have been done

counter_transactions_monthly_GA=[0]*num_months #[0]*len(transaction_types)
counter_transactions_monthly_GB=[0]*num_months
counter_transaction_suceeded_monthly_GA=[0]*num_months
counter_transaction_suceeded_monthly_GB=[0]*num_months

for i in range(1,nrow):#over all the rows of data
    if data[i][4]=="Purchase":
        month=int((float(data[i][2])-float(min_date))/2628288.0)
        #print month
        if data[i][5]=="GA":
            counter_transactions_monthly_GA[month]+=1
            if data[i][3]=="succeeded":
                counter_transaction_suceeded_monthly_GA[month]+=1
        elif data[i][5]=="GB":
            counter_transactions_monthly_GB[month]+=1
            if data[i][3]=="succeeded":
                counter_transaction_suceeded_monthly_GB[month]+=1


zeros=[] #find months that did not have any purchases, to eliminate them from success rate calculations(to prevent divide by zero)
for i in range(num_months):
    if counter_transactions_monthly_GA[i]==0 or counter_transactions_monthly_GB[i]==0:
        zeros.append(i)

del(counter_transactions_monthly_GB[0:len(zeros)])
del(counter_transaction_suceeded_monthly_GB[0:len(zeros)])


#calculate the monthly success rates
success_rate_transaction_month_GA=[float(b) / float(m) for b,m in zip(counter_transaction_suceeded_monthly_GA, counter_transactions_monthly_GA)]
success_rate_transaction_month_GB=[float(b) / float(m) for b,m in zip(counter_transaction_suceeded_monthly_GB, counter_transactions_monthly_GB)]
                
#print success_rate_transaction_month_GA
#print success_rate_transaction_month_GB

#plotting monthly success rates
axis_months=range(len(zeros)+1,num_months+1)
axis_months2=range(1,num_months+1)
plt.scatter(axis_months2, success_rate_transaction_month_GA)
plt.xlabel('Months')
plt.ylabel('GA monthly success rate for purchases')
plt.show()

plt.scatter(axis_months, success_rate_transaction_month_GB)
plt.xlabel('Months')
plt.ylabel('GB monthly success rate for purchases')
plt.show()


del(success_rate_transaction_month_GA[0:len(zeros)])
plt.scatter(success_rate_transaction_month_GA,success_rate_transaction_month_GB)
plt.xlabel('GA monthly success rate for purchases')
plt.ylabel('GB monthly success rate for purchases')
plt.show()
