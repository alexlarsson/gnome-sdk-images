%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name: gnome-themes-standard
Version: 3.15.90
Release: 1%{?dist}
Summary: Standard themes for GNOME applications

Group: User Interface/Desktops
License: LGPLv2+
URL: http://git.gnome.org/browse/gnome-themes-standard
Source0: http://download.gnome.org/sources/%{name}/%{release_version}/%{name}-%{version}.tar.xz
Source2: gtkrc

BuildRequires: freedesktop-sdk-base
BuildRequires: gtk2-dev
BuildRequires: gtk3-dev
BuildRequires: librsvg2-dev
Requires: abattis-cantarell-fonts
Requires: adwaita-gtk2-theme = %{version}-%{release}
Requires: adwaita-icon-theme

%description
The gnome-themes-standard package contains the standard theme for the GNOME
desktop, which provides default appearance for cursors, desktop background,
window borders and GTK+ applications.

%package -n adwaita-gtk2-theme
Summary: Adwaita gtk2 theme
Group: User Interface/Desktops
Requires: gtk2%{_isa} >= %{gtk2_version}

%description -n adwaita-gtk2-theme
The adwaita-gtk2-theme package contains a gtk2 theme for presenting widgets
with a GNOME look and feel.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

for t in HighContrast; do
  rm -f $RPM_BUILD_ROOT%{_datadir}/icons/$t/icon-theme.cache
  touch $RPM_BUILD_ROOT%{_datadir}/icons/$t/icon-theme.cache
done

rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.la

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-2.0
cp $RPM_SOURCE_DIR/gtkrc $RPM_BUILD_ROOT%{_datadir}/gtk-2.0/gtkrc

%post
for t in HighContrast; do
  touch --no-create %{_datadir}/icons/$t &>/dev/null || :
done

%posttrans
for t in HighContrast; do
  gtk-update-icon-cache %{_datadir}/icons/$t &>/dev/null || :
done

%files
%doc COPYING NEWS

# Background and WM
%{_datadir}/themes/Adwaita
%exclude %{_datadir}/themes/Adwaita/gtk-2.0

# A11y themes
%ghost %{_datadir}/icons/HighContrast/icon-theme.cache
%{_datadir}/icons/HighContrast
%{_datadir}/themes/HighContrast

%files -n adwaita-gtk2-theme
# gtk2 Theme and engine
%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.so
%{_datadir}/themes/Adwaita/gtk-2.0
# Default gtk2 settings
%{_datadir}/gtk-2.0/gtkrc

%changelog
* Fri Nov 21 2014 Alexander Larsson <alexl@redhat.com> - 3.14.2-1
- Initial version, based on F21

