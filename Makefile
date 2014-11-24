srcdir = $(CURDIR)
builddir = $(CURDIR)

ARCH=x86_64
IMAGES=yocto-build/$(ARCH)/images
SPECS=packages/SPECS
NOARCH=packages/RPMS/noarch

all: gnome-platform.tar.xz gnome-sdk.tar.xz

$(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz images:
	if test ! -d gnome-continuous-yocto; then \
		git clone https://github.com/alexlarsson/gnome-continuous-yocto.git --branch gnomeostree-3.14-dizzy-platform;\
	fi
	(cd  gnome-continuous-yocto; git pull;)
	(cd  gnome-continuous-yocto; git submodule update --init;)
	mkdir -p yocto-build/$(ARCH)
	./gnome-sdk-build-yocto ${srcdir}/gnome-continuous-yocto ${builddir}/yocto-build/ $(ARCH)

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
	gnome-sdk gnome-platform dejavu-fonts abattis-cantarell-fonts \
	gtk2 gnome-themes-standard libproxy gsettings-desktop-schemas glib-networking libsoup \
	$(NULL)

ALL_SPECS =$(PACKAGES:%=$(SPECS)/%.spec)

deps: rpm-dependencies.P

rpm-dependencies.P: $(ALL_SPECS) makedeps.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh ./makedeps.sh $(ALL_SPECS) > rpm-dependencies.P

gnome-sdk.tar.xz gnome-sdk-rpmdb.tar.xz: $(NOARCH)/gnome-sdk-0.1-1.noarch.rpm
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh smart install -y  $(NOARCH)/gnome-sdk-0.1-1.noarch.rpm
	rm -rf gnome-sdk.tar.xz
	tar --transform 's,^root/usr/,,S' -cJf gnome-sdk.tar.xz root/usr --owner=root
	tar --transform 's,^var/,,S' -cJf gnome-sdk-rpmdb.tar.xz var/lib/rpm --owner=root

gnome-platform-base: $(NOARCH)/gnome-platform-base-0.1-1.noarch.rpm

$(NOARCH)/gnome-platform-base-0.1-1.noarch.rpm: $(SPECS)/gnome-platform-base.spec setup.sh build.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	-echo building gnome-platform-base.spec
	rm -rf packages/gnome-platform
	mkdir -p packages/gnome-platform
	tar -C packages/gnome-platform -xzf $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh rpmbuild -ba $(SPECS)/gnome-platform-base.spec

gnome-sdk-base: $(NOARCH)/gnome-sdk-base-0.1-1.noarch.rpm

gnome-platform-packages: $(NOARCH)/gnome-platform-0.1-1.noarch.rpm setup.sh build.sh
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	rm -f gnome-platform-packages
	./build.sh ./list_packages.sh gnome-platform > gnome-platform-packages

gnome-platform.tar.xz gnome-platform-rpmdb.tar.xz: gnome-platform-packages $(NOARCH)/gnome-platform-0.1-1.noarch.rpm setup.sh build.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	-echo building gnome-platform
	./setup_root.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	./build.sh rpm -Uvh `cat gnome-platform-packages`
	tar --transform 's,^root/usr/,,S' -cJf gnome-platform.tar.xz root/usr --owner=root
	tar --transform 's,^var/,,S' -cJf gnome-platform-rpmdb.tar.xz var/lib/rpm --owner=root

-include rpm-dependencies.P
