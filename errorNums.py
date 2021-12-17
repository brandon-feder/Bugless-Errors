import math

class AvgErrFloat:
    # ===========================================
    # ============= Helper Methods =============
    # ===========================================

    # Returns `n` in scientific notation with `nsf` significant figures
    @staticmethod
    def __sigFigify(n, nsf, useSciNot=True):
        if useSciNot:
            if nsf == float('inf'):
                return n
            else:
                # TODO: Figure out how to do this with one `format` and no `+`.
                return ("{:#." + str(nsf-1) + "e}").format(n)
        else:
            if nsf == float('inf'):
                return n
            else:
                # TODO: Figure out how to do this with one `format` and no `+`.
                return ("{:#." + str(nsf) + "g}").format(n)

    def __errify(err, lastd, useSciNot=True):

        nsf = math.ceil(math.log10(abs(err))) - lastd + 1

        if useSciNot:
            if(nsf <= 0):
                return ("{:#.0e}").format(0)
            else:
                return ("{:#." + str(nsf-1) + "e}").format(err)
        else:
            if nsf <= 0:
                return ("{:#.0e}").format(0)
            else:
                return ("{:#." + str(nsf) + "g}").format(err)

    # Checks that an operator argument is a valid type, and returns a valid 
    # argument as an `AvgErrFloat`
    @staticmethod
    def __checkAvgErrFloat(B):
        if isinstance(B, float) or isinstance(B, int):
            return AvgErrFloat(B, 0, float('inf'))
        elif not isinstance(B, AvgErrFloat):
            raise TypeError
        else:
            return B
        
    # ===========================================
    # ============== Constructors ===============
    # ===========================================

    def __init__(self, val, err=0, nsf=float('inf')):
        if(
            (isinstance(val, float) or isinstance(val, int)) and
            (isinstance(err, float) or isinstance(err, int)) and
            isinstance(nsf, int) or nsf==float('inf')
        ):
            self.val = val
            self.err = err
            self.nsf = nsf
        else:
            raise TypeError("Invalid constructor arguments")

    # ===========================================
    # =============== Operations ================
    # ===========================================

    @staticmethod
    def add(A, B):
        A = AvgErrFloat.__checkAvgErrFloat(A)
        B = AvgErrFloat.__checkAvgErrFloat(B)

        return AvgErrFloat(
            A.val + B.val,
            A.err + B.err,
            min(A.nsf, B.nsf)
        )

    @staticmethod
    def sub(A, B):
        A = AvgErrFloat.__checkAvgErrFloat(A)
        B = AvgErrFloat.__checkAvgErrFloat(B)

        return AvgErrFloat(
            A.val - B.val,
            A.err + B.err,
            min(A.nsf, B.nsf)
        )

    @staticmethod
    def mul(A, B):
        A = AvgErrFloat.__checkAvgErrFloat(A)
        B = AvgErrFloat.__checkAvgErrFloat(B)

        if A.val == 0 or B.val == 0:
            return AvgErrFloat(0, 0, min(A.nsf, B.nsf))
        else:
            return AvgErrFloat(
                A.val*B.val,
                (A.err/A.val + B.err/B.val)*A.val*B.val, 
                min(A.nsf, B.nsf)
            )

    @staticmethod
    def div(A, B):
        A = AvgErrFloat.__checkAvgErrFloat(A)
        B = AvgErrFloat.__checkAvgErrFloat(B)

        if A.val == 0:
            return AvgErrFloat(0, 0, min(A.nsf, B.nsf))
        elif B.val == 0:
            raise ZeroDivisionError
        else:
            return AvgErrFloat(
                A.val*B.val,
                (A.err/A.val + B.err/B.val)*(A.val/B.val), 
                min(A.nsf, B.nsf)
            )

    @staticmethod
    def pow(A, m):
        A = AvgErrFloat.__checkAvgErrFloat(A)

        # Make sure `m` is a float or an integer. Convert it to a float.
        if not ( (isinstance(m, AvgErrFloat) and m.err == 0) or isinstance(m, float) or isinstance(m, int) ):
            raise TypeError("Exponenet must be an integer, float, or a AvgErrFloat with 0 error.")
        else:
            m = float(m)
        
        if A.val == 0:
            return AvgErrFloat(0, 0, A.nsf)
        else:
            return AvgErrFloat(
                A.val**m, 
                (abs(m)*A.err/A.val)*(A.val**m), 
                A.nsf
            )

    @staticmethod
    def sqrt(A):
        return AvgErrFloat.pow(A, 0.5)

    # ===========================================
    # ========== Operator Overloading ===========
    # ===========================================

    # overload `str()` function
    def __str__(self):
        return "{} ± {} ({} sig figs)".format(
            self.getValue(),
            self.getError(),
            self.nsf
        )
    
    # overload `float()` function
    def __float__(self): return self.val

    # other operators
    def __add__(A, B): return AvgErrFloat.add(A, B)
    def __radd__(A, B): return AvgErrFloat.add(A, B)

    def __sub__(A, B): return AvgErrFloat.sub(A, B)
    def __rsub__(A, B): return AvgErrFloat.add(A, B)
    
    def __mul__(A, B): return AvgErrFloat.mul(A, B)
    def __rmul__(A, B): return AvgErrFloat.mul(A, B)

    def __truediv__(A, B): return AvgErrFloat.div(A, B)
    def __rtruediv__(A, B): return AvgErrFloat.div(A, B)

    def __pow__(A, m): return AvgErrFloat.pow(A, m)

    # ===========================================
    # ============== Member Access ==============
    # ===========================================

    def getValue(self, useSciNot=True):
        return AvgErrFloat.__sigFigify(self.val, self.nsf, useSciNot)

    def getError(self, useSciNot=True):
        lastd = math.ceil(math.log10(self.val)) - self.nsf
        return AvgErrFloat.__errify(self.err, lastd, useSciNot)

    def getPercentError(self, ndig=3):
        return str(round(float(self.getError())/float(self.getValue())*100, ndig)) + "%"

def printTabular(raw):
    # Get a list of lines
    lines = raw.split("\n")

    # Splot element in each line
    for i in range(len(lines)): lines[i] = lines[i].split(",")

    # Get the maximum length of each coloumn
    M = [6]*len(lines[0])
    for line in lines:
        for i in range(len(line)):
            if len(line[i]) > M[i]:
                M[i] = len(line[i])
    
    # Get the string that will be formatted
    formatStr = ""
    for i, l in enumerate(M): formatStr += " {:<" + str(l) + "} "

    # Create the first row
    out = formatStr.format(*[
        "Col " + str(i) for i in range(len(lines[0]))
    ]) + "\n"

    # Create all the other rows
    for line in lines: out += formatStr.format(*line) + "\n"
    
    # Print
    print(out)

def applyFuncToCSV(func, finPath, foutPath=None, foutAppendToIn=False):
    # Open the input file
    fin = open(finPath, "r")

    out = "" 

    # For each line
    for line in fin:
        # Remove new line charecter
        line = line.replace("\n", "")

        # Get the output and make it as string
        res = str(func(line.split(","))).replace("[", "").replace("]", "")

        # Add to the output
        if foutAppendToIn:
            out += line[0:-1] + ", "   
        out += res + "\n"

    # Format the output
    out = out[0:-1]

    # Output
    if foutPath == None:
        printTabular(out)
    else:
        fout = open(foutPath, "w")
        fout.write(out)