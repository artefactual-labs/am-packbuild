FROM rockylinux:9

# Install build dependencies.
RUN \
	yum -y install epel-release dnf-plugins-core && \
	yum config-manager --set-enabled crb && \
	yum -y install \
	rpm-build \
	make \
	git \
	patchelf \
	gcc \
	gcc-c++ \
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

# Build modern libewf from source.
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
