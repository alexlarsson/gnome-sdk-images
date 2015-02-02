Name:           freedesktop-platform
Version:        0.1
Release:        1%{?dist}
Summary:        Freedesktop platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: freedesktop-platform-base

BuildRequires: dbus-libs
BuildRequires: dejavu-fonts
BuildRequires: desktop-file-utils
BuildRequires: glib2
BuildRequires: gstreamer1
BuildRequires: hicolor-icon-theme
BuildRequires: libICE-dev
BuildRequires: libXv
BuildRequires: libXxf86vm-dev
BuildRequires: libepoxy-dev
BuildRequires: libproxy
BuildRequires: mesa-libGL
BuildRequires: pulseaudio-libs-dev
BuildRequires: xkeyboard-config-dev
BuildRequires: gobject-introspection

Requires: freedesktop-platform-base

Requires: abattis-cantarell-fonts
Requires: cairo
Requires: cairo-gobject
Requires: dbus
Requires: dbus-libs
Requires: dejavu-fonts
Requires: desktop-file-utils
Requires: fontconfig
Requires: glib2
Requires: gobject-introspection
Requires: graphite2
Requires: gstreamer1
Requires: harfbuzz
Requires: harfbuzz-icu
Requires: hicolor-icon-theme
Requires: hunspell
Requires: hunspell-en
Requires: libICE
Requires: libSM
Requires: libX11
Requires: libXau
Requires: libXcomposite
Requires: libXcursor
Requires: libXdamage
Requires: libXext
Requires: libXfixes
Requires: libXft
Requires: libXi
Requires: libXinerama
Requires: libXrandr
Requires: libXrender
Requires: libXt
Requires: libXtst
Requires: libXv
Requires: libXxf86vm
Requires: libepoxy
Requires: libproxy
Requires: libwayland-client
Requires: libwayland-cursor
Requires: libwayland-server
Requires: libxcb
Requires: libxkbcommon
Requires: libxkbcommon-x11
Requires: libxshmfence
Requires: mesa-dri-drivers
Requires: mesa-libEGL
Requires: mesa-libGL
Requires: mesa-libwayland-egl
Requires: pulseaudio-libs
Requires: pulseaudio-libs-glib2
Requires: shared-mime-info
Requires: xkeyboard-config

%description
Meta package for Freedesktop platform dependencies

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
