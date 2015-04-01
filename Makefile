srcdir = $(CURDIR)
builddir = $(CURDIR)

FREEDESKTOP_VERSION=1.0
GNOME_VERSION=3.16
ARCH=x86_64
IMAGEDIR=freedesktop-sdk-base/images/$(ARCH)
SPECS=packages/SPECS
NOARCH=packages/RPMS/noarch
BASE_HASH=8e44c998adbf1546c45cf733c688fed74e8ddc89

EXTRA_NAME=
DELTAS=
GPG_KEY=
GPG_HOME=

all: gnome-platform.tar.gz gnome-sdk.tar.gz

SDK_BASE_IMAGE=$(IMAGEDIR)/freedesktop-contents-sdk-$(ARCH)-$(BASE_HASH).tar.gz
PLATFORM_BASE_IMAGE=$(IMAGEDIR)/freedesktop-contents-platform-$(ARCH)-$(BASE_HASH).tar.gz

$(SDK_BASE_IMAGE) $(PLATFORM_BASE_IMAGE) images:
	if test ! -d freedesktop-sdk-base; then \
		git clone git://git.gnome.org/freedesktop-sdk-base;\
	fi
	(cd  freedesktop-sdk-base && \
	 git fetch origin && \
	 git checkout $(BASE_HASH) && \
	 make)

NULL=

PACKAGES = \
	freedesktop-platform-base \
	freedesktop-sdk-base \
	freedesktop-platform \
	freedesktop-sdk \
	gnome-platform \
	gnome-sdk \
	\
	SDL2 \
	SDL2_image \
	SDL2_mixer \
	SDL2_net \
	SDL2_ttf \
	abattis-cantarell-fonts \
	adwaita-icon-theme \
	aspell \
	at-spi2-atk \
	at-spi2-core \
	atk \
	cairo \
	clutter \
	clutter-gtk \
	cogl \
	dbus \
	dbus-glib \
	dconf \
	dejavu-fonts \
	desktop-file-utils \
	enchant \
	fontconfig \
	freetype \
	gdk-pixbuf2 \
	gjs \
	glib-networking \
	glib2 \
	gnome-common \
	gnome-themes-standard \
	gnu-free-fonts \
	gobject-introspection \
	google-crosextra-caladea-fonts \
	google-crosextra-carlito-fonts \
	graphite2 \
	gsettings-desktop-schemas \
	gstreamer1 \
	gstreamer1-plugins-base \
	gtk-doc-stub \
	gtk2 \
	gtk3 \
	gvfs \
	harfbuzz \
	hicolor-icon-theme \
	hunspell-en hunspell \
	itstool \
	json-glib \
	libICE \
	libSM \
	libX11 \
	libXScrnSaver \
	libXau \
	libXcomposite \
	libXcursor \
	libXdamage \
	libXdmcp \
	libXext \
	libXfixes \
	libXft \
	libXi \
	libXinerama \
	libXpm \
	libXrandr \
	libXrender \
	libXt \
	libXtst \
	libXv \
	libXvMC \
	libXxf86vm \
	libappstream-glib \
	libcroco \
	libdatrie \
	libdrm \
	libepoxy \
	liberation-fonts \
	libnotify \
	libpciaccess \
	libproxy \
	librsvg2 \
	libsecret \
	libsoup \
	libthai \
	libxcb \
	libxkbcommon \
	libxkbfile \
	libxshmfence \
	llvm \
	mesa \
	mozjs24 \
	orc \
	pango \
	pixman \
	pulseaudio \
	pygobject3 \
	python3-cairo \
	shared-mime-info \
	vala \
	vte \
	wayland \
	webkitgtk4 \
	xcb-proto \
	xkeyboard-config \
	xorg-x11-proto-devel \
	xorg-x11-util-macros \
	xorg-x11-xtrans-devel \
	yelp-tools \
	yelp-xsl \
	zenity \
	$(NULL)

ALL_SPECS =$(PACKAGES:%=$(SPECS)/%.spec)

deps: rpm-dependencies.P

rpm-dependencies.P: $(ALL_SPECS) makedeps.sh $(SDK_BASE_IMAGE)
	./setup.sh $(SDK_BASE_IMAGE)
	./build.sh ./makedeps.sh $(ALL_SPECS) > rpm-dependencies.P
	./clear_root.sh

gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz: $(NOARCH)/gnome-sdk-0.1-1.sdk.noarch.rpm
	./setup.sh $(SDK_BASE_IMAGE)
	./build.sh smart install -y  $(NOARCH)/gnome-sdk-0.1-1.sdk.noarch.rpm
	rm -rf gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz
	tar --transform 's,^build/root/usr,files,S' -czf gnome-sdk.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf gnome-sdk-rpmdb.tar.gz build/var/lib/rpm --owner=root
	./clear_root.sh

freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz: $(NOARCH)/freedesktop-sdk-0.1-1.sdk.noarch.rpm
	./setup.sh $(SDK_BASE_IMAGE)
	./build.sh smart install -y  $(NOARCH)/freedesktop-sdk-0.1-1.sdk.noarch.rpm
	rm -rf freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
	tar --transform 's,^build/root/usr,files,S' -czf freedesktop-sdk.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf freedesktop-sdk-rpmdb.tar.gz build/var/lib/rpm --owner=root
	./clear_root.sh

freedesktop-platform-base: $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm

$(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm: $(SPECS)/freedesktop-platform-base.spec setup.sh build.sh $(PLATFORM_BASE_IMAGE) $(SDK_BASE_IMAGE)
	-echo building freedesktop-platform-base.spec
	rm -rf packages/freedesktop-platform
	mkdir -p packages/freedesktop-platform
	tar -C packages/freedesktop-platform -xzf $(PLATFORM_BASE_IMAGE)
	./setup.sh $(SDK_BASE_IMAGE)
	./build.sh rpmbuild -ba $(SPECS)/freedesktop-platform-base.spec
	./clear_root.sh

freedesktop-sdk-base: $(NOARCH)/freedesktop-sdk-base-0.1-1.sdk.noarch.rpm

freedesktop-platform-packages: $(NOARCH)/freedesktop-platform-0.1-1.sdk.noarch.rpm $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm setup.sh build.sh
	./setup.sh $(SDK_BASE_IMAGE)
	rm -f freedesktop-platform-packages
	./build.sh ./list_packages.sh freedesktop-platform > freedesktop-platform-packages
	./clear_root.sh

freedesktop-platform.tar.gz freedesktop-platform-rpmdb.tar.gz: freedesktop-platform-packages $(NOARCH)/freedesktop-platform-0.1-1.sdk.noarch.rpm setup.sh build.sh $(PLATFORM_BASE_IMAGE)
	-echo building freedesktop-platform
	./setup_root.sh $(PLATFORM_BASE_IMAGE)
	./build.sh rpm -Uvh `cat freedesktop-platform-packages`
	tar --transform 's,^build/root/usr,files,S' -czf freedesktop-platform.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf freedesktop-platform-rpmdb.tar.gz build/var/lib/rpm --owner=root
	./clear_root.sh

gnome-platform-packages: $(NOARCH)/gnome-platform-0.1-1.sdk.noarch.rpm $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm setup.sh build.sh
	./setup.sh $(SDK_BASE_IMAGE)
	rm -f gnome-platform-packages
	./build.sh ./list_packages.sh gnome-platform > gnome-platform-packages
	./clear_root.sh

gnome-platform.tar.gz gnome-platform-rpmdb.tar.gz: gnome-platform-packages $(NOARCH)/gnome-platform-0.1-1.sdk.noarch.rpm setup.sh build.sh $(PLATFORM_BASE_IMAGE)
	-echo building gnome-platform
	./setup_root.sh $(PLATFORM_BASE_IMAGE)
	./build.sh rpm -Uvh `cat gnome-platform-packages`
	tar --transform 's,^build/root/usr,files,S' -czf gnome-platform.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf gnome-platform-rpmdb.tar.gz build/var/lib/rpm --owner=root
	./clear_root.sh

repo:
	ostree  init --mode=archive-z2 --repo=repo

commit-freedesktop-platform: repo freedesktop-platform.tar.gz  freedesktop-platform-rpmdb.tar.gz
	./commit.sh repo freedesktop-platform.tar.gz freedesktop-platform-rpmdb.tar.gz metadata.freedesktop-platform org.freedesktop.Platform$(EXTRA_NAME) $(ARCH) $(FREEDESKTOP_VERSION)

commit-freedesktop-sdk: repo freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
	./commit.sh repo freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz metadata.freedesktop-sdk org.freedesktop.Sdk$(EXTRA_NAME) $(ARCH) $(FREEDESKTOP_VERSION)

commit-platform: repo gnome-platform.tar.gz  gnome-platform-rpmdb.tar.gz
	./commit.sh repo gnome-platform.tar.gz gnome-platform-rpmdb.tar.gz metadata.platform org.gnome.Platform$(EXTRA_NAME) $(ARCH) $(GNOME_VERSION)

commit-sdk: repo gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz
	./commit.sh repo gnome-sdk.tar.gz gnome-sdk-rpmdb.tar.gz metadata.sdk org.gnome.Sdk$(EXTRA_NAME) $(ARCH) $(GNOME_VERSION)

commit-gnome: commit-sdk commit-platform
	echo done

commit-freedesktop: commit-freedesktop-sdk commit-freedesktop-platform
	echo done

commit: commit-gnome commit-freedesktop
	echo done

untag:
	./untag.sh repo org.freedesktop.Platform $(ARCH) $(FREEDESKTOP_VERSION) $(EXTRA_NAME)
	./untag.sh repo org.freedesktop.Sdk $(ARCH) $(FREEDESKTOP_VERSION) $(EXTRA_NAME)
	./untag.sh repo org.gnome.Platform $(ARCH) $(GNOME_VERSION) $(EXTRA_NAME)
	./untag.sh repo org.gnome.Sdk $(ARCH) $(GNOME_VERSION) $(EXTRA_NAME)

-include rpm-dependencies.P
