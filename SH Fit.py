# MGA-1 4-parameter S-H Fit
# Author: Tyson Aramaki

try:
    import csv
    import numpy
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
except:
    print("One or more packages is not installed. \nThis script requires packages csv, numpy, scipy, and matplotlib. \nMake sure these are installed, and try again.")


### USER INPUTS BEGIN --------------------------------------------
Tdata = []
Rdata = []
R25 = 10000 
Nominal_coeffs = [0.003354016,0.000300131,0.00000508516,0.000000218765] # Default S-H values for the thermistor in question (and R25!)
### USER INPUTS END ---------------------------------------------

# read data from CSV file
with open('data.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    row1 = next(datareader)
    for row in datareader:
        #print(row)
        Rdata.append(float(row[1])) 
        Tdata.append(float(row[0]))

print("\nTemps from datafile:" + str(Tdata))
print("Resistances from datafile:" + str(Rdata))

# Steinhart-Hart-Equation
def f(x, a0, a1, a2, a3):
    return 1 / (a0 + a1 * numpy.log(x/R25) + a2 * numpy.power(numpy.log(x/R25),2) + a3 * numpy.power(numpy.log(x/R25),3))-273.15

# Do the fit with initial values (needed, otherwise no meaningful result)
coefficients, cov = curve_fit(f, Rdata, Tdata, p0=Nominal_coeffs)

print("\nCoefficients: {}".format(coefficients))

# generate curve with fit result
Tfit = []
for v in Rdata: 
    Tfit.append(f(v, coefficients[0], coefficients[1], coefficients[2], coefficients[3]))

Tdiffs = []
for i in range(len(Tdata)):
    Tdiffs.append(float(Tfit[i]-Tdata[i]))
print("Tdiffs: {}".format(Tdiffs))
sumofsquares = 0
for i in range(len(Tdata)):
    sumofsquares = sumofsquares+(Tdiffs[i]*Tdiffs[i])
print("SSE: "+ str(sumofsquares)+'\n')

# export results to csv
header = ['a','b','c','d','SSE']
with open('output.csv', 'w', newline='') as outputfile:
    writer = csv.writer(outputfile)
    writer.writerow(header)
    data = numpy.append(coefficients,sumofsquares)
    writer.writerow(data)

# plot original data and result
plt.plot(Rdata, Tdata, 'o', label='Data')
plt.plot(Rdata, Tfit, label='Fit')
plt.legend()

plt.show()

