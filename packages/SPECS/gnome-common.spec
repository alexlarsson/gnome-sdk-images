Name:           gnome-common
Version:        3.14.0
Release:        1%{?dist}
Summary:        Useful things common to building GNOME packages from scratch

Group:          Development/Tools
BuildArch:      noarch
License:        GPLv2+
URL:            https://wiki.gnome.org/Projects/GnomeCommon
Source0:        https://download.gnome.org/sources/%{name}/3.14/%{name}-%{version}.tar.xz

BuildRequires: gnome-sdk-base
BuildRequires: yelp-tools
Requires: yelp-tools

%description
This package contains sample files that should be used to develop pretty much
every GNOME application.  The programs included here are not needed for running
GNOME apps or building ones from distributed tarballs.  They are only useful
for compiling from git sources or when developing the build infrastructure for
a GNOME application.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}
cp -p doc-build/README doc-README

%install
make DESTDIR=%{buildroot} INSTALL="install -p" install

%files
%doc doc-README ChangeLog COPYING README
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/%{name}

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 3.14.0-1
- Initial version imported from f21
