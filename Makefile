# Override the arch with `make ARCH=i386`
ARCH   ?= $(shell xdg-app --default-arch)

# SDK Versions setup here
#
# SDK_BRANCH:          The version (branch) of runtime and sdk to produce
# SDK_RUNTIME_VERSION: The org.freedesktop.BaseSdk and platform version to build against
#
SDK_BRANCH=master
SDK_RUNTIME_VERSION=1.4

# Canned recipe for generating metadata
SUBST_FILES=org.gnome.Sdk.json metadata.sdk metadata.platform
define subst-metadata
	@echo -n "Generating files: ${SUBST_FILES}... ";
	@for file in ${SUBST_FILES}; do 					\
	  file_source=$${file}.in; 						\
	  sed -e 's/@@SDK_ARCH@@/${ARCH}/g' 					\
	      -e 's/@@SDK_BRANCH@@/${SDK_BRANCH}/g' 				\
	      -e 's/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g' 		\
	      $$file_source > $$file.tmp && mv $$file.tmp $$file || exit 1;	\
	done
	@echo "Done.";
endef

all: repo $(patsubst %,%.in,$(SUBST_FILES))
	rm -rf sdk
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=repo --arch=${ARCH} \
                        --subject="build of org.gnome.Sdk, `date`" \
                        ${EXPORT_ARGS} sdk org.gnome.Sdk.json
	rm -rf sdk

repo:
	ostree  init --mode=archive-z2 --repo=repo

check:
	json-glib-validate org.gnome.Sdk.json
