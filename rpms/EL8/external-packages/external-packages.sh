# This scripts downloads packages from external repositories.
# The SHA256SUM needs to be checked *before* packages are signed with our key
# Requires EPEL repo installed


# RPM fusion repo

wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/f/ffmpeg-4.2.9-1.el8.x86_64.rpm 
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/f/ffmpeg-libs-4.2.9-1.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/o/opencore-amr-0.1.5-7.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/x/xvidcore-1.3.7-1.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/v/vo-amrwbenc-0.1.3-8.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/x/x264-libs-0.157-12.20190717git34c06d1.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/x/x264-0.157-12.20190717git34c06d1.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/x/x265-libs-3.1.2-1.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/x/x265-3.1.2-1.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/g/gpac-libs-0.8.0-2.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/f/faad2-libs-2.8.8-6.el8.x86_64.rpm
wget https://download1.rpmfusion.org/free/el/updates/8/x86_64/l/libavdevice-4.2.9-1.el8.x86_64.rpm

# CERT Forensics repo

wget https://forensics.cert.org/repository/centos/cert/8/x86_64/bulk_extractor-2.0.3-1.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/libewf-20160718-20140806.4.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/libbfio-20221025-1.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/libpst-0.6.72-4.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/libpst-libs-0.6.72-4.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/libvhdi-20221124-1.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/libvmdk-20221124-1.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/sleuthkit-4.12.1-100.el8.x86_64.rpm
wget https://forensics.cert.org/repository/centos/cert/8/x86_64/sleuthkit-libs-4.12.1-100.el8.x86_64.rpm
