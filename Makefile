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
	./setup.sh root var yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./build.sh root var packages ./makedeps.sh $(SPECS) > rpm-dependencies.P

gnome-sdk-rpmdb.tar.xz gnome-sdk.tar.xz: packages/RPMS/noarch/gnome-sdk-0.1-1.noarch.rpm
	./setup.sh root var yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./build.sh root var packages smart install -y  packages/RPMS/noarch/gnome-sdk-0.1-1.noarch.rpm
	rm -rf gnome-sdk.tar.xz
	tar --transform 's,^root/usr/,,S' -cJf gnome-sdk.tar.xz root/usr --owner=root
	tar --transform 's,^var/,,S' -cJf gnome-sdk-rpmdb.tar.xz var/lib/rpm --owner=root

gnome-platform-base: packages/RPMS/noarch/gnome-platform-base-0.1-1.noarch.rpm

packages/RPMS/noarch/gnome-platform-base-0.1-1.noarch.rpm: packages/SPECS/gnome-platform-base.spec setup.sh build.sh yocto-build/x86_64/images/gnomeos-contents-platform-x86_64.tar.gz yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	echo building packages/SPECS/gnome-platform-base.spec
	rm -rf packages/gnome-platform
	mkdir -p packages/gnome-platform
	tar -C packages/gnome-platform -xzf yocto-build/x86_64/images/gnomeos-contents-platform-x86_64.tar.gz
	./setup.sh root var yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	./build.sh root var packages rpmbuild -ba packages/SPECS/gnome-platform-base.spec

gnome-sdk-base: packages/RPMS/noarch/gnome-sdk-base-0.1-1.noarch.rpm

gnome-platform-packages: packages/RPMS/noarch/gnome-platform-0.1-1.noarch.rpm setup.sh build.sh
	./setup.sh root var yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz
	rm -f gnome-platform-packages
	./build.sh root var packages ./list_packages.sh gnome-platform > gnome-platform-packages

gnome-platform.tar.xz: gnome-platform-packages packages/RPMS/noarch/gnome-platform-0.1-1.noarch.rpm setup.sh build.sh
	echo building gnome-platform
	./setup_root.sh root var yocto-build/x86_64/images/gnomeos-contents-platform-x86_64.tar.gz
	./build.sh root var packages rpm -Uvh `cat gnome-platform-packages`
	tar --transform 's,^root/usr/,,S' -cJf gnome-platform.tar.xz root/usr --owner=root
	tar --transform 's,^var/,,S' -cJf gnome-platform-rpmdb.tar.xz var/lib/rpm --owner=root

-include rpm-dependencies.P
