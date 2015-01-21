#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  packbuild.py
#  


def main():

    import argparse
    import os
    import time
    import logging
    import subprocess
    import shlex

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    PROCESS_DIR = "/tmp/ampackbuilder"


    parser = argparse.ArgumentParser()

    #-ver CURRENT_VERSION -br BRANCH
    parser.add_argument("-r", "--repository", help="repository (am or ss)", required=True, choices=['am','ss'])
    parser.add_argument("-v", "--version", help="current version", required=True)
    parser.add_argument("-b", "--branch", help="branch", required=True)

    args = parser.parse_args()

    """
    print( "Name {} Version {} Branch {} ".format(
    args.name,
    args.version,
    args.branch,
    ))
    """
        

    # create package version string
    
    utctime=time.strftime("%Y%m%d%H%M%S", time.gmtime())
    
    package_string = args.repository+"_"+args.version \
                        +"+1SNAPSHOT"+utctime+"_"+args.branch 
    logging.info ("package_string= %s", package_string)


    # create directory for the build
    build_path = os.path.join (PROCESS_DIR, package_string)
    logging.info("Creating directory: %s", build_path)
    os.makedirs(build_path)

    # clone corresponding git repo
    if args.repository == "ss":
        logging.info("Cloning git repo for Storage Service")

        command_string = 'git clone https://github.com/artefactual/archivematica-storage-service.git'
        logging.info("calling subprocess for: %s", command_string)
        p = subprocess.Popen(shlex.split(command_string), cwd=build_path )
        p.wait()

        command_string = 'git checkout -t '+args.branch
        logging.info("calling subprocess for: %s", command_string)
        p = subprocess.Popen(shlex.split(command_string), cwd=build_path )
        p.wait()

    return 0

if __name__ == '__main__':
    main()

