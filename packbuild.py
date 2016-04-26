#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  packbuild.py
#  

import argparse
import os
import time
import logging
import subprocess 
import shlex
import re
import sys
import shutil
import glob

def run_subprocess(command_string, cwd=None): 
    logging.info("Running: %s", command_string)
    logging.info("    cwd: %s", cwd)
    subprocess.check_call(shlex.split(command_string), cwd=cwd)
    return

def run_subprocess_co(command_string, cwd=None): 
    logging.info("Running: %s", command_string)
    logging.info("    cwd: %s", cwd)
    output = subprocess.check_output(shlex.split(command_string), cwd=cwd)
    return output


def main():

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    PROCESS_DIR = "/tmp/ampackbuilder"

    parser = argparse.ArgumentParser()

    #-ver CURRENT_VERSION -br BRANCH
    parser.add_argument("-r", "--repository", help="repository (am or ss)", required=True, choices=['am','ss'])
    parser.add_argument("-v", "--version", help="current version", required=True)
    parser.add_argument("-c", "--checkout", help="branch/commit/tag to checkout", required=True)
    parser.add_argument("-p", "--ppa", help="ppa to upload", required=False)
    parser.add_argument("-k", "--key", help="key for package signing", required=True)
    parser.add_argument("-b", "--build", help="build number. If this option is present, will build a release package")

    args = parser.parse_args()
    
    # create package version string

    build_time = time.gmtime() 

    utctime=time.strftime("%Y%m%d%H%M%S", build_time)
    checkout_alphanum= re.sub(r'[^a-zA-Z0-9]','', args.checkout)

    # create directory for the build
    dir_string = args.repository+"-"+args.version \
                        +"-"+utctime+"-"+checkout_alphanum 
    working_dir = os.path.join (PROCESS_DIR, dir_string)
    logging.info("Creating directory: %s", working_dir)

    os.makedirs(working_dir)

    if args.repository == "am":
        try:        
            #git clone 
            command_string = 'git clone https://github.com/artefactual/archivematica.git'
            run_subprocess(command_string, cwd=working_dir)

            #git checkout
            repo_dir = os.path.join(working_dir,"archivematica")
            command_string = 'git checkout '+args.checkout
            run_subprocess(command_string, cwd=repo_dir)

            #git submodule init
            command_string = 'git submodule init'
            run_subprocess(command_string, cwd=repo_dir)

            #git submodule update
            command_string = 'git submodule update'
            run_subprocess(command_string, cwd=repo_dir)

            #check the latest commit
            command_string = 'git rev-parse HEAD'
            commit_hash = run_subprocess_co(command_string, cwd=repo_dir)
            # need to convert output from byte to string
            commit_hash_str = commit_hash.decode("utf-8").strip()

            # package version string
            if args.build:
                package_ver_string = "1:{0}-{1}".format(args.version, args.build)
                package_ver_string_noepoch = "{0}-{1}".format(args.version, args.build)
            else:
                package_ver_string = "1:{0}+1SNAPSHOT{1}-{2}-{3}".format(args.version, utctime, commit_hash_str[:6], checkout_alphanum)
                package_ver_string_noepoch = "{0}+1SNAPSHOT{1}-{2}-{3}".format(args.version, utctime, commit_hash_str[:6], checkout_alphanum)

            logging.info("package version: %s", package_ver_string)

            # dict: package_name -> directory
            packagedir_dic = { "archivematica-common":"archivematicaCommon",
                               "archivematica-dashboard":"dashboard",  
                               "archivematica-mcp-client":"MCPClient",
                               "archivematica-mcp-server":"MCPServer",                               
                             }
 

            # dict: distribution -> numeric version
            distronum_dic = { "precise":"12.04",
                              "trusty":"14.04",
                              "xenial":"16.04"
                            }


            # lines for the changelog
            
            chglog_maintainer = "Artefactual Systems <sysadmin@artefactual.com>"
            chglog_package_name = "archivematica-common"
            chglog_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", build_time)
            line = ["","","","","",""]
            line[2] = "  * commit: {0}".format(commit_hash_str)
            line[3] = "  * checkout: {0}".format(args.checkout)
            line[5] = " -- {0}  {1}".format(chglog_maintainer, chglog_time)

            # Iterate on distros
            for d in distronum_dic:
                # Iterate on packages
                for p in packagedir_dic:
                    line[0] = "{0} ({1}~{2}) {3}; urgency=high".format(p, package_ver_string, distronum_dic[d], d)
                    for l in line:
                        print(l)
                    print()

                    # write debian changelog file
                    package_dir = os.path.join(repo_dir, "src", packagedir_dic[p])
                    chglog_file = os.path.join(package_dir, "debian","changelog" )
                    logging.info("writing debian changelog in %s", chglog_file)

                    f = open(chglog_file, 'r')
                    temp = f.read()
                    f.close()

                    f = open(chglog_file, 'w')
                    for l in line:
                        f.write(l+'\n')
                    f.write(temp)
                    f.close()

                    # debuild
                    command_string = 'debuild --no-tgz-check -S -k{0} -I'.format(args.key)
                    run_subprocess(command_string, cwd=package_dir)

                    # dput
                    if args.ppa:
                        dput_dir = os.path.join(repo_dir, "src")
                        dput_filename = "{0}_{1}~{2}_source.changes".format(p, package_ver_string_noepoch, distronum_dic[d])
                        command_string = 'dput ppa:{0} {1}'.format(args.ppa, dput_filename)
                        run_subprocess(command_string, cwd=dput_dir)
                    else:
                        command_string = 'debuild --no-tgz-check -b -k{0} -I'.format(args.key)
                        run_subprocess(command_string, cwd=package_dir)




        except subprocess.CalledProcessError as e:
            logging.error("Subprocess returned code %d", e.returncode)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    elif args.repository == "ss":
        try:        
            #git clone 
            command_string = 'git clone git@git.artefactual.com:archivematica-storage-service.git'
            run_subprocess(command_string, cwd=working_dir)

            #git checkout
            repo_dir = os.path.join(working_dir,"archivematica-storage-service")
            command_string = 'git checkout '+args.checkout
            run_subprocess(command_string, cwd=repo_dir)

            #git submodule init
            command_string = 'git submodule init'
            run_subprocess(command_string, cwd=repo_dir)

            #git submodule update
            command_string = 'git submodule update'
            run_subprocess(command_string, cwd=repo_dir)


            #install pip requirements workaround
            #currently launchpad gives package builder errors when using pip to download libraries
            #currently workaround is just to copy the .tar.gz files from a previous install

            # pip_reqs = [
            #             "Django==1.5.4",
            #             "django-braces==1.0.0",
            #             "django-model-utils==1.3.1",
            #             "logutils==0.3.3",
            #             "South==0.8.4",
            #             "django-tastypie==0.9.15",
            #             "django-extensions==1.1.1",
            #             "lxml==3.2.3",
            #             "django-jsonfield==0.9.12",
            #             "bagit==1.3.7",
            #             "django-annoying==0.7.7",
            #             "requests>=2.3.0",
            #             "httplib2",
            #             "argparse",
            #             "dateutils",
            #             "mimeparse",
            #             "python-dateutil",
            #             "pytz",
            #             "six",
            #             ]                        
            # for req in pip_reqs:
            #     command_string = 'pip install \'{0}\' -d lib'.format(req)
            #     run_subprocess(command_string, cwd=repo_dir)

            logging.info("Copying files to lib")
            #requires pip >= 8
            command_string = "pip download -d lib --no-binary all -r requirements.txt"
            run_subprocess(command_string, cwd=repo_dir)

            #check the latest commit
            command_string = 'git rev-parse HEAD'
            commit_hash = run_subprocess_co(command_string, cwd=repo_dir)
            # need to convert output from byte to string
            commit_hash_str = commit_hash.decode("utf-8").strip()

            # package version string
            if args.build:
                package_ver_string = "1:{0}-{1}".format(args.version, args.build)
                package_ver_string_noepoch = "{0}-{1}".format(args.version, args.build)
            else:
                package_ver_string = "1:{0}+1SNAPSHOT{1}-{2}-{3}".format(args.version, utctime, commit_hash_str[:6], checkout_alphanum)
                package_ver_string_noepoch = "{0}+1SNAPSHOT{1}-{2}-{3}".format(args.version, utctime, commit_hash_str[:6], checkout_alphanum)


            logging.info("package version: %s", package_ver_string)
 

            # dict: distribution -> numeric version
            distronum_dic = { "precise":"12.04",
                              "trusty":"14.04",
                              "xenial":"16.04"
                            }

            # lines for the changelog
            
            chglog_maintainer = "Artefactual Systems <sysadmin@artefactual.com>"
            chglog_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", build_time)
            line = ["","","","","",""]
            line[2] = "  * commit: {0}".format(commit_hash_str)
            line[3] = "  * checkout: {0}".format(args.checkout)
            line[5] = " -- {0}  {1}".format(chglog_maintainer, chglog_time)

            # Iterate on distros
            for d in distronum_dic:
                p = "archivematica-storage-service"
                line[0] = "{0} ({1}~{2}) {3}; urgency=high".format(p, package_ver_string, distronum_dic[d], d)
                for l in line:
                    print(l)
                print()

                # write debian changelog file
                chglog_file = os.path.join(repo_dir, "debian","changelog" )
                logging.info("writing debian changelog in %s", chglog_file)

                f = open(chglog_file, 'r')
                temp = f.read()
                f.close()

                f = open(chglog_file, 'w')
                for l in line:
                    f.write(l+'\n')
                f.write(temp)
                f.close()

                # debuild
                command_string = 'debuild --no-tgz-check -S -k{0} -I'.format(args.key)
                run_subprocess(command_string, cwd=repo_dir)

                # dput
                if args.ppa:
                    dput_dir = working_dir
                    dput_filename = "{0}_{1}~{2}_source.changes".format(p, package_ver_string_noepoch, distronum_dic[d])
                    command_string = 'dput ppa:{0} {1}'.format(args.ppa, dput_filename)
                    run_subprocess(command_string, cwd=dput_dir)
                else:
                    command_string = 'debuild --no-tgz-check -b -k{0} -I'.format(args.key)
                    run_subprocess(command_string, cwd=repo_dir)





        except subprocess.CalledProcessError as e:
            logging.error("Subprocess returned code %d", e.returncode)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


if __name__ == '__main__':
    main()

