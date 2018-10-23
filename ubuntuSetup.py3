#!/usr/bin/env python3
import argparse
import yaml
import os, sys, subprocess


def _run_scalar_cmds(commandString):
    commands = commandString.split("\n")
    for command in commands:
        print("$ {}".format(command))
        output = subprocess.check_output(['bash', '-c', command])
        print(output)


def _print_step(cmd):
    print("    **** " + cmd)

def setup_software_linux(softwareDict):
    '''
    Given a list of software to install, set up the environment
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
                The command to prepend in front of all extensions
    - extensions (list)
                Each argument to pass to the extensions_tool
    '''
    # Check that we're being run as sudo (Return early)
    numErrors = 0
    if os.geteuid() != 0:
        print("This script must be run as sudo")
        numErrors += 1
        return numErrors
    else:
        sudoUID = os.getenv('SUDO_UID')
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
                _run_scalar_cmds(linuxDict['ppa_setup'])
                retcode = subprocess.call(['bash', '-c', 'apt-get update'])
        else:
            continue

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
                _run_scalar_cmds(linuxDict['fetch'])
            if 'pre_install' in linuxDict:
                _print_step('pre_install defined commands')
                _run_scalar_cmds(linuxDict['pre_install'])
            if 'apt_install' in linuxDict:
                for pkg in linuxDict['apt_install']:
                    print(subprocess.check_output(['bash', '-c', 'apt-get install', pkg]))
            if 'install' in linuxDict:
                _print_step('install defined commands')
                _run_scalar_cmds(linuxDict['install'])
            if 'post_install' in linuxDict:
                _print_step('post_install defined commands')
                _run_scalar_cmds(linuxDict['post_install'])
        
    print("====================================================================")
    return numErrors

def setup_software_windows(softwareDict):
    print("Windows config not yet supported")
    return 1

def setup_software(softwareDict):
    '''
    Detect if Windows or Linux and execute the correct sub-function
    '''
    if 'posix' == os.name:
        print('Posix system detected, assuming Ubuntu OS')
        return setup_software_linux(softwareDict)
        
    elif 'nt' == os.name:
        print('nt system detected, assuming Windows 10')
        return setup_software_windows(softwareDict)
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
    parser.add_argument('-f', '--software-file', help='Provide path to the software-file')

    args = parser.parse_args()
    userVars = vars(args)

    # Parse the software file
    softwaredict = parse_software_file(userVars['software_file'])
    if len(softwaredict) == 0:
        print('Could not execute any tasks defined in: {}'.format(
                                        userVars['software_file']))
        numErrors += 1

    # Pass things into the "do work" function if checks pass
    if 0 == numErrors:
        setup_software(softwaredict)

    return numErrors


if __name__ == "__main__":
    returncode = _entrypoint()
    if returncode != 0:
        exit(returncode)