Summary: An Enchanting Spell Checking Library
Name: enchant
Version: 1.6.0
Release: 1%{?dist}
Group: System Environment/Libraries
License: LGPLv2+
Source: http://www.abisource.com/downloads/enchant/%{version}/enchant-%{version}.tar.gz
URL: http://www.abisource.com/
BuildRequires: gnome-sdk-base
BuildRequires: glib2-dev
BuildRequires: hunspell-dev
BuildRequires: hunspell-en

%description
A library that wraps other spell checking backends.

%package dev
Summary: Support files necessary to compile applications with libenchant.
Group: Development/Libraries
Requires: enchant = %{version}-%{release}
Requires: glib2-dev

%description dev
Libraries, headers, and support files necessary to compile applications using libenchant.

%prep
%setup -q

%build
%configure --enable-myspell --with-myspell-dir=/usr/share/myspell --disable-static --disable-ispell --disable-aspell --disable-hspell --disable-zemberek
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/enchant/*.la

%files
%defattr(-,root,root)
%doc AUTHORS COPYING.LIB README
%{_bindir}/*
%{_libdir}/lib*.so.*
%dir %{_libdir}/enchant
%{_libdir}/enchant/lib*myspell.so*
%{_mandir}/man1/enchant.1*
%{_datadir}/enchant

%files dev
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/enchant.pc
%{_includedir}/enchant

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jan 22 2015 Alexander Larsson <alexl@redhat.com> - 1.6.0-1
- Initial version
