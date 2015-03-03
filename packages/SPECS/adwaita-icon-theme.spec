%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           adwaita-icon-theme
Version:        3.15.90
Release:        1%{?dist}
Summary:        Adwaita icon theme

License:        LGPLv3+ or CC-BY-SA
URL:            http://www.gnome.org
Source0:        http://download.gnome.org/sources/adwaita-icon-theme/%{release_version}/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  freedesktop-sdk-base
BuildRequires:  librsvg2
BuildRequires:  gtk3-dev
BuildRequires:  hicolor-icon-theme

Requires:       adwaita-cursor-theme = %{version}-%{release}

%description
This package contains the Adwaita icon theme used by the GNOME desktop.

%package -n     adwaita-cursor-theme
Summary:        Adwaita cursor theme

%description -n adwaita-cursor-theme
The adwaita-cursor-theme package contains a modern set of cursors originally
designed for the GNOME desktop.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    dev
The %{name}-dev package contains the pkgconfig file for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install

touch $RPM_BUILD_ROOT%{_datadir}/icons/Adwaita/icon-theme.cache

%post
touch --no-create %{_datadir}/icons/Adwaita &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/Adwaita &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/Adwaita &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/Adwaita &>/dev/null || :

%files
%doc COPYING*
%{_datadir}/icons/Adwaita/8x8/
%{_datadir}/icons/Adwaita/16x16/
%{_datadir}/icons/Adwaita/22x22/
%{_datadir}/icons/Adwaita/24x24/
%{_datadir}/icons/Adwaita/32x32/
%{_datadir}/icons/Adwaita/48x48/
%{_datadir}/icons/Adwaita/64x64/
%{_datadir}/icons/Adwaita/96x96/
%{_datadir}/icons/Adwaita/256x256/
%{_datadir}/icons/Adwaita/scalable/
%{_datadir}/icons/Adwaita/scalable-up-to-32/
%{_datadir}/icons/Adwaita/index.theme
%ghost %{_datadir}/icons/Adwaita/icon-theme.cache

%files -n adwaita-cursor-theme
%doc COPYING*
%{_datadir}/icons/Adwaita/cursors/

%files dev
%{_datadir}/pkgconfig/adwaita-icon-theme.pc

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 3.14.1-1
- Initial version based on F21
