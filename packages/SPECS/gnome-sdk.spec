Name:           gnome-sdk
Version:        0.1
Release:        1%{?dist}
Summary:        Gnome sdk
Source1:        rpm-macros

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: gnome-platform
BuildRequires: freedesktop-sdk
BuildRequires: libappstream-glib

Requires: gnome-platform
Requires: freedesktop-sdk

Requires: adwaita-icon-theme-dev
Requires: at-spi2-atk-dev
Requires: at-spi2-core-dev
Requires: atk-dev
Requires: clutter-dev
Requires: clutter-gtk-dev
Requires: cogl-dev
Requires: dbus-glib-dev
Requires: dconf-dev
Requires: enchant-dev
Requires: gdk-pixbuf2-dev
Requires: gjs-dev
Requires: gsettings-desktop-schemas-dev
Requires: gtk2-dev
Requires: gtk3-dev
Requires: gvfs-dev
Requires: json-glib-dev
Requires: libappstream-glib-dev
Requires: libappstream-glib-builder-dev
Requires: libcroco-dev
Requires: libnotify-dev
Requires: librsvg2-dev
Requires: libsecret-dev
Requires: libsoup-dev
Requires: libthai-dev
Requires: mozjs24-dev
Requires: pango-dev
Requires: vala-dev
Requires: vala-tools
Requires: vte-dev
Requires: webkitgtk4-dev
Requires: python3-cairo-dev
Requires: pygobject3-dev

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
