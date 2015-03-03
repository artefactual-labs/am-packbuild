# am-packbuild
Archivematica package building scripts

Usage example:

For snapshot package:

    ./packbuild.py -r am -v 1.3.1 -c dev/issue-7239-contentdm-metadata-dip -p archivematica/daily -k 7F0699A0


For release package (include -b flag):

    ./packbuild.py -r ss -v 0.6.1 -c stable/0.6.x -p archivematica/packbuild-test -k 7F0699A0 -b 1