FROM centos:7

# Environmnet variables needed during build
ENV GRADLE_VERSION 2.12

# Environment variables needed during runtime
ENV GRADLE_HOME /opt/gradle/latest 
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$GRADLE_HOME/bin

RUN yum -y install rpm-build make git java-1.8.0-openjdk-devel wget

RUN mkdir /opt/gradle && \
    wget -N http://downloads.gradle.org/distributions/gradle-${GRADLE_VERSION}-all.zip && \
    unzip -oq ./gradle-${GRADLE_VERSION}-all.zip -d /opt/gradle && \
    ln -sfnv gradle-${GRADLE_VERSION} /opt/gradle/latest && \
    rm ./gradle-${GRADLE_VERSION}-all.zip
