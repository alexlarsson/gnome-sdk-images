srcdir = $(CURDIR)
builddir = $(CURDIR)

yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz yocto-build/x86_64/images/gnomeos-contents-platform-x86_64.tar.gz images:
	if test ! -d gnome-continuous-yocto; then \
		git clone https://github.com/alexlarsson/gnome-continuous-yocto.git --branch gnomeostree-3.14-dizzy-platform;\
	fi
	(cd  gnome-continuous-yocto; git pull;)
	(cd  gnome-continuous-yocto; git submodule update --init;)
	mkdir -p yocto-build/x86_64
	./gnome-sdk-build-yocto ${srcdir}/gnome-continuous-yocto ${builddir}/yocto-build/ x86_64

NULL=

PACKAGES = \
	gnome-sdk-base \
	gtk-doc-stub \
	glib2 \
	gnome-common \
	gobject-introspection \
	shared-mime-info \
	pixman \
	freetype \
	fontconfig \
	xorg-x11-util-macros \
	xorg-x11-proto-devel \
	libXau xcb-proto libxcb libXdmcp xorg-x11-xtrans-devel libX11 libXrender \
	libXfixes libXext libXft libXi libXinerama libICE libSM libXpm libXrandr libXtst \
	libXv libXvMC libXxf86vm libXdamage libXcursor libXcomposite libxkbfile libxshmfence \
	dbus cairo dbus-glib \
	graphite2 harfbuzz libdatrie libthai pango atk at-spi2-core at-spi2-atk gdk-pixbuf2 gtk3 \
	itstool yelp-xsl yelp-tools \
	hicolor-icon-theme libcroco vala librsvg2 adwaita-icon-theme \
	gnome-sdk gnome-platform dejavu-fonts \
	$(NULL)

SPECS =$(PACKAGES:%=packages/SPECS/%.spec)

deps: rpm-dependencies.P

rpm-dependencies.P: $(SPECS) makedeps.sh yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./setup.sh root-sdk var-sdk yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./build.sh root-sdk var-sdk packages ./makedeps.sh $(SPECS) > rpm-dependencies.P

gnome-sdk-rpmdb.tar.xz gnome-sdk.tar.xz: packages/RPMS/noarch/gnome-sdk-0.1-1.noarch.rpm
	./setup.sh root-sdk var-sdk yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./build.sh root-sdk var-sdk packages smart install -y  packages/RPMS/noarch/gnome-sdk-0.1-1.noarch.rpm
	rm -rf gnome-sdk.tar.xz
	tar --transform 's,^root-sdk/usr/,,S' -cJvf gnome-sdk.tar.xz root-sdk/usr --owner=root
	tar --transform 's,^var-sdk/,,S' -cJvf gnome-sdk-rpmdb.tar.xz var-sdk/lib/rpm --owner=root

gnome-platform-base: packages/RPMS/x86_64/gnome-platform-base-0.1-1.x86_64.rpm

packages/RPMS/x86_64/gnome-platform-base-0.1-1.x86_64.rpm: packages/SPECS/gnome-platform-base.spec  setup.sh build.sh yocto-build/x86_64/images/gnomeos-contents-platform-x86_64.tar.gz
	echo building packages/SPECS/gnome-platform-base.spec
	cp yocto-build/x86_64/images/gnomeos-contents-platform-x86_64.tar.gz packages/SOURCES/
	./setup.sh root-sdk var-sdk yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./build.sh root-sdk var-sdk packages rpmbuild -ba packages/SPECS/gnome-platform-base.spec

gnome-sdk-base: packages/RPMS/x86_64/gnome-sdk-base-0.1-1.x86_64.rpm

gnome-platform.tar.xz: packages/RPMS/x86_64/gnome-platform-base-0.1-1.x86_64.rpm packages/RPMS/noarch/gnome-platform-0.1-1.noarch.rpm setup.sh build.sh
	echo building gnome-platform
	rm -rf packages/gnome-platform
	mkdir -p packages/gnome-platform/var/lib/rpm
	./setup.sh root-sdk var-sdk yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./build.sh root-sdk var-sdk packages ./install_rpms.sh gnome-platform
	./build.sh packages/gnome-platform packages/gnome-platform/var packages /bin/sh /self/gnome-platform/post_install.sh
	tar --transform 's,^packages/gnome-platform/usr/,,S' -cJvf gnome-platform.tar.xz packages/gnome-platform/usr --owner=root

-include rpm-dependencies.P
