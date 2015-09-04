%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           yelp-xsl
Version:        3.17.90
Release:        1%{?dist}
Summary:        XSL stylesheets for the yelp help browser

License:        LGPLv2+
Group:          Applications/System
URL:            http://download.gnome.org/sources/yelp-xsl
Source0:        http://download.gnome.org/sources/yelp-xsl/%{release_version}/yelp-xsl-%{version}.tar.xz
BuildArch:      noarch

BuildRequires: freedesktop-sdk-base
BuildRequires: itstool

%description
This package contains XSL stylesheets that are used by the yelp help browser.


%package dev
Summary: Developer documentation for yelp-xsl
Requires: %{name} = %{version}-%{release}

%description dev
The yelp-xsl-dev package contains developer documentation for the
XSL stylesheets in yelp-xsl.


%prep
%setup -q


%build
%configure --enable-doc
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"


%files
%doc README COPYING AUTHORS
%{_datadir}/yelp-xsl


%files dev
%{_datadir}/pkgconfig/yelp-xsl.pc


%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 3.14.0-1
- Initial version based on F21
