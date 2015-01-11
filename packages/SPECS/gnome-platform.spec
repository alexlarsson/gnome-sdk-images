Name:           gnome-platform
Version:        0.1
Release:        1%{?dist}
Summary:        Gnome platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: gnome-sdk

Requires: gnome-platform-base
Requires: gtk2 gtk2-immodules
Requires: gtk3 gtk3-immodules
Requires: hicolor-icon-theme
Requires: adwaita-icon-theme
Requires: gnome-themes-standard
Requires: dejavu-fonts
Requires: abattis-cantarell-fonts
Requires: dbus-libs
Requires: librsvg2
Requires: dbus-glib
Requires: gobject-introspection
Requires: gtk2 gnome-themes-standard
Requires: dconf libsoup
Requires: gsettings-desktop-schemas
Requires: gvfs
Requires: desktop-file-utils
Requires: json-glib
Requires: libnotify
Requires: vte
Requires: gjs
Requires: zenity
Requires: libXt
Requires: mesa-libGL
Requires: mesa-libEGL
Requires: mesa-dri-drivers
Requires: libepoxy
Requires: clutter
Requires: clutter-gtk
Requires: pulseaudio-libs-glib2
Requires: libsecret
Requires: webkitgtk4

%description
Meta package for Gnome SDK dependencies

%prep


%build

%install
rm -rf $RPM_BUILD_ROOT

# Need empty machine-id to bind mount over
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/
touch $RPM_BUILD_ROOT%{_sysconfdir}/machine-id

%files
%doc
%{_sysconfdir}/machine-id

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
