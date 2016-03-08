FROM centos:7



RUN yum -y install rpm-build make git epel-release

ADD ./package.spec /package.spec
RUN yum-builddep -y /package.spec
