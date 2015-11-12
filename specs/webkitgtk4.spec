# Disable debug info by default.
%define with_webkit_debug 1

## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global add_to_license_files() \
        mkdir -p _license_files ; \
        cp -p %1 _license_files/$(echo '%1' | sed -e 's!/!.!g')

Name:           webkitgtk4
Version:        2.10.4
Release:        1%{?dist}
Summary:        GTK+ Web content engine library

License:        LGPLv2
URL:            http://www.webkitgtk.org/
Source0:        http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz
BuildRequires: at-spi2-core-dev
BuildRequires: cairo-dev
BuildRequires: enchant-dev
BuildRequires: fontconfig-dev
BuildRequires: freetype-dev
BuildRequires: glib2-dev
BuildRequires: gobject-introspection-dev
BuildRequires: gstreamer1-dev
BuildRequires: gstreamer1-plugins-base-dev
BuildRequires: gtk2-dev
BuildRequires: gtk3-dev
BuildRequires: harfbuzz-dev
BuildRequires: libsecret-dev
BuildRequires: libsoup-dev
BuildRequires: libXt-dev
BuildRequires: mesa-libGL-dev
BuildRequires: mesa-libEGL-dev
BuildRequires: geoclue2-dev
BuildRequires: libwayland-client-dev
BuildRequires: libwayland-cursor-dev
BuildRequires: libwayland-server-dev
BuildRequires: libnotify-dev
BuildRequires: hyphen-dev

# Filter out provides for private libraries
%global __provides_exclude_from ^%{_libdir}/webkit2gtk-4\\.0/.*\\.so$

%description
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

This package contains WebKitGTK+ for GTK+ 3.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    dev
The %{name}-dev package contains libraries, build data, and header
files for developing applications that use %{name}.

%prep
%setup -q -n webkitgtk-%{version}

%build

# Disable ld.gold on s390 as it does not have it.
# Also for aarch64 as the support is in upstream, but not packaged in Fedora.
mkdir -p %{_target_platform}
pushd %{_target_platform}
%if %{with_webkit_debug}
# Decrease debuginfo verbosity to reduce memory consumption even more
CFLAGS="%(echo %{optflags} | sed 's/-g/-g1/')"
%else
# Disable -g to save disk space during build
CFLAGS="%(echo %{optflags} | sed 's/-g//')"
%endif
export CFLAGS ; \
CXXFLAGS="${CFLAGS}" ; export CXXFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \
/usr/bin/cmake \
        -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DPORT=GTK \
        -DCMAKE_BUILD_TYPE=Release \
        -DENABLE_GTKDOC=OFF \
        -DENABLE_VIDEO=ON \
        -DENABLE_WEB_AUDIO=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%find_lang WebKit2GTK-4.0

# Finally, copy over and rename various files for %%license inclusion
%add_to_license_files Source/JavaScriptCore/COPYING.LIB
%add_to_license_files Source/JavaScriptCore/icu/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/compiler/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/murmurhash/LICENSE
%add_to_license_files Source/WebCore/icu/LICENSE
%add_to_license_files Source/WebCore/LICENSE-APPLE
%add_to_license_files Source/WebCore/LICENSE-LGPL-2
%add_to_license_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CodeMirror/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/Esprima/LICENSE
%add_to_license_files Source/WTF/icu/LICENSE
%add_to_license_files Source/WTF/wtf/dtoa/COPYING
%add_to_license_files Source/WTF/wtf/dtoa/LICENSE

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f WebKit2GTK-4.0.lang
%license _license_files/*
%{_libdir}/libjavascriptcoregtk-4.0.so.*
%{_libdir}/libwebkit2gtk-4.0.so.*
%{_libdir}/girepository-1.0/JavaScriptCore-4.0.typelib
%{_libdir}/girepository-1.0/WebKit2-4.0.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-4.0.typelib
%{_libdir}/webkit2gtk-4.0/
%{_libexecdir}/webkit2gtk-4.0/

%files dev
%{_bindir}/jsc
%{_includedir}/webkitgtk-4.0/
%{_libdir}/libjavascriptcoregtk-4.0.so
%{_libdir}/libwebkit2gtk-4.0.so
%{_libdir}/pkgconfig/javascriptcoregtk-4.0.pc
%{_libdir}/pkgconfig/webkit2gtk-4.0.pc
%{_libdir}/pkgconfig/webkit2gtk-web-extension-4.0.pc
%{_datadir}/gir-1.0/JavaScriptCore-4.0.gir
%{_datadir}/gir-1.0/WebKit2-4.0.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-4.0.gir

%changelog
* Thu Jan  8 2015 Alexander Larsson <alexl@redhat.com> - 2.7.3-1
- import from fedora
