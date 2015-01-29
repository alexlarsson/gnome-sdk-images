%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:             libcroco
Summary:          A CSS2 parsing library
Version:          0.6.8
Release:          5%{?dist}
License:          LGPLv2
Group:            System Environment/Libraries
Source:           http://download.gnome.org/sources/libcroco/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires: gnome-sdk-base
BuildRequires: glib2-dev

%description
CSS2 parsing and manipulation library for GNOME

%package dev
Summary:          Libraries and include files for developing with libcroco
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         glib2-dev

%description dev
This package provides the necessary development libraries and include
files to allow you to develop with libcroco.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING COPYING.LIB NEWS README 
%{_bindir}/csslint-0.6
%{_libdir}/*.so.*

%files dev
%{_libdir}/*.so
%{_includedir}/libcroco-0.6
%{_bindir}/croco-0.6-config
%{_libdir}/pkgconfig/libcroco-0.6.pc
%{_datadir}/gtk-doc/html/libcroco

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 0.6.8-5
- Initial version based on F21
