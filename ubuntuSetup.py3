#!/usr/bin/env python3
import argparse
import yaml
import os, sys, subprocess
# From this repo, import the module that does the work
import usrsdevenv.extensionsInstallers as extInst


def _run_scalar_cmds(commandString, verbose=False):
    print("$ {}".format(commandString))
    output = subprocess.check_output(['bash', '-c', commandString],
                                     stderr=subprocess.STDOUT)
    if verbose:
        print(output)
    return output

def _print_step(cmd):
    print("    **** " + cmd)

def setup_software_linux(softwareDict, verbose):
    '''
    Given a list of software to install, set up the environment.
    Literal Block Scalars will be executed as bash commands
    NOTE - Any operation that takes a Literal Block Scalar set of commands can
           also accept a '_py' suffixed key, which will cause the lines to be executed
           within the python environment (after any command line calls).
           usersdevenv will be added to the python path before execution.
    - ppa_setup (Literal Block Scalar)
                All lines in the scalar of these are executed and apt update is
                executed to update the software list as a first pass before any
                other steps are run
    - check_install (string)
                This command should return exit 0 if the software is already
                installed. If it is, skip to after post_install step.
    - fetch (Literal Block Scalar)
                All lines in the scalar are executed
    - pre_install (Literal Block Scalar)
                All lines in the scalar are executed
    - apt_install (list)
                All apt packages listed are installed
    - install (Literal Block Scalar)
                All lines in the scalar are executed
    - post_install (Literal Block Scalar)
                All lines in the scalar are executed
    - simlink (dictionary)
         <name>:
           replace_file : <file to replace>
           use_file : <file to symlink to>
           replace_folder : <folder to replace>
           use_folder : <folder to symlink to>
    - extensions_tool (string)
                The command to prepend in front of all listed extensions.
                If not set, but extensions are listed, will check if there is
                an in-built handler for that app.
    - extensions (list)
                Each argument to pass to the extensions_tool
    '''
    import pwd
    # Check that we're being run as sudo (Return early)
    numErrors = 0
    if os.geteuid() != 0:
        print("This script must be run as sudo")
        numErrors += 1
        return numErrors
    else:
        sudoUID = os.getenv('SUDO_UID')
        sudoUserRecord = pwd.getpwuid(int(sudoUID))
        sudoUser = sudoUserRecord.pw_name
        homeDir = os.getenv('HOME')
        if ( sudoUID is None or 0 == sudoUID or homeDir is None or "root" in homeDir):
            print("This script must be run as sudo, not as root")
            print("Need the HOME variable to be set to configure software")
            numErrors += 1
            return numErrors
    print("====================================================================")
    print("=======    Setting up all software per file description      =======")
    print("====================================================================")
    for software in softwareDict:
        if 'ubuntu' in softwareDict[software]:
            # Get the linux dictionary reference inside the softwareDict
            linuxDict = softwareDict[software]['ubuntu']
            if 'ppa_setup' in linuxDict:
                _print_step("ppa is required for {}".format(software))
                _run_scalar_cmds(linuxDict['ppa_setup'], verbose)
        else:
            continue

    _print_step("Run apt-get update")
    _run_scalar_cmds('apt-get update', verbose)

    for software in softwareDict:
        print("----------------------------------------------------------------")
        print("-------    {}".format(software))
        print("----------------------------------------------------------------")
        linuxDict = {}
        if 'ubuntu' in softwareDict[software]:
            # Get the linux dictionary reference inside the softwareDict
            linuxDict = softwareDict[software]['ubuntu']
        else:
            print("No install instructions defined for ubuntu")
            continue
        isInstalled = False
        if 'check_install' in linuxDict:
            print("Running {} to check install".format(linuxDict['check_install']))
            try:
                retcode = subprocess.call(['bash', '-c', linuxDict['check_install']])
                if 0 == retcode:
                    isInstalled = True
                    _print_step("Software already installed")
            except:
                print('Could not run {}'.format(linuxDict['check_install']))
        if not isInstalled:
            if 'fetch' in linuxDict:
                _print_step('fetch defined commands')
                _run_scalar_cmds(linuxDict['fetch'], verbose)
            if 'pre_install' in linuxDict:
                _print_step('pre_install defined commands')
                _run_scalar_cmds(linuxDict['pre_install'], verbose)
            if 'apt_install' in linuxDict:
                for pkg in linuxDict['apt_install']:
                    print(subprocess.check_output(['bash', '-c', 'apt-get install', pkg]))
            if 'install' in linuxDict:
                _print_step('install defined commands')
                _run_scalar_cmds(linuxDict['install'], verbose)
            if 'post_install' in linuxDict:
                _print_step('post_install defined commands')
                _run_scalar_cmds(linuxDict['post_install'], verbose)

        if 'extensions' in softwareDict[software]:
            extensionsList = softwareDict[software]['extensions']
            _print_step('install extensions')
            if 'extensions_tool' in softwareDict[software]:
                for extension in extensionsList:
                    cmd = ['sudo', '-H', '-i', '-u', sudoUser]
                    cmd.extend(softwareDict[software]['extensions_tool'].split())
                    cmd.append(extension)
                    print('Running: "{}"'.format(cmd))
                    try:
                        output = subprocess.check_output(cmd,
                                                stderr=subprocess.STDOUT, shell=False)
                        if verbose:
                            print(output)
                    except Exception as e:
                        print(e)
                        raise Exception('Error occured trying to run extensions installer\n{}'.format(e.output))

            else: # No cli tool given
                # Try in-built extensions scripts
                extInst.extensions_installer(software, 'posix', extensionsList)

    print("====================================================================")
    return numErrors

def setup_software_windows(softwareDict, verbose):
    print("Windows config not yet supported")
    return 1

def setup_software(softwareDict, verbose):
    '''
    Detect if Windows or Linux and execute the correct sub-function
    '''
    if 'posix' == os.name:
        print('Posix system detected, assuming Ubuntu OS')
        return setup_software_linux(softwareDict, verbose)
        
    elif 'nt' == os.name:
        print('nt system detected, assuming Windows 10')
        return setup_software_windows(softwareDict, verbose)
    else:
        print('Could not identify the target system')


def parse_software_file(softwareFile):
    '''
    Open the software YAML file and return the dictionary
    '''
    softwaredict = {}
    filepath = softwareFile.strip()
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            softwaredict = yaml.safe_load(f)
    else:
        print('The file: "{}"'.format(softwareFile))
        print('Does not exist')
    return softwaredict


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