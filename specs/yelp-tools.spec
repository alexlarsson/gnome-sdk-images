%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:          yelp-tools
Version:       3.17.4
Release:       1%{?dist}
Summary:       Create, manage, and publish documentation for Yelp

Group:         Applications/Publishing
License:       GPLv2+
URL:           https://wiki.gnome.org/Apps/Yelp/Tools
Source0:       https://download.gnome.org/sources/%{name}/%{release_version}/%{name}-%{version}.tar.xz
BuildArch:     noarch

BuildRequires: freedesktop-sdk-base
BuildRequires: yelp-xsl-dev
BuildRequires: itstool

Requires: /usr/bin/itstool
Requires: /usr/bin/xmllint
Requires: yelp-xsl

%description
yelp-tools is a collection of scripts and build utilities to help create,
manage, and publish documentation for Yelp and the web. Most of the heavy
lifting is done by packages like yelp-xsl and itstool. This package just
wraps things up in a developer-friendly way.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" install

%files
%doc AUTHORS COPYING COPYING.GPL README
%{_bindir}/yelp-build
%{_bindir}/yelp-check
%{_bindir}/yelp-new
%{_datadir}/yelp-tools
%{_datadir}/aclocal/yelp.m4

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 3.14.1-1
- Initial version based on F21
