# Override the arch with `make ARCH=i386`
ARCH   ?= $(shell flatpak --default-arch)
REPO   ?= repo
FB_ARGS ?=

# SDK Versions setup here
#
# SDK_BRANCH:          The version (branch) of runtime and sdk to produce
# SDK_RUNTIME_VERSION: The org.freedesktop.BaseSdk and platform version to build against
#
SDK_BRANCH=3.26
SDK_RUNTIME_VERSION=1.6

# Canned recipe for generating metadata
SUBST_FILES=org.gnome.Sdk.json os-release issue issue.net org.gnome.Platform.appdata.xml org.gnome.Sdk.appdata.xml
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

all: ${REPO} $(patsubst %,%.in,$(SUBST_FILES))
	$(call subst-metadata)
	flatpak-builder --force-clean --require-changes --repo=${REPO} --arch=${ARCH} \
                        --subject="build of org.gnome.Sdk, `date`" \
                        ${EXPORT_ARGS} ${FB_ARGS} sdk org.gnome.Sdk.json

${REPO}:
	ostree  init --mode=archive-z2 --repo=${REPO}

check:
	json-glib-validate org.gnome.Sdk.json
