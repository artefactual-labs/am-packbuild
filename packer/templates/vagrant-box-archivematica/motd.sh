#!/usr/bin/env bash

cat << EOF > /etc/motd
            ,,,,,,,,,,,,,,,
         ,,,,,,,,,,,,,,,,,,,,,
      ,,,,,,,,,,,,,,,,,,,,,,,,,,,
     ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
   ,,,,,,,,,,,,,           ,,,,,,,,,
  ,,,,,,,,,,,      ,,,       ,,,,,,,,
 ,,,,,,,,,,   ,,,,,,,,,,,     ,,,,,,,,
 ,,,,,,,,    ,,,,,,,,,,,,,    ,,,,,,,,
,,,,,,,,     ,,,,,,,,,,,,,     ,,,,,,,,
,,,,,,,,    ,,,,,,,,,,,,,,,    ,,,,,,,,
,,,,,,,,    ,,,,,,,,,,,,,,,    ,,,,,,,,
,,,,,,,,,   ,,,,,,,,,,,         ,,,,,,,,
,,,,,,,,,,,,,,,,,,       ,,,    ,,,,,,,,
,,,,,,,,,,,,,,,      ,,,,,,,    ,,,,,,,
,,,,,,,,,,,,     ,,,,,,,,,,,     ,,,,,,
,,,,,,,,,,,    ,,,,,,,,,,,,,,    ,,,,,,
 ,,,,,,,,,    ,,,,,,,,,,,,,,     ,,,,,
 ,,,,,,,,     ,,,,,,,,,,,,,       ,,,,
  ,,,,,,,     ,,,,,,,,,,,   ,,
   ,,,,,,,      ,,,,,,     ,,,,
     ,,,,,,             ,,,,,,,,,,
      ,,,,,,,        ,,,,,,,,,,,,
         ,,,,,,,,,,,,,,,,,,,,,        Archivematica
            ,,,,,,,,,,,,,,,
                  ,,,                 - Web: https://www.archivematica.org
                                      - Dashboard: http://10.10.10.20
                                      - Storage Service: http://10.10.10.20:8000

                                        Username: admin
                                        Password: archivematica

--------------------------------------------------------------------------------
EOF