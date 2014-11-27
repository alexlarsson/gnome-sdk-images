srcdir = $(CURDIR)
builddir = $(CURDIR)

VERSION=3.14
ARCH=x86_64
IMAGES=yocto-build/$(ARCH)/images
SPECS=packages/SPECS
NOARCH=packages/RPMS/noarch

all: gnome-platform.tar.gz gnome-sdk.tar.gz

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
	dconf gvfs desktop-file-utils json-glib libnotify vte mozjs24 gjs \
	$(NULL)

ALL_SPECS =$(PACKAGES:%=$(SPECS)/%.spec)

deps: rpm-dependencies.P

rpm-dependencies.P: $(ALL_SPECS) makedeps.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh ./makedeps.sh $(ALL_SPECS) > rpm-dependencies.P

gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz: $(NOARCH)/gnome-sdk-0.1-1.noarch.rpm
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh smart install -y  $(NOARCH)/gnome-sdk-0.1-1.noarch.rpm
	rm -rf gnome-sdk.tar.gz
	tar --transform 's,^root/usr,files,S' -czf gnome-sdk.tar.gz root/usr --owner=root
	tar --transform 's,^var,files,S' -czf gnome-sdk-rpmdb.tar.gz var/lib/rpm --owner=root

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

gnome-platform.tar.gz gnome-platform-rpmdb.tar.gz: gnome-platform-packages $(NOARCH)/gnome-platform-0.1-1.noarch.rpm setup.sh build.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	-echo building gnome-platform
	./setup_root.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	./build.sh rpm -Uvh `cat gnome-platform-packages`
	tar --transform 's,^root/usr,files,S' -czf gnome-platform.tar.gz root/usr --owner=root
	tar --transform 's,^var,files,S' -czf gnome-platform-rpmdb.tar.gz var/lib/rpm --owner=root

repository:
	ostree  init --mode=archive-z2 --repo=repository

#TODO: Add --owner-uid=0 --owner-gid=0
commit-platform: repository gnome-platform.tar.gz  gnome-platform-rpmdb.tar.gz
	rm -rf commit
	mkdir -p commit
	tar xf gnome-platform.tar.gz -C commit
	ostree commit --repo=repository --branch=runtime/org.gnome.Platform/$(ARCH)/$(VERSION) --disable-fsync --no-xattrs -s "commit" commit
	rm -rf commit
	mkdir -p commit
	tar xf gnome-platform-rpmdb.tar.gz -C commit
	ostree commit --repo=repository --branch=runtime/org.gnome.PlatformVar/$(ARCH)/$(VERSION) --disable-fsync --no-xattrs -s "commit" commit

commit-sdk: repository gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz
	rm -rf commit
	mkdir -p commit
	tar xf gnome-sdk.tar.gz -C commit
	ostree commit --repo=repository --branch=runtime/org.gnome.Sdk/$(ARCH)/$(VERSION) --disable-fsync --no-xattrs -s "commit" commit
	rm -rf commit
	mkdir -p commit
	tar xf gnome-sdk-rpmdb.tar.gz -C commit
	ostree commit --repo=repository --branch=runtime/org.gnome.SdkVar/$(ARCH)/$(VERSION) --disable-fsync --no-xattrs -s "commit" commit

commit: commit-sdk commit-platform



-include rpm-dependencies.P
