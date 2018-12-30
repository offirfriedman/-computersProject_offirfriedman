import sys # importing system function for exit with error
from math import * # importing math functions
import matplotlib
import matplotlib.pyplot as plt #imprting graph functions
import numpy as np
#main function
def fit_linear(fileName):  # main function. this function input is a text file of data and output is a fitting parametes and a saved graph
    fileData = reading_file(fileName) # calling readig data function
    dataDict = prepareInput(fileData) #calling the function that makes dictionary from the data
    dataDict = calcAllParametes(dataDict) #calling the function that calculate the parameters and adds them to the Dict
    printAllParameters(dataDict) #calling the function that prints the parameters
    drawLine(dataDict) #calling the function that save the graph

#functions for part 1

#this function reads the data from notepad. input is a file name as a string including .filetype and output is a list of strings
def reading_file(file_input):
    file_pointer=open(file_input)
    data=file_pointer.readlines()
    file_pointer.close()
    final=[]
    for string in data:
        string_1=string.lower()[:] #taking only small letters
        string_2=string_1.replace("\n","")[:] # removing \n
        final.append(string_2)
    return final

#this function creats the data dictionary, input is list of strings and output is a dictionary
def prepareInput(data):
    temp = stringToList(data) #calling the function that makes the strings to lists
    if (isDataMissing(temp)): #checking that each row of data as the same length
        exitOnError("Input file error: Data lists are not the same length.")
    else:
        if isDataCols(temp):  # taking data for cols input
            dataDict = prepareDataFromCols(temp)
        else:  # taking data for rows input
            dataDict = prepareDataFromRows(temp)

        dataDict = addLabelsOfAxis(data, dataDict) #adding the labels

        if isErrorZero(dataDict): #checking that thera are no none positve error
            exitOnError("Input file error: Not all uncertainties are positive.")
        return dataDict

#this function turns the strings into lists input data as a list
def stringToList(data):
    temp=[]
    for x in range(0,len(data)-3):
        split_1=data[x].split(" ")
        real_split=[]
        for y in split_1: #remove extra spaces
            if y!='':
                real_split.append(y)
        temp.append(real_split)
    return temp

#this function check if there is data missing. input is data before it's a dict
def isDataMissing(data):
    isMissing = False
    dataLength = len(data[0])

    for x in data:
        if len(x) != dataLength:
            isMissing = True
            break

    return isMissing

# this function Checkes if dx or dy are non positive
def isErrorZero(dataDict):
    hasNonPositive = False

    for x in dataDict['dx']:
        if x <= 0:
            hasNonPositive = True
            break

    if not hasNonPositive:
        for x in dataDict['dy']:
            if x <= 0:
                hasNonPositive = True
                break

    return hasNonPositive

#this function Checks the structure of the data
def isDataCols(data):
    if data[0][1]=='dx' or data[0][1]=='dy' or data[0][1]=='x' or data[0][1]=='y':
        return True
    else:
        return False;

#this function creats dict from the data if the stracture is cols
def prepareDataFromCols(data):
    data_dict={}
    for y in [0, 1, 2, 3]:
        list_values = []  # temporary var
        for x in range(1, len(data)):
            value = float(data[x][y])
            list_values.append(value)
        data_dict[data[0][y]] = list_values
    return data_dict

#this function creats dict from the data if the stracture is rows
def prepareDataFromRows(data):
    data_dict={}
    for x in data:
        list_values = []  # temporary var
        for y in range(1, len(x)):
            value = float(x[y])
            list_values.append(value)
        data_dict[x[0]] = list_values
    return data_dict

#this function adds the axis names to the dict
def addLabelsOfAxis(data, data_dict):
    x_axis = data[len(data) - 2][8:]  # keep the x axis
    y_axis = data[len(data) - 1][8:]  # keep the y axis
    data_dict["x_axis"] = x_axis  # appendig to dict
    data_dict["y_axis"] = y_axis  # apendding to dict
    return data_dict

#this function ouput error message. input is a string
def exitOnError(errorDescription):
    sys.exit(errorDescription) #this is a function from phyton libary

#functions for part 2

#this functin takes list of values and list of errors and return the bar of the list
def xBar(x,dy):
    sum_1=0
    for z in range(0,len(x)):
        sum_1=sum_1+x[z]/((dy[z]*dy[z]))
    sum_2=0
    for z in range(0,len(x)):
        sum_2=sum_2+1/((dy[z]*dy[z]))
    xbar=sum_1/sum_2
    return xbar

#this function takes two lists with the same length and returns a list of the multplyiction of every elemnt in each list
def list_mult(x,y):
    output=[]
    for z in range(0,len(x)):
        temp=x[z]*y[z]
        output.append(temp)
    return output

#this functin calculates a parmeter in the linear function y=ax +b.
def calc_a(x,y,dy):
    xy=list_mult(x,y)
    x_2=list_mult(x,x)
    x_bar=xBar(x,dy)
    x_2_bar=xBar(x_2,dy)
    xy_bar=xBar(xy,dy)
    y_bar=xBar(y,dy)
    a=(xy_bar-x_bar*y_bar)/(x_2_bar-x_bar*x_bar)
    return a

#this function calculates b parmeter in the linear functio y=ax +b.
def calc_b(x,y,dy):
    y_bar=xBar(y,dy)
    x_bar=xBar(x,dy)
    a=calc_a(x,y,dy)
    b=y_bar-a*x_bar
    return b

#this function calculates the error in the parameter a
def calc_da(x,dy):
    dy_2=list_mult(dy,dy)
    x_2=list_mult(x,x)
    x_2_bar=xBar(x_2,dy)
    dy_2_bar=xBar(dy_2,dy)
    x_bar=xBar(x,dy)
    da=sqrt(dy_2_bar/(len(x)*(x_2_bar-x_bar*x_bar)))
    return da

#this function calculates the error in the parameter b
def calc_db(x,dy):
    dy_2=list_mult(dy,dy)
    x_2=list_mult(x,x)
    x_2_bar=xBar(x_2,dy)
    dy_2_bar=xBar(dy_2,dy)
    x_bar=xBar(x,dy)
    db=sqrt((dy_2_bar*x_2_bar)/(len(x)*(x_2_bar-x_bar*x_bar)))
    return db

#this function calculates the chi squere - for a and b.
def calc_chi(a,b,x,y,dy):
    s=0
    for z in range(0,len(x)):
        s=s+((y[z]-a*x[z]-b)/dy[z])**2
    return s

#this function calculates reduce chi
def calc_chi_red(chi,x):
    chi_red=chi/(len(x)-2)
    return chi_red

#this function calculates all needed parametes and adds them to the data dictionary
def calcAllParametes(dataDict):
    x=dataDict['x']
    y=dataDict['y']
    dy=dataDict['dy']
    a=calc_a(x,y,dy)
    b = calc_b(x, y, dy)
    da=calc_da(x,dy)
    db = calc_db(x, dy)
    chi=calc_chi(a,b,x,y,dy)
    chi_red=calc_chi_red(chi,x)
    dataDict['a']=a
    dataDict['b']=b
    dataDict['da']=da
    dataDict['db']=db
    dataDict['chi']=chi
    dataDict['chi_red']=chi_red
    return dataDict

#this function print all of the parameters
def printAllParameters(datDict):
    print('a=',datDict['a'],'+-',datDict['da'],sep='')
    print('b=',datDict['b'],'+-',datDict['db'],sep='')
    print('chi2=',datDict['chi'],sep='')
    print('chi2_reduced=',datDict['chi_red'],sep='')

#functions for part 3

#this function draws the graph and saves it
def drawLine(dataDict):
    x = np.linspace(min(dataDict['x']),max(dataDict['x'])) #creating a line space for the length of the data
    y = dataDict['a']*x+dataDict['b'] #calc y according to the parameters
    plt.xlabel(dataDict['x_axis']) #plotting labels
    plt.ylabel(dataDict['y_axis'])
    plt.plot(x, y,color='red') #plot the line
    x = dataDict['x']
    y = dataDict['y']
    dy = dataDict['dy']
    dx = dataDict['dx']
    plt.errorbar(x, y,xerr=dx, yerr=dy, fmt='b,') #plotting error bars
    plt.savefig('linear_fit.SVG') #saving the data
