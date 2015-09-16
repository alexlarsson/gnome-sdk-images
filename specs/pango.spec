%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')
%global bin_version 1.8.0

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.37.5
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
#VCS: git:git://git.gnome.org/pango
Source: http://download.gnome.org/sources/pango/%{release_version}/pango-%{version}.tar.xz
URL: http://www.pango.org

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: freetype-dev
BuildRequires: fontconfig-dev
BuildRequires: libXft-dev
BuildRequires: cairo-dev
BuildRequires: libthai-dev
BuildRequires: harfbuzz-dev
BuildRequires: gobject-introspection-dev
BuildRequires: cairo-gobject-dev

Requires: glib2%{?_isa}
Requires: freetype%{?_isa}
Requires: fontconfig%{?_isa}
Requires: cairo%{?_isa}
Requires: libthai%{?_isa}

%description
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

%package dev
Summary: Development files for pango
Group: Development/Libraries
Requires: pango%{?_isa} = %{version}-%{release}
Requires: glib2-dev%{?_isa}
Requires: freetype-dev%{?_isa}
Requires: fontconfig-dev%{?_isa}
Requires: cairo-dev%{?_isa}

%description dev
The pango-dev package includes the header files and developer documentation
for the pango package.

%package tests
Summary: Tests for the %{name} package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.


%prep
%setup -q -n pango-%{version}

%build

# We try hard to not link to libstdc++
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
          --enable-doc-cross-references \
          --enable-installed-tests
)
make %{?_smp_mflags} V=1


%install

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove files that should not be packaged
rm $RPM_BUILD_ROOT%{_libdir}/*.la

PANGOXFT_SO=$RPM_BUILD_ROOT%{_libdir}/libpangoxft-1.0.so
if ! test -e $PANGOXFT_SO; then
        echo "$PANGOXFT_SO not found; did not build with Xft support?"
        ls $RPM_BUILD_ROOT%{_libdir}
        exit 1
fi

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc README AUTHORS COPYING NEWS
%doc pango-view/HELLO.txt
%{_libdir}/libpango*-*.so.*
%{_bindir}/pango-view
%{_mandir}/man1/pango-view.1.gz
%{_libdir}/girepository-1.0/Pango-1.0.typelib
%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib
%{_libdir}/girepository-1.0/PangoXft-1.0.typelib


%files dev
%{_libdir}/libpango*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%doc %{_datadir}/gtk-doc/html/pango
%{_datadir}/gir-1.0/Pango-1.0.gir
%{_datadir}/gir-1.0/PangoCairo-1.0.gir
%{_datadir}/gir-1.0/PangoFT2-1.0.gir
%{_datadir}/gir-1.0/PangoXft-1.0.gir


%files tests
%{_libexecdir}/installed-tests/%{name}
%{_datadir}/installed-tests


%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 1.36.8-1
- Initial version based on F21
