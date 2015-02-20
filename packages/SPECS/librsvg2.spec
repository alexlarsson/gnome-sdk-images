%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           librsvg2
Summary:        An SVG library based on cairo
Version:        2.40.7
Release:        1%{?dist}

License:        LGPLv2+
Group:          System Environment/Libraries
#VCS:           git:git://git.gnome.org/librsvg
Source:         http://download.gnome.org/sources/librsvg/%{release_version}/librsvg-%{version}.tar.xz

BuildRequires:  freedesktop-sdk-base
BuildRequires:  glib2-dev
BuildRequires:  gdk-pixbuf2-dev
BuildRequires:  pango-dev
BuildRequires:  freetype-dev
BuildRequires:  cairo-dev
BuildRequires:  cairo-gobject-dev
BuildRequires:  libcroco-dev
BuildRequires:  gobject-introspection-dev
BuildRequires:  vala-dev
BuildRequires:  vala-tools

Requires(post):   gdk-pixbuf2%{?_isa}
Requires(postun): gdk-pixbuf2%{?_isa}

%description
An SVG library based on cairo.


%package dev
Summary:        Libraries and include files for developing with librsvg
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description dev
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.


%package tools
Summary:        Extra tools for librsvg
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
This package provides extra utilities based on the librsvg library.


%prep
%setup -q -n librsvg-%{version}


%build
GDK_PIXBUF_QUERYLOADERS=/usr/bin/gdk-pixbuf-query-loaders-%{__isa_bits}
export GDK_PIXBUF_QUERYLOADERS
# work around an ordering problem in configure
enable_pixbuf_loader=yes
export enable_pixbuf_loader
%configure --disable-static  \
        --disable-gtk-doc \
        --enable-introspection \
        --enable-vala
make %{?_smp_mflags}

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/svg-viewer.svg

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%postun
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_libdir}/librsvg-2.so.*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-svg.so
%{_libdir}/girepository-1.0/*

%files dev
%{_libdir}/librsvg-2.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/librsvg-2.0.pc
%{_datadir}/gir-1.0/*
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/librsvg-2.0.vapi
%doc %{_datadir}/gtk-doc/html/rsvg-2.0

%files tools
%{_bindir}/rsvg-convert
%{_mandir}/man1/rsvg-convert.1*


%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 2.40.5-1
- Initial version based on F21
