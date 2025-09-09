FROM rockylinux:8

# Install build dependencies.
RUN \
	yum -y install epel-release dnf-plugins-core && \
	yum config-manager --set-enabled powertools && \
	yum -y install \
	rpm-build \
	make \
	git \
	curl \
	patchelf \
	gcc \
	gcc-c++ \
	xz \
	autoconf \
	automake \
	gettext \
	gettext-devel \
	libtool \
	pkgconfig \
	flex \
	bison \
	expat-devel \
	libgpg-error-devel \
	libgcrypt-devel \
	libpcap-devel \
	ncurses-devel \
	openssl-devel \
	sqlite-devel \
	libuuid-devel \
	zlib-devel \
	re2 \
	re2-devel \
	tre-devel \
	abseil-cpp-devel

# Install modern gettext (autopoint >= 0.21) from source for libewf build.
RUN \
    curl -L -o /tmp/gettext.tar.xz https://mirror.csclub.uwaterloo.ca/gnu/gettext/gettext-0.26.tar.xz && \
    mkdir -p /tmp/gettext && \
    tar -xf /tmp/gettext.tar.xz -C /tmp/gettext --strip-components=1 && \
    cd /tmp/gettext && \
    ./configure --prefix=/usr/local && \
    make -j"$(nproc)" && \
    make install

# Build modern libewf from source for bulk_extractor build.
RUN \
    git clone --depth 1 https://github.com/libyal/libewf.git /tmp/libewf && \
    cd /tmp/libewf && \
    ./synclibs.sh && \
    sed -i 's/AC_PREREQ(\[2\.71\])/AC_PREREQ([2.69])/' configure.ac && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local --disable-wide-character-type --disable-python --disable-nls && \
    make -j"$(nproc)" && \
    make install && \
    /sbin/ldconfig
