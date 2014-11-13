%global fontname    dejavu

Name:    %{fontname}-fonts
Version: 2.34
Release: 1%{?alphatag}%{?dist}
Summary: DejaVu fonts

Group:     User Interface/X
License:   Bitstream Vera and Public Domain
URL:       http://%{name}.org/
Source0:   http://sourceforge.net/projects/dejavu/files/%{fontname}/%{version}/%{name}-ttf-%{version}.tar.bz2

BuildArch:     noarch

%description
The DejaVu font set is based on the “Bitstream Vera” fonts, release 1.10. Its\
purpose is to provide a wider range of characters, while maintaining the \
original style, using an open collaborative development process.

%prep
%setup -q -n %{name}-ttf-%{version}

%build


%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_datadir}/fonts/dejavu
install -m 0644 -p ttf/*.ttf %{buildroot}%{_datadir}/fonts/dejavu

install -m 0755 -d %{buildroot}%{_sysconfdir}/fonts/conf.d \
                   %{buildroot}%{_datadir}/fontconfig/conf.avail

cd fontconfig
for fontconf in *conf ; do
  install -m 0644 -p $fontconf %{buildroot}%{_datadir}/fontconfig/conf.avail
  ln -s %{_datadir}/fontconfig/conf.avail/$fontconf \
        %{buildroot}%{_sysconfdir}/fonts/conf.d/$fontconf
done

%clean
rm -fr %{buildroot}


%files
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS LICENSE NEWS README
%{_datadir}/fonts/dejavu
%{_datadir}/fontconfig/conf.avail/*
%{_sysconfdir}/fonts/conf.d/*

%changelog
* Thu Nov 13 2014 Alexander Larsson <alexl@redhat.com> - 2.34-1%{?dist}
- Initial version based on F21
