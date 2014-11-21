Name:           gdk-pixbuf2
Version:        2.31.1
Release:        1%{?dist}
Summary:        An image loading library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gt.org
#VCS:           git:git://git.gnome.org/gdk-pixbuf
Source0:        http://download.gnome.org/sources/gdk-pixbuf/2.31/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  gnome-sdk-base
BuildRequires:  glib2-devel
BuildRequires:  libX11-devel
BuildRequires:  gobject-introspection-devel
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info-devel

Requires: glib2%{?_isa} >= %{glib2_version}

# We also need MIME information at runtime
Requires: shared-mime-info

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%package devel
Summary: Development files for gdk-pixbuf
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa}

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf.

%package tests
Summary: Tests for the %{name} package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.


%prep
%setup -q -n gdk-pixbuf-%{version}

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS             \
        --with-x11                   \
        --without-libjasper          \
        --with-included-loaders=png  \
        --enable-installed-tests
)
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT    \
             RUN_QUERY_LOADER_TEST=false

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.la

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)

%find_lang gdk-pixbuf

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :
fi

%files -f gdk-pixbuf.lang
%doc AUTHORS COPYING NEWS
%{_libdir}/libgdk_pixbuf-2.0.so.*
%{_libdir}/libgdk_pixbuf_xlib-2.0.so.*
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%{_includedir}/gdk-pixbuf-2.0
%{_libdir}/libgdk_pixbuf-2.0.so
%{_libdir}/libgdk_pixbuf_xlib-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/gdk-pixbuf-csource.1*

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests


%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 2.31.1-1
- Initial version based on F21
