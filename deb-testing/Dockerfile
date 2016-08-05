FROM ubuntu:trusty

#RUN echo 'Acquire::http::proxy "http://192.168.0.11:3142";' > /etc/apt/apt.conf.d/30proxy

RUN apt-get update

#Some needed dependencis
RUN apt-get install -y apt-transport-https python-pip wget git \
                       software-properties-common python-software-properties

# Install repositories for am and elasticsearch
RUN add-apt-repository ppa:archivematica/externals && \
    apt-add-repository multiverse && \
    wget -qO - https://packages.archivematica.org/1.5.x/key.asc |  apt-key add - && \
    wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch |  apt-key add - && \
    echo 'deb http://packages.elasticsearch.org/elasticsearch/1.7/debian stable main' >> /etc/apt/sources.list.d/elasticsearch-1.7.list && \
    echo 'deb [arch=amd64] https://packages.archivematica.org/1.5.x/ubuntu-candidate trusty main' >> /etc/apt/sources.list.d/archivematica-candidate.list 

# Install archviematica-storage-service
RUN apt-get update

RUN     apt-get install -y archivematica-storage-service && \
        rm -f /etc/nginx/sites-enabled/default && \
        ln -sf /etc/nginx/sites-available/storage /etc/nginx/sites-enabled/storage && \
        ln -sf /etc/uwsgi/apps-available/storage.ini /etc/uwsgi/apps-enabled/storage.ini 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server-5.5
RUN service mysql start && DEBIAN_FRONTEND=noninteractive apt-get install -y archivematica-mcp-server && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y archivematica-mcp-client
RUN apt-get install -y archivematica-dashboard
RUN apt-get install -y elasticsearch
RUN apt-get install -y supervisor

RUN rm -f /etc/apache2/sites-enabled/*default* && \
 wget -q https://raw.githubusercontent.com/artefactual/archivematica/stable/1.4.x/localDevSetup/apache/apache.default -O /etc/apache2/sites-available/default.conf && \
 ln -s /etc/apache2/sites-available/default.conf /etc/apache2/sites-enabled/default.conf 
RUN /usr/bin/freshclam

#RUN apt-get install -y git python-virtualenv && \
#	git clone https://github.com/artefactual/automation-tools /usr/lib/archivematica/automation-tools && \
#        virtualenv /usr/share/python/automation-tools && \
#	cd /usr/lib/archivematica/automation-tools/ && \
#        /usr/share/python/automation-tools/bin/pip install -r requirements.txt && \
#	mkdir -p /var/log/archivematica/automation-tools && \
#	mkdir -p /var/archivematica/automation-tools && \
#	chown archivematica.archivematica /var/log/archivematica/automation-tools /var/archivematica/automation-tools

	
RUN git clone https://github.com/artefactual/archivematica-sampledata /home/archivematica-sampledata
 
	
ADD supervisord/* /etc/supervisor/conf.d/
ADD run.sh /
RUN chmod 755 /run.sh
RUN apt-get install -y git python-virtualenv && \
	git clone https://github.com/artefactual/automation-tools /usr/lib/archivematica/automation-tools 
RUN        virtualenv /usr/share/python/automation-tools 
RUN /bin/bash -c "cd /usr/lib/archivematica/automation-tools/ && \
	source /usr/share/python/automation-tools/bin/activate && \
        pip install -r requirements.txt "


#ENTRYPOINT "/run.sh"
