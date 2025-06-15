import pandas 
import matplotlib.pyplot
import seaborn 
import math
from scipy.stats import chi2 # for chi square table

# reading data from the table using pandas lib.

TableOfData = pandas.read_csv(r"C:\Users\Motasem\Desktop\MOTASEM YILDIZ 2221221380 P&S\archive (1)\Sleep_health_and_lifestyle_dataset.csv")


SleepDuration= TableOfData["Sleep Duration"]


#### Descriptive Statistics ##### : 

# Mean: measuaring the average value of the sample
# The formula to find mean is sum of values in a sample / number of values in a sample

def Mean(SleepDuration):

    return sum(SleepDuration) / len(SleepDuration)



# Median : A Median is a middle value for sorted data.
# To find the Medain , first i will sort the values of sample. Then there are two cases:
# if the number of values is odd, the median is the value in the middle
# but if the number of values is even, the median is the sum of the two middle numbers divided by 2

def Median(SleepDuration):
    
    SortedValues = sorted(SleepDuration)
    n = len(SortedValues)
    
    if n == 0:
        return None  

    
    if n % 2 != 0: # odd
        middle_index = n // 2
        result = SortedValues[middle_index]
    else: # even
        mid1 = SortedValues[(n // 2) - 1]
        mid2 = SortedValues[n // 2]
        result = (mid1 + mid2) / 2

    return result



# Variance:is a number that tells us how spread out the values in a data set are from the mean.
# The formul to find variance is ( ∑(x - mean) ^ 2) / (n-1)  
# The sum  of each value - the mean to the power of 2  then divided by the number of values - 1

def Variance(SleepDuration):

    resault = 0
    mean = Mean(SleepDuration)
    n = len(SleepDuration)

    for i in SleepDuration:

        resault += ( i - mean) ** 2

    resault = resault / (n-1)

    return resault


# Standard Deviation: a measure of how dispersed the data is in relation to the mean
# Standard Deviation is the square root of the variance

def StandardDeviation(SleepDuration):
    resault = 0
    variance = Variance(SleepDuration)

    resault = variance ** 0.5

    return resault

#  Standard Error: Standard Error is the measure of the variability of a sample statistic used to estimate the variability of a population
# The formul to find SE is  SE = sd / len^0.5
# standard deviation divided by the square root of the number of values of a sample 

def StandardEror(SleepDuration):
    resault = 0
    sd = StandardDeviation(SleepDuration)
    n = len(SleepDuration) 
    
    resault = sd / (n**0.5)

    return resault



#### Confidence Intervals ###:
# In statistics, a confidence interval (CI) is a range of values used to estimate an unknown statistical > 
# >parameter, such as a population mean.
# Construct 95% confidence intervals for both the population mean and variance.
# The formul to find  CImean = mean of sample +- t(df) * (standard dav. / square root number of values)
# t: t-critical value , from (t-distribution table A5)
# df(Degrees of Freedom) df = number of values - 1 (df = 373)
# So tdf will be = 1.960 (NOT: df > 100 so t will be very close from z so we use t = 1.96)
# Not: a(alpha) = 0.05 for %95 then a/2 = 0.025 (divided by 2 because (two-tailed))
# https://wildart.github.io/CSC21700/t-table.pdf     A5 table

def CImean(SleepDuration):
    tdf = 1.960
    sd = StandardDeviation(SleepDuration)
    mean = Mean(SleepDuration)
    n = len(SleepDuration)

    upper = mean + (tdf * (sd / n**0.5))
    lower = mean - (tdf * (sd / n**0.5))

    return(lower , upper)

# Now to find CIvar = ((n - 1) * sample_variance / chiUpper , (n - 1) * sample_variance / chiLower)
# we will find chiUpper and chiLower values from chi-square table (A6)
# (df = 373 ) there is no df = 373 in A6 table so i will use ready funtions to find chiUpper and chiLower
# chiUpper = chi2.ppf(1 - alpha / 2, df) alpha = 0.05 
# chiLower = chi2.ppf(alpha / 2, df)
# https://math.arizona.edu/~jwatkins/chi-square-table.pdf Table A6

def CIvar(SleepDuration):
    
    var = Variance(SleepDuration)
    n = len(SleepDuration)
    a = 0.05
    df = 373

    chiUpper = chi2.ppf(1 - a / 2, df)
    chiLower = chi2.ppf(a / 2, df) 

    lower = ((n - 1) * var) / chiLower
    upper = ((n - 1) * var) / chiUpper

    return( float(upper) , float(lower)) 



### Sample Size Estimation ###:
# the minimum sample size required to estimate the population mean with a maximum> 
#> margin of error of 0.1 units at a 90% confidence level.
# the formul to find sample size estimation is ((standart dav. * z ) / E)^2
# E: Margin of Error (0.1)
# z: z-critical value we will find z from standard normal (Z) distribution table A4
# for %90 then 1 - 0.90 = 0.10 then a/2 = 0.05
# now from table A4 for 0.95 >> z = 1.645
# https://math.arizona.edu/~rsims/ma464/standardnormaltable.pdf A4 table

def SampleSizeEstimation(SleepDuration):
    z = 1.645
    E = 0.1
    sd = StandardDeviation(SleepDuration)

    resault = ((sd * z) / E) ** 2
    return resault

### Hypothesis Testing ###:
# Hypothesis testing is a statistical method used to determine if there is enough evidence
# in a sample to draw conclusions about a population.
# First, we will make an assumption about the population.
# For example, we assume that the average sleep duration in the population is 7.0 hours.
# H0: Hypothesis mean = 7.0 and H1: Hypothesis mean != 7.0         
# Then we will calculate the sample statistics: 
# mean, standard deviation, and number of values
# After that, we will compute the t-statistic using the formula:
# t = (mean - hypothesized mean) / (standard deviation / √n)
# Then we will find the t-critical value from the t-distribution table A5 (1.96) 
# Finally, we compare the t-statistic with the t-critical value:
# If |t| > t_critical we reject H0
# Otherwise we fail to reject H0

def HypothesisTesting(SleepDuration , hypothesizedMean = 7.0):

    tcri = 1.96
    mean = Mean(SleepDuration)
    sd = StandardDeviation(SleepDuration)
    n = len(SleepDuration)

    tStatistics = (mean - hypothesizedMean) / (sd / n**0.5)

    if abs(tStatistics) > tcri:
        return "Reject H0"
    else:
        return "Fail to reject H0" 
    
# print values
print(f"Mean:{Mean(SleepDuration)}")
print(f"Median:{Median(SleepDuration)}")
print(f"Variance:{Variance(SleepDuration)}")
print(f"Standard Deviation:{StandardDeviation(SleepDuration)}")
print(f"Standard Eror:{StandardEror(SleepDuration)}")
print(f"CImean:{CImean(SleepDuration)}")
print(f"CIvariance:{CIvar(SleepDuration)}")
print(f"Sample Size Estimation:{SampleSizeEstimation(SleepDuration)}")
print(f"Hypothesis Testing:{HypothesisTesting(SleepDuration , 7.0)}")


#### Data Visualization ###:
# Now i will use matplotlib.pyplot and seaborn libraries to represent data visualization

#histogram
matplotlib.pyplot.hist(SleepDuration, bins=10, edgecolor='black', color='skyblue') 
matplotlib.pyplot.xlabel("Sleep duration - hour")
matplotlib.pyplot.ylabel("Frequency")
matplotlib.pyplot.grid(True)
matplotlib.pyplot.show()

#boxplot
seaborn.boxplot(x=SleepDuration, color='lightgreen')
matplotlib.pyplot.xlabel("Sleep duration - hour")
matplotlib.pyplot.grid(True)
matplotlib.pyplot.show()










 












