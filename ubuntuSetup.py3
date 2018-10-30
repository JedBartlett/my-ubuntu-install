#!/usr/bin/env python3
import argparse
import yaml
from usrsdevenv.setupSoftware import parse_software_file, setup_software

def _entrypoint():
    '''
    Parse the arguments provided on the command-line prompt
    '''
    numErrors = 0
    parser = argparse.ArgumentParser(description='Setup Ubuntu dev environment')
    parser.add_argument('-f', '--software-file', required=True,
                         help='Provide path to the software-file')
    parser.add_argument('-o', '--only-run',
                         help='Only do the work for one software found in software-file')
    parser.add_argument('-v', '--verbose', action='store_true',
                         help='Print out all the subprocess stdout / stderr')

    args = parser.parse_args()
    userVars = vars(args)

    # Parse the software file
    softwaredict = parse_software_file(userVars['software_file'])
    dictToUse = {}
    if len(softwaredict) == 0:
        print('Could not execute any tasks defined in: {}'.format(
                                        userVars['software_file']))
        numErrors += 1
    if 'only_run' in userVars and userVars['only_run']:
        onlySoftwareKey = userVars['only_run'].strip() # Remove spaces
        if onlySoftwareKey in softwaredict:
            dictToUse[onlySoftwareKey] = softwaredict[onlySoftwareKey]
        else:
            print('ERROR - Could not locate key {} in {}'.format(onlySoftwareKey,
                                                                 userVars['software_file']))
            numErrors += 1
    else:
        dictToUse = softwaredict

    # Pass things into the "do work" function if checks pass
    verbose = False
    if 'verbose' in userVars and userVars['verbose']:
        verbose = True
    if 0 == numErrors:
        setup_software(dictToUse, verbose)

    return numErrors


if __name__ == "__main__":
    returncode = _entrypoint()
    if returncode != 0:
        exit(returncode)