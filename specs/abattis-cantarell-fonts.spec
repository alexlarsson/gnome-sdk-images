%global actualname cantarell

%global fontname abattis-%{actualname}
%global fontconf 31-cantarell.conf

%global archivename1 Cantarell-Bold
%global archivename2 Cantarell-Regular

Name: %{fontname}-fonts
Version: 0.0.16
Release: 1%{?dist}
Summary: Cantarell, a Humanist sans-serif font family

Group: User Interface/X
License: OFL
URL: http://abattis.org/cantarell/
Source0: http://download.gnome.org/sources/%{actualname}-fonts/0.0/%{actualname}-fonts-%{version}.tar.xz

BuildArch: noarch

%description
Cantarell is a set of fonts designed by Dave Crossland.
It is a sans-serif humanist typeface family.

%prep
%setup -q -n %{actualname}-fonts-%{version}

%build

%install
install -m 0755 -d %{buildroot}%{_datadir}/fonts/abattis-cantarell
install -m 0644 -p otf/*.otf %{buildroot}%{_datadir}/fonts/abattis-cantarell
install -m 0755 -d %{buildroot}%{_sysconfdir}/fonts/conf.d \
                   %{buildroot}%{_datadir}/fontconfig/conf.avail
install -m 0644 -p fontconfig/31-cantarell.conf \
        %{buildroot}%{_datadir}/fontconfig/conf.avail
ln -s %{_datadir}/fontconfig/conf.avail/31-cantarell.conf \
        %{buildroot}%{_sysconfdir}/fonts/conf.d/31-cantarell.conf


%files
%defattr(0644,root,root,0755)
%doc COPYING NEWS README
%{_datadir}/fonts/abattis-cantarell
%{_datadir}/fontconfig/conf.avail/*
%{_sysconfdir}/fonts/conf.d/*

%changelog
* Mon Nov 24 2014 Alexander Larsson <alexl@redhat.com> - 0.0.16-1
- Add initial version
