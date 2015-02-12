srcdir = $(CURDIR)
builddir = $(CURDIR)

FREEDESKTOP_VERSION=0.1
GNOME_VERSION=3.16
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
	freedesktop-platform-base freedesktop-sdk-base \
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
	libXfixes libXext libXft libXi libXinerama libICE libSM libXpm libXrandr libXtst libXt libXScrnSaver libXpm \
	libXv libXvMC libXxf86vm libXdamage libXcursor libXcomposite libxkbfile libxshmfence \
	xkeyboard-config libxkbcommon \
	SDL2 \
	dbus cairo dbus-glib \
	libpciaccess libdrm llvm mesa libepoxy wayland \
	pulseaudio \
	freedesktop-platform freedesktop-sdk \
	graphite2 harfbuzz libdatrie libthai pango atk at-spi2-core at-spi2-atk gdk-pixbuf2 gtk3 \
	libsecret \
	itstool yelp-xsl yelp-tools \
	hicolor-icon-theme libcroco vala librsvg2 adwaita-icon-theme \
	gnome-sdk gnome-platform dejavu-fonts abattis-cantarell-fonts \
	gtk2 gnome-themes-standard libproxy gsettings-desktop-schemas glib-networking libsoup \
	dconf gvfs desktop-file-utils json-glib libnotify vte mozjs24 gjs \
	gstreamer1 python3-cairo pygobject3 \
	cogl clutter clutter-gtk webkitgtk4 \
	aspell hunspell-en hunspell enchant \
	zenity \
	$(NULL)

ALL_SPECS =$(PACKAGES:%=$(SPECS)/%.spec)

deps: rpm-dependencies.P

rpm-dependencies.P: $(ALL_SPECS) makedeps.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh ./makedeps.sh $(ALL_SPECS) > rpm-dependencies.P

gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz: $(NOARCH)/gnome-sdk-0.1-1.sdk.noarch.rpm
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh smart install -y  $(NOARCH)/gnome-sdk-0.1-1.sdk.noarch.rpm
	rm -rf gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz
	tar --transform 's,^root/usr,files,S' -czf gnome-sdk.tar.gz root/usr --owner=root
	tar --transform 's,^var,files,S' -czf gnome-sdk-rpmdb.tar.gz var/lib/rpm --owner=root

freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz: $(NOARCH)/freedesktop-sdk-0.1-1.sdk.noarch.rpm
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh smart install -y  $(NOARCH)/freedesktop-sdk-0.1-1.sdk.noarch.rpm
	rm -rf freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
	tar --transform 's,^root/usr,files,S' -czf freedesktop-sdk.tar.gz root/usr --owner=root
	tar --transform 's,^var,files,S' -czf freedesktop-sdk-rpmdb.tar.gz var/lib/rpm --owner=root

freedesktop-platform-base: $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm

$(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm: $(SPECS)/freedesktop-platform-base.spec setup.sh build.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	-echo building freedesktop-platform-base.spec
	rm -rf packages/freedesktop-platform
	mkdir -p packages/freedesktop-platform
	tar -C packages/freedesktop-platform -xzf $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	./build.sh rpmbuild -ba $(SPECS)/freedesktop-platform-base.spec

freedesktop-sdk-base: $(NOARCH)/freedesktop-sdk-base-0.1-1.sdk.noarch.rpm

freedesktop-platform-packages: $(NOARCH)/freedesktop-platform-0.1-1.sdk.noarch.rpm $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm setup.sh build.sh
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	rm -f freedesktop-platform-packages
	./build.sh ./list_packages.sh freedesktop-platform > freedesktop-platform-packages

freedesktop-platform.tar.gz freedesktop-platform-rpmdb.tar.gz: freedesktop-platform-packages $(NOARCH)/freedesktop-platform-0.1-1.sdk.noarch.rpm setup.sh build.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	-echo building freedesktop-platform
	./setup_root.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	./build.sh rpm -Uvh `cat freedesktop-platform-packages`
	tar --transform 's,^root/usr,files,S' -czf freedesktop-platform.tar.gz root/usr --owner=root
	tar --transform 's,^var,files,S' -czf freedesktop-platform-rpmdb.tar.gz var/lib/rpm --owner=root

gnome-platform-packages: $(NOARCH)/gnome-platform-0.1-1.sdk.noarch.rpm $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm setup.sh build.sh
	./setup.sh $(IMAGES)/gnomeos-contents-sdk-$(ARCH).tar.gz
	rm -f gnome-platform-packages
	./build.sh ./list_packages.sh gnome-platform > gnome-platform-packages

gnome-platform.tar.gz gnome-platform-rpmdb.tar.gz: gnome-platform-packages $(NOARCH)/gnome-platform-0.1-1.sdk.noarch.rpm setup.sh build.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	-echo building gnome-platform
	./setup_root.sh $(IMAGES)/gnomeos-contents-platform-$(ARCH).tar.gz
	./build.sh rpm -Uvh `cat gnome-platform-packages`
	tar --transform 's,^root/usr,files,S' -czf gnome-platform.tar.gz root/usr --owner=root
	tar --transform 's,^var,files,S' -czf gnome-platform-rpmdb.tar.gz var/lib/rpm --owner=root

repository:
	ostree  init --mode=archive-z2 --repo=repository

commit-freedesktop-platform: repository freedesktop-platform.tar.gz  freedesktop-platform-rpmdb.tar.gz
	./commit.sh repository freedesktop-platform.tar.gz freedesktop-platform-rpmdb.tar.gz metadata.freedesktop-platform org.freedesktop.Platform $(ARCH) $(FREEDESKTOP_VERSION)

commit-freedesktop-sdk: repository freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
	./commit.sh repository freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz metadata.freedesktop-sdk org.freedesktop.Sdk $(ARCH) $(FREEDESKTOP_VERSION)

commit-platform: repository gnome-platform.tar.gz  gnome-platform-rpmdb.tar.gz
	./commit.sh repository gnome-platform.tar.gz gnome-platform-rpmdb.tar.gz metadata.platform org.gnome.Platform $(ARCH) $(GNOME_VERSION)

commit-sdk: repository gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz
	./commit.sh repository gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz metadata.sdk org.gnome.Sdk $(ARCH) $(GNOME_VERSION)

commit-gnome: commit-sdk commit-platform
	echo done

commit-freedesktop: commit-freedesktop-sdk commit-freedesktop-platform
	echo done

commit: commit-gnome commit-freedesktop
	echo done

release/repo:
	ostree  init --mode=archive-z2 --repo=release/repo

release-commit-freedesktop-platform: release/repo freedesktop-platform.tar.gz  freedesktop-platform-rpmdb.tar.gz
	./commit.sh release/repo freedesktop-platform.tar.gz freedesktop-platform-rpmdb.tar.gz metadata.freedesktop-platform org.freedesktop.Platform $(ARCH) $(FREEDESKTOP_VERSION)

release-commit-freedesktop-sdk: release/repo freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
	./commit.sh release/repo freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz metadata.freedesktop-sdk org.freedesktop.Sdk $(ARCH) $(FREEDESKTOP_VERSION)

release-commit-platform: release/repo gnome-platform.tar.gz  gnome-platform-rpmdb.tar.gz
	./commit.sh release/repo gnome-platform.tar.gz gnome-platform-rpmdb.tar.gz metadata.platform org.gnome.Platform $(ARCH) $(GNOME_VERSION)

release-commit-sdk: release/repo gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz
	./commit.sh release/repo gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz metadata.sdk org.gnome.Sdk $(ARCH) $(GNOME_VERSION)

release-commit-gnome: release-commit-sdk release-commit-platform
	echo done

release-commit-freedesktop: release-commit-freedesktop-sdk release-commit-freedesktop-platform
	echo done

release-commit: release-commit-gnome release-commit-freedesktop
	echo done

-include rpm-dependencies.P
