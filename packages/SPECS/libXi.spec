Summary: X.Org X11 libXi runtime library
Name: libXi
Version: 1.7.4
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: gnome-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel

Requires: libX11

%description
X.Org X11 libXi runtime library

%package devel
Summary: X.Org X11 libXi development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
# required by xi.pc
Requires: xorg-x11-proto-devel

%description devel
X.Org X11 libXi development package

%prep
%setup -q -n libXi-%{version}

# Disable static library creation by default.
%define with_static 0

%build
autoreconf -v --install || exit 1
%configure --disable-specs \
%if ! %{with_static}
	--disable-static
%endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libXi.so.6
%{_libdir}/libXi.so.6.1.0

%files devel
%defattr(-,root,root,-)
%if %{with_static}
%{_libdir}/libXi.a
%endif
%{_includedir}/X11/extensions/XInput.h
%{_includedir}/X11/extensions/XInput2.h
%{_libdir}/libXi.so
%{_libdir}/pkgconfig/xi.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.7.4-1
- Initial version based on f21
