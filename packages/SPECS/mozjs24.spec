Summary:	JavaScript interpreter and libraries
Name:		mozjs24
Version:	24.2.0
Release:	1%{?dist}
License:	MPLv2.0
Group:		Development/Languages
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/mozjs-%{version}.tar.bz2

BuildRequires: gnome-sdk-base

Patch0:		mozjs-build-fixes.patch

%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
super set of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n mozjs-%{version}
# Delete bundled sources
rm js/src/editline -rf
rm js/src/ctypes/libffi -rf
%patch0 -p1
chmod a+x configure

%build
%configure \
  --disable-static \
  --with-system-nspr \
  --enable-threadsafe \
  --enable-readline \
  --enable-xterm-updates
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# For some reason the headers and pkg-config file are executable
find %{buildroot}%{_includedir} -type f -exec chmod a-x {} \;
chmod a-x  %{buildroot}%{_libdir}/pkgconfig/*.pc
# Upstream does not honor --disable-static yet
rm -f %{buildroot}%{_libdir}/*.a
# This is also statically linked; once that is fixed that we could
# consider shipping it.
rm -f %{buildroot}%{_bindir}/js24

# However, delete js-config since everything should use
# the pkg-config file.
rm -f %{buildroot}%{_bindir}/js24-config

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE README
%{_libdir}/*.so

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/mozjs-24

%changelog
* Tue Nov 25 2014 Alexander Larsson <alexl@redhat.com> - 24.2.0-1
- Initial version, based on F21
