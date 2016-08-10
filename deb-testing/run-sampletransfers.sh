#!/bin/bash
STORAGEDB=/var/archivematica/storage-service/storage.db
AMTMP=$(echo 'SELECT `key` FROM tastypie_apikey;' | mysql MCP)
AMKEY=$(echo $AMTMP | awk '{print $2}')
SSUSER=$(sqlite3 $STORAGEDB "select username from auth_user limit 1;")
SSKEY=$(sqlite3 $STORAGEDB "select  \`key\` FROM tastypie_apikey;")
SOURCEUUID=$(sqlite3 $STORAGEDB "select uuid from locations_location where purpose=\"TS\";")


TRANSFERSDB=/usr/lib/archivematica/automation-tools/transfers/transfers.db
WAIT=60
LAST=$(sqlite3 $TRANSFERSDB "select path from unit where current=1")
COUNT=0
while true
        do
        /usr/share/python/automation-tools/bin/python \
     -m transfers.transfer \
     --user test \
      --api-key ${AMKEY}  --ss-user $SSUSER --ss-api-key $SSKEY \
   --transfer-source $SOURCEUUID \
    --transfer-path /home/archivematica-sampledata/TestTransfers/

        CURRENT=$(sqlite3 $TRANSFERSDB "select path from unit where current=1")
        if [ x"$LAST" = x"$CURRENT" ]
                then
                COUNT=$(($COUNT + 1 ))
                echo $COUNT
                else
		echo $(date) Finished $LAST
		echo $(date) Started $CURRENT
                LAST=$CURRENT
                fi
         if [ "$COUNT" -gt "10" ]
         then
                echo $(date) "Failing transfer $CURRENT"
                ID=$(sqlite3 $TRANSFERSDB "select id from unit where current=1;")
                sqlite3 $TRANSFERSDB "update unit set current=0,status=\"FAILED\" where id=$ID;"
        COUNT=0
fi
                sleep $WAIT
        done

