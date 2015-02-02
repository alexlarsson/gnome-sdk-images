# first two digits of version
%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libsecret
Version:        0.18
Release:        1%{?dist}
Summary:        Library for storing and retrieving passwords and other secrets

License:        LGPLv2+
URL:            https://live.gnome.org/Libsecret
Source0:        http://download.gnome.org/sources/libsecret/%{release_version}/libsecret-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: gobject-introspection-dev
BuildRequires: gtk-doc-stub
BuildRequires: vala-dev
BuildRequires: vala-tools

%description
libsecret is a library for storing and retrieving passwords and other secrets.
It communicates with the "Secret Service" using DBus. gnome-keyring and
KSecretService are both implementations of a Secret Service.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
aclocal --force
autoconf
%configure --disable-static --disable-gtk-doc --disable-manpages
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang libsecret

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f libsecret.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/secret-tool
%{_libdir}/libsecret-1.so.*
%{_libdir}/girepository-1.0/Secret-1.typelib

%files dev
%{_includedir}/libsecret-1/
%{_libdir}/libsecret-1.so
%{_libdir}/pkgconfig/libsecret-1.pc
%{_libdir}/pkgconfig/libsecret-unstable.pc
%{_datadir}/gir-1.0/Secret-1.gir
%{_datadir}/vala/vapi/libsecret-1.deps
%{_datadir}/vala/vapi/libsecret-1.vapi
%doc %{_datadir}/gtk-doc/


%changelog
* Fri Jan  9 2015 Alexander Larsson <alexl@redhat.com> - 0.18-1
- Initial version from fedora
