from errorNums import *

# The data that is being used is located in ./data/example-data.csv
# It contains data that I just made up. I assume that the first and second coloumns 
# are a known constant with infinite precision, the third coloumn 
# is accurate to within +/- 0.1 and the last coloumn is accurate to within 
# +/- 0.002

# Here is my special function to calculate some special quantity
def calcSomething(args):
    # args is a list of each element in the coloumn. Every element 
    # of args is a strings

    # I know that my input data, example-data.csv, has three coloumns.
    # Therefore, there are three elements in args. I will call them A, B, 
    # and C
    
    # Remember that these will all be strings.
    rawA = args[0]
    rawB = args[1]
    rawC = args[2]
    rawD = args[3]

    A = float(rawA) #   Here I am converting A to a float which implies it 
    # has infinite sig-figs and 0 error. Internally, A will just be converted
    # to a AvgErrFloat exactly like how B is below.

    B = AvgErrFloat(float(rawB), 0, float('inf')) # Here I am converting B
    # to an AvgErrFloat where I am explicitly saying that B has 0 error and
    # infinite sig-figs

    
    C = AvgErrFloat(float(rawC), 0.1, len(rawC)-1) # Here I am setting B to have 0.1 error and 
    D = AvgErrFloat(float(rawD), 0.002, len(rawD)-1)

    # Since A is a constant and has infinte s anignificant figures and 0 error, I can 
    # just leave it as a normal float

    # Here is some meanengless arithmetic
    X = AvgErrFloat.add(AvgErrFloat.sqrt(AvgErrFloat.mul(A, C)), AvgErrFloat.pow(D, B))

    # Brandon is nice and created his class such that you can operate
    # on AvgErrFloat and floats together using the built in +, -, *,
    # /, and ** operators. He also created a sqrt() function for you.


    # This is the same thing using the builtin operators
    Y = AvgErrFloat.sqrt(A*C) + D**B

    # Now I can return the output as a list, though if there is one value it can be returned 
    # on it's own. You can use the getError() and getValue() functions as well as the str() 
    # function to get the number and its errors.

    return [X.getValue(), X.getError(), X.getPercentError(), str(Y), Y.getPercentError()]

# Now you can call the applyFuncToCSV function, pass in the calcSomething function 
# we just created, tell where the data file is, None means that we are outputing
# to the consle, and True means that I want the output data to be appended
# to the input data. Read the documentation for more information.
applyFuncToCSV(calcSomething, "data/example-data.csv", None, True)

# Here is a similar call where I am outputing the data to a file and not
# appending the output to the input
applyFuncToCSV(calcSomething, "data/example-data.csv", "example-out.csv")