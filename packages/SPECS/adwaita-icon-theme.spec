# Set boostrap to 1 for initial bootstrapping when gtk3 is not yet built
%global bootstrap 0

Name:           adwaita-icon-theme
Version:        3.14.1
Release:        1%{?dist}
Summary:        Adwaita icon theme

License:        LGPLv3+ or CC-BY-SA
URL:            http://www.gnome.org
Source0:        http://download.gnome.org/sources/adwaita-icon-theme/3.14/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  gnome-sdk-base
BuildRequires:  librsvg2
BuildRequires:  gtk3-devel
BuildRequires:  hicolor-icon-theme

Requires:       adwaita-cursor-theme = %{version}-%{release}

%description
This package contains the Adwaita icon theme used by the GNOME desktop.

%package -n     adwaita-cursor-theme
Summary:        Adwaita cursor theme

%description -n adwaita-cursor-theme
The adwaita-cursor-theme package contains a modern set of cursors originally
designed for the GNOME desktop.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains the pkgconfig file for
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
%if ! 0%{bootstrap}
%{_datadir}/icons/Adwaita/64x64/
%{_datadir}/icons/Adwaita/96x96/
%endif
%{_datadir}/icons/Adwaita/256x256/
%{_datadir}/icons/Adwaita/scalable/
%{_datadir}/icons/Adwaita/scalable-up-to-32/
%{_datadir}/icons/Adwaita/index.theme
%ghost %{_datadir}/icons/Adwaita/icon-theme.cache

%files -n adwaita-cursor-theme
%doc COPYING*
%{_datadir}/icons/Adwaita/cursors/

%files devel
%{_datadir}/pkgconfig/adwaita-icon-theme.pc

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 3.14.1-1
- Initial version based on F21
