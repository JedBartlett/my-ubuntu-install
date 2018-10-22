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

def setup_software(softwareDict, sudoUID, homeDir):
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
    print("====================================================================")
    print("=======    Setting up all software per file description      =======")
    print("====================================================================")
    for software in softwareDict:
        if 'ppa_setup' in softwareDict[software]:
            _print_step("ppa is required for {}".format(software))
            _run_scalar_cmds(softwareDict[software]['ppa_setup'])
            retcode = subprocess.call(['bash', '-c', 'apt-get update'])

    for software in softwareDict:
        print("----------------------------------------------------------------")
        print("-------    {}".format(software))
        print("----------------------------------------------------------------")
        isInstalled = False
        if 'check_install' in softwareDict[software]:
            print("Running {} to check install".format(softwareDict[software]['check_install']))
            try:
                retcode = subprocess.call(['bash', '-c', softwareDict[software]['check_install']])
                if 0 == retcode:
                    isInstalled = True
                    _print_step("Software already installed")
            except:
                print('Could not run {}'.format(softwareDict[software]['check_install']))
        if not isInstalled:
            if 'fetch' in softwareDict[software]:
                _print_step('fetch defined commands')
                _run_scalar_cmds(softwareDict[software]['fetch'])
            if 'pre_install' in softwareDict[software]:
                _print_step('pre_install defined commands')
                _run_scalar_cmds(softwareDict[software]['pre_install'])
            if 'apt_install' in softwareDict[software]:
                for pkg in softwareDict[software]['apt_install']:
                    print(subprocess.check_output(['bash', '-c', 'apt-get install', pkg]))
            if 'install' in softwareDict[software]:
                _print_step('install defined commands')
                _run_scalar_cmds(softwareDict[software]['install'])
            if 'post_install' in softwareDict[software]:
                _print_step('post_install defined commands')
                _run_scalar_cmds(softwareDict[software]['post_install'])
        
    print("====================================================================")


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
    parser = argparse.ArgumentParser(description='Setup Ubuntu dev environment')
    parser.add_argument('-f', '--software-file', help='Provide path to the software-file')

    args = parser.parse_args()
    userVars = vars(args)

    # Check that we're being run as sudo
    numErrors = 0
    if os.geteuid() != 0:
        print("This script must be run as sudo")
        numErrors += 1
    else:
        sudoUID = os.getenv('SUDO_UID')
        homeDir = os.getenv('HOME')
        if ( sudoUID is None or 0 == sudoUID or homeDir is None or "root" in homeDir):
            print("This script must be run as sudo, not as root")
            print("Need the HOME variable to be set to configure software")
            numErrors += 1

    # Parse the software file
    softwaredict = parse_software_file(userVars['software_file'])
    if len(softwaredict) == 0:
        print('Could not execute any tasks defined in: {}'.format(
                                        userVars['software_file']))
        numErrors += 1

    # Pass things into the "do work" function if checks pass
    if 0 == numErrors:
        setup_software(softwaredict, sudoUID, homeDir)

    return numErrors


if __name__ == "__main__":
    returncode = _entrypoint()
    if returncode != 0:
        exit(returncode)