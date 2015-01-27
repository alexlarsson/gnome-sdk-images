Name:           gnome-platform
Version:        0.1
Release:        1%{?dist}
Summary:        Gnome platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: gnome-sdk-base
BuildRequires: gtk2
BuildRequires: gtk3 gtk3-immodules
BuildRequires: hicolor-icon-theme
BuildRequires: adwaita-icon-theme
BuildRequires: gnome-themes-standard
BuildRequires: dejavu-fonts
BuildRequires: abattis-cantarell-fonts
BuildRequires: dbus-libs
BuildRequires: librsvg2
BuildRequires: dbus-glib
BuildRequires: gobject-introspection
BuildRequires: libsoup
BuildRequires: gvfs
BuildRequires: desktop-file-utils
BuildRequires: json-glib
BuildRequires: libnotify-devel
BuildRequires: vte-devel
BuildRequires: gjs-devel
BuildRequires: zenity
BuildRequires: mesa-libGL
BuildRequires: libICE-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libepoxy-devel
BuildRequires: clutter-gtk-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: dconf-devel
BuildRequires: libsecret-devel
BuildRequires: webkitgtk4-devel
BuildRequires: xkeyboard-config-devel
BuildRequires: enchant-devel
BuildRequires: gstreamer1

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
Requires: libXv
Requires: mesa-libGL
Requires: mesa-libEGL
Requires: mesa-libwayland-egl
Requires: mesa-dri-drivers
Requires: libepoxy
Requires: clutter
Requires: clutter-gtk
Requires: pulseaudio-libs-glib2
Requires: libsecret
Requires: webkitgtk4
Requires: xkeyboard-config
Requires: libxkbcommon libxkbcommon-x11 libwayland-cursor
Requires: enchant
Requires: gstreamer1


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
