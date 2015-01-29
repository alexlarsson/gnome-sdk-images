Name:           gnome-sdk
Version:        0.1
Release:        1%{?dist}
Summary:        Gnome sdk
Source1:        rpm-macros

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: gnome-platform

Requires: gnome-platform
Requires: gtk2-dev
Requires: gtk3-dev
Requires: desktop-file-utils
Requires: json-glib-dev
Requires: libnotify-dev
Requires: gvfs-dev
Requires: vte-dev
Requires: librsvg2-dev
Requires: adwaita-icon-theme-dev
Requires: gtk-doc-stub
Requires: atk-dev
Requires: at-spi2-atk-dev
Requires: at-spi2-core-dev
Requires: cairo-dev
Requires: cairo-gobject-dev
Requires: dbus-dev
Requires: dbus-glib-dev
Requires: fontconfig-dev
Requires: freetype-dev
Requires: gdk-pixbuf2-dev
Requires: glib2-dev
Requires: gobject-introspection-dev
Requires: graphite2-dev
Requires: gtk3-dev
Requires: harfbuzz-dev
Requires: libcroco-dev
Requires: librsvg2-dev
Requires: libthai-dev
Requires: libX11-dev
Requires: libXau-dev
Requires: libxcb-dev
Requires: libXcomposite-dev
Requires: libXcursor-dev
Requires: libXdamage-dev
Requires: libXdmcp-dev
Requires: libXext-dev
Requires: libXfixes-dev
Requires: libXft-dev
Requires: libXi-dev
Requires: libXinerama-dev
Requires: libXrandr-dev
Requires: libXrender-dev
Requires: libXtst-dev
Requires: libXt-dev
Requires: libXv-dev
Requires: pango-dev
Requires: pixman-dev
Requires: vala-dev
Requires: vala-tools
Requires: dconf-dev
Requires: libsoup-dev
Requires: libproxy-dev
Requires: gsettings-desktop-schemas-dev
Requires: gjs-dev mozjs24-dev
Requires: mesa-libGL-dev
Requires: mesa-libEGL-dev
Requires: libICE-dev
Requires: libXxf86vm-dev
Requires: libepoxy-dev
Requires: cogl-dev
Requires: clutter-dev
Requires: clutter-gtk-dev
Requires: pulseaudio-libs-dev
Requires: libsecret-dev
Requires: webkitgtk4-dev
Requires: libxkbcommon-dev libxkbcommon-x11-dev
Requires: libwayland-client-dev libwayland-cursor-dev mesa-libwayland-egl-dev
Requires: xkeyboard-config-dev
Requires: xorg-x11-util-macros
Requires: hunspell-dev
Requires: enchant-dev
Requires: gstreamer1-dev


%description
Meta package for Gnome SDK dependencies

%prep


%build


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros

%files
%doc
%{_sysconfdir}/rpm/macros

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
