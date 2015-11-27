NAME=gnome
ID=org.gnome
VERSION=3.18
ARCH=x86_64
IMAGEDIR=freedesktop-sdk-base/images/$(ARCH)
BASE_HASH=fb9431b869642eab9a0f4489370aba27d1e75e07

EXTRA_NAME=
DELTAS=
GPG_KEY=
GPG_HOME=

BASE_SPECS=$(wildcard freedesktop-sdk-images/specs/*.spec)
BASE_SPECS_BASENAME=$(notdir $(BASE_SPECS))
GNOME_SPECS=$(wildcard specs/*.spec)
GNOME_SPECS_BASENAME=$(notdir $(GNOME_SPECS))

# ALL_SPECS is all of GNOME_SPECS and the ones from BASE_SPECS that are not overridden by GNOME_SPECS
ALL_SPECS = $(addprefix freedesktop-sdk-images/specs/,$(filter-out $(GNOME_SPECS_BASENAME),$(BASE_SPECS_BASENAME))) $(GNOME_SPECS)

all: $(NAME)-$(VERSION)-platform.tar.gz $(NAME)-$(VERSION)-sdk.tar.gz

debug: $(NAME)-$(VERSION)-debug.tar.gz

include freedesktop-sdk-images/Makefile.inc
-include rpm-dependencies.P

$(SDK_BASE_IMAGE) $(PLATFORM_BASE_IMAGE) images:
	if test ! -d freedesktop-sdk-base; then \
		git clone git://anongit.freedesktop.org/xdg-app/freedesktop-sdk-base;\
	fi
	(cd  freedesktop-sdk-base && \
	 git fetch origin && \
	 git checkout $(BASE_HASH) && \
	 make)

