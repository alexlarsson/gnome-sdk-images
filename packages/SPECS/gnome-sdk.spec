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
Requires: gtk2-devel
Requires: gtk3-devel
Requires: desktop-file-utils
Requires: json-glib-devel
Requires: libnotify-devel
Requires: gvfs-devel
Requires: vte-devel
Requires: librsvg2-devel
Requires: adwaita-icon-theme-devel
Requires: gtk-doc-stub
Requires: atk-devel
Requires: at-spi2-atk-devel
Requires: at-spi2-core-devel
Requires: cairo-devel
Requires: cairo-gobject-devel
Requires: dbus-devel
Requires: dbus-glib-devel
Requires: fontconfig-devel
Requires: freetype-devel
Requires: gdk-pixbuf2-devel
Requires: glib2-devel
Requires: gobject-introspection-devel
Requires: graphite2-devel
Requires: gtk3-devel
Requires: harfbuzz-devel
Requires: libcroco-devel
Requires: librsvg2-devel
Requires: libthai-devel
Requires: libX11-devel
Requires: libXau-devel
Requires: libxcb-devel
Requires: libXcomposite-devel
Requires: libXcursor-devel
Requires: libXdamage-devel
Requires: libXdmcp-devel
Requires: libXext-devel
Requires: libXfixes-devel
Requires: libXft-devel
Requires: libXi-devel
Requires: libXinerama-devel
Requires: libXrandr-devel
Requires: libXrender-devel
Requires: libXtst-devel
Requires: libXt-devel
Requires: pango-devel
Requires: pixman-devel
Requires: vala-devel
Requires: vala-tools
Requires: dconf-devel
Requires: libsoup-devel
Requires: libproxy-devel
Requires: gsettings-desktop-schemas-devel
Requires: gjs-devel mozjs24-devel
Requires: mesa-libGL-devel
Requires: mesa-libEGL-devel
Requires: libICE-devel
Requires: libXxf86vm-devel
Requires: libepoxy-devel
Requires: cogl-devel
Requires: clutter-devel
Requires: clutter-gtk-devel
Requires: pulseaudio-libs-devel
Requires: libsecret-devel
Requires: webkitgtk4-devel
Requires: libxkbcommon-devel libxkbcommon-x11-devel
Requires: libwayland-client-devel libwayland-cursor-devel mesa-libwayland-egl-devel
Requires: xkeyboard-config-devel
Requires: hunspell-devel
Requires: enchant-devel
Requires: gstreamer1-devel


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
