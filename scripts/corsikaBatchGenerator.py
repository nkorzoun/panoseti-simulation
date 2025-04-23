# imports
import numpy as np
import sys
import argparse

# input template 
#
# PALOMAR
#
inptemp='''RUNNR 1
EVTNR 1
NSHOW 100
PRMPAR 1
ERANGE 1E4 1E4
ESLOPE -2
THETAP 0. 20.
PHIP 0. 360.
SEED 200 0 0
SEED 202 0 0
SEED 204 0 0
SEED 206 0 0
ATMOD 1
MAGNET 25.2 40.88
ARRANG 11.03
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
HOST gamma22 
ATMOSPHERE 61 T
TELFIL ./DATbatch0.telescope
OBSLEV 1650.E2
CSCAT 1 1200.E2 1200.E2
CERFIL 0
CERSIZ 5.
CWAVLG 200. 700.
TELESCOPE 39000.7 16741.3 3466.2 25.
TELESCOPE 21709.0 22289.6 4917.2 25.
TELESCOPE 27025.4 7928.1 3970.4 25.
TELESCOPE 14130.9 -6844.7 3721.9 25.
TELESCOPE -2795.8 -26138.7 2091.7 25.
TELESCOPE 24666.4 -34052.5 4306.2 25.
TELESCOPE -14958.9 -10903.1 4281.8 25.
TELESCOPE -2823.1 -8978.7 3912.2 25.
TELESCOPE -16040.7 -32238.0 2378.4 25.
TELESCOPE -70907.4 -34125.3 2886.0 25.
TELESCOPE -37825.9 -9113.0 126.8 25.
TELESCOPE -54721.4 -37000.2 2346.6 25.
TELESCOPE -79058.9 -49391.1 559.6 25.
TELESCOPE -32192.7 14482.1 160.4 25.
TELESCOPE -27082.5 -24144.2 2610.1 25.
TELESCOPE -11190.3 2831.3 3523.5 25.
TELESCOPE 3875.0 -22893.5 2387.1 25.
TELESCOPE 18717.2 -28872.6 2786.5 25.
TELESCOPE 22595.5 -47890.9 2751.4 25.
TELESCOPE 32613.4 -17739.3 4604.2 25.
TELESCOPE 35574.1 1876.4 3485.3 25.
TELESCOPE 9318.3 22769.5 3696.6 25.
TELESCOPE 31824.1 34869.0 4522.6 25.
TELESCOPE 50459.9 30961.2 2933.0 25.
TELESCOPE 66307.4 9871.6 1599.4 25.
TELESCOPE 64395.3 68321.8 1353.3 25.
EXIT'''
#
# LICK
#
# inptemp='''RUNNR 1
# EVTNR 1
# NSHOW 100
# PRMPAR 1
# ERANGE 1E2 1E2
# ESLOPE -2.5
# THETAP 0. 0.
# PHIP 0. 360.
# SEED 200 0 0
# SEED 202 0 0
# SEED 204 0 0
# SEED 206 0 0
# ATMOD 1
# MAGNET 25.2 40.88
# ARRANG 12.77
# ELMFLG F T
# RADNKG 200.E2
# FIXCHI 0.
# HADFLG 0 0 0 0 0 2
# QGSJET T 0
# QGSSIG T
# HILOW 100.
# ECUTS 0.30 0.05 0.02 0.02
# MUADDI F
# MUMULT T
# LONGI T 20. F F
# MAXPRT 50
# PAROUT F F
# ECTMAP 1.E6
# DEBUG F 6 F 1000000
# DIRECT ./
# USER nkorzoun 
# HOST caviness
# ATMOSPHERE 61 T
# TELFIL ./DATbatch0.telescope
# OBSLEV 1239.E2
# CSCAT 1 200.E2 200.E2
# CERFIL 0
# CERSIZ 5.
# CWAVLG 200. 700.
# TELESCOPE 53.59E2 73.52E2 1E2 0.25E2
# TELESCOPE 53.59E2 -80.48E2 1E2 0.25E2
# TELESCOPE -107.18E2 6.95E2 1E2 0.25E2
# EXIT'''

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
    parser.add_argument('-a', '--azimuth-range', type=str, help='range of allowable azimuth angles')
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
    if args.azimuth_range:
	arg1 = args.azimuth_range.split()[0]
	arg2 = args.azimuth_range.split()[1]
	controller.append(
	    ['PHIP',[arg1 for i in range(nFiles)],[arg2 for i in range(nFiles)]]
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
