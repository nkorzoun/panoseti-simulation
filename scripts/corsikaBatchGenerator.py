# imports
import numpy as np
import sys
import argparse

# input template 
inptemp='''RUNNR 1
EVTNR 1
NSHOW 100
PRMPAR 1
ERANGE 1E2 1E2
ESLOPE -2.5
THETAP 0. 0.
PHIP 0. 360.
SEED 200 0 0
SEED 202 0 0
SEED 204 0 0
SEED 206 0 0
ATMOD 1
MAGNET 25.2 40.88
ARRANG 10.4
ELMFLG F T
RADNKG 200.E2
FIXCHI 0.
HADFLG 0 0 0 0 0 2
QGSJET T 0
QGSSIG T
HILOW 100.
ECUTS 0.30 0.05 0.02 0.02
MUADDI F
MUMULT T
LONGI T 20. F F
MAXPRT 50
PAROUT F F
ECTMAP 1.E6
DEBUG F 6 F 1000000
DIRECT ./
USER nkorzoun 
HOST caviness
ATMOSPHERE 61 T
TELFIL ./DATbatch0.telescope
OBSLEV 1239.E2
CSCAT 1 200.E2 200.E2
CERFIL 0
CERSIZ 5.
CWAVLG 200. 700.
TELESCOPE 53.59E2 73.52E2 1E2 0.25E2
TELESCOPE 53.59E2 -80.48E2 1E2 0.25E2
TELESCOPE -107.18E2 6.95E2 1E2 0.25E2
EXIT'''

# definition of line number in inp from keyword
keyword = {
    "EVTNR": 1,
    "NSHOW": 2,
    "PRMPAR": 3,
    "ERANGE": 4,
    "ESLOPE": 5,
    "THETAP": 6,
    "PHIP": 7,
    "SEED1": 8,
    "SEED2": 9,
    "SEED3": 10,
    "SEED4": 11,
    "TELFIL": 34,
    "OBSLEV": 35,
    "CSCAT": 36,
    "CERSIZ": 38,
    "TELESCOPE": 40
}

def makeInput(*args):
    """
    Generates the input for a single corsika run
    
    Parameters:
         *args -- lists of line number and replacement string for the input template
             i.e. [ [line1, replacementString1], [line2,replacementString2], ... ]
             If Null, returns the input template
        
    Returns:
        inp -- string with contents of corsika input file
        
    """
    # set input to template
    inp = inptemp
    
    # check *args not null
    if (args):
        lines = inp.splitlines()
        for arg in args:
            lines[arg[0]] = arg[1]
        inp = "\n".join(lines)
    return inp

def writeInput(filename, contents):
    """
    Writes contents into a file.

    Parameters:
        filename -- name of the file to write to
        contents -- string to write into the file
        
    
    """
    file = open("{}".format(filename), "w")
    file.write(contents)
    file.close()

def genRuns(index, controller):
    """
    Writes corsika input files.

    Parameters:
        index -- index of the first corsika input file generated
        controller -- list of corsika input keywords to adjust 
                    see example in the 'input controller' notebook cell
        
    
    """ 
    # check there is no invalid keyword (has a definition in the dictionary)
    for item in controller:
        if (item[0] not in keyword):
            e ='{} is not valid keyword. Update keyword dictionary or change controller.'.format(item[0])
            return e
    
        # check lists of each argument is the same size for each individual keyword
        size = len(item[1])
        for i in range(1,len(item)):
            if (size != len(item[i]) ):
                e='Mismatch in number of values for arguments in keyword {}. Fix controller.'.format(item[0])
                return e
    
    # check lists of each argument is the same size among all keywords (do not include nested keywords), 
    nVals = len(controller[-1][-1]) 
    if (nVals == 0):
        e = '0 arguments found in controller.'
        return e
    
    for item in controller:
        if (len(item[-1]) != nVals):       
            e = 'Mismatch in number of values among keywords. Fix controller.'
            return e
    
    # write input files
    for i in range(0, nVals):
        contents = []
        for item in controller:
            nArgs = len(item)
            replacementString = item[0]
            if('SEED' in replacementString):
                replacementString = 'SEED'
            for j in range(1,nArgs):
                replacementString += ' '
                replacementString += item[j][i]

            line = keyword[item[0]]
            contents.append([line,replacementString])
        
        # increment TELFIL name
        contents.append([keyword["TELFIL"],'TELFIL ./DATbatch{}.telescope'.format(index)])
        inp = makeInput(*contents)
        filename = 'batch{}.inp'.format(index)
        writeInput(filename, inp)
        index += 1
        
    return 'Created {} input files'.format(nVals)

if __name__ == '__main__':
    nFiles=1000 #number of input files
    nShow=100 #number of showers per run - must match NSHOW in the template

    seed1=['{}'.format(np.random.randint(0,9999)) for i in range(nFiles)]
    seed2=['{}'.format(np.random.randint(0,9999)) for i in range(nFiles)]
    seed3=['{}'.format(np.random.randint(0,9999)) for i in range(nFiles)]
    seed4=['{}'.format(np.random.randint(0,9999)) for i in range(nFiles)]

    controller = [
        ['EVTNR',[str(x) for x in range(1,(nFiles*nShow)+1,nShow)]],
        ['SEED1',seed1,[str(0) for x in range(nFiles)],[str(0) for x in range(nFiles)]],
        ['SEED2',seed2,[str(0) for x in range(nFiles)],[str(0) for x in range(nFiles)]],
        ['SEED3',seed3,[str(0) for x in range(nFiles)],[str(0) for x in range(nFiles)]],
        ['SEED4',seed4,[str(0) for x in range(nFiles)],[str(0) for x in range(nFiles)]]
    ]

    # parse agruments
    parser = argparse.ArgumentParser(description='Creates {} CORSIKA input files'.format(nFiles*nShow))
    parser.add_argument('-p', '--particle', choices=['gamma','proton','iron'], type=str, help='primary particle')
    parser.add_argument('-e', '--energy-range', type=str, help='range of energies to simulate')
    parser.add_argument('-m', '--energy-slope', type=str, help='spectral slope to simulate')
    parser.add_argument('-z', '--zenith-range', type=str, help='range of allowable zenith angles')
    parser.add_argument('-s', '--scattering-range', type=str, help='range of allowable shower core positions')
    args = parser.parse_args()

    # update controller as necessary (if argument is not supplied, program defaults to value in template)
    if args.particle:
        if args.particle=='gamma':
            code=str(1)
        elif args.particle=='proton':
            code=str(14)
        # Fe-56 (most abundant isotope)
        elif args.particle=='iron':
            code=str(5626)
        controller.append(
            ['PRMPAR',[code for i in range(nFiles)]]
        )
    if args.energy_range:
        arg1 = args.energy_range.split()[0]
        arg2 = args.energy_range.split()[1]
        controller.append(
            ['ERANGE',[arg1 for i in range(nFiles)],[arg2 for i in range(nFiles)]]
        )
    if args.energy_slope:
        controller.append(
            ['ESLOPE',[args.energy_slope for i in range(nFiles)]]
        )
    if args.zenith_range:
        arg1 = args.zenith_range.split()[0]
        arg2 = args.zenith_range.split()[1]
        controller.append(
            ['THETAP',[arg1 for i in range(nFiles)],[arg2 for i in range(nFiles)]]
        )
    if args.scattering_range:
        arg1 = args.scattering_range.split()[0]
        arg2 = args.scattering_range.split()[1]
        controller.append(
            ['CSCAT',[str(1) for i in range(nFiles)],[arg1 for i in range(nFiles)],[arg2 for i in range(nFiles)]]
        )

    # run in terminal like: 
    # python corsikaBatchGenerator.py [args]
    print(genRuns(1, controller))
