FROM centos:7


RUN yum -y install rpm-build make git epel-release

# Install node repo and build depends, to speed up the build process
RUN rpm -Uvh https://rpm.nodesource.com/pub_8.x/el/7/x86_64/nodesource-release-el7-1.noarch.rpm
RUN yum install -y git gcc openldap-devel openssl-devel python-virtualenv python-pip mariadb-devel libxslt-devel python-devel libffi-devel openssl-devel gcc-c++ postgresql-devel nodejs

