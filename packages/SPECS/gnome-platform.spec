Name:           gnome-platform
Version:        0.1
Release:        1%{?dist}
Summary:        Gnome platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: freedesktop-platform

BuildRequires: abattis-cantarell-fonts
BuildRequires: adwaita-icon-theme
BuildRequires: clutter-gtk-dev
BuildRequires: dbus-glib
BuildRequires: dconf-dev
BuildRequires: dejavu-fonts
BuildRequires: enchant-dev
BuildRequires: gjs-dev
BuildRequires: gnome-themes-standard
BuildRequires: gtk2
BuildRequires: gtk3
BuildRequires: gvfs
BuildRequires: hicolor-icon-theme
BuildRequires: json-glib
BuildRequires: libnotify-dev
BuildRequires: librsvg2
BuildRequires: libsecret-dev
BuildRequires: libsoup
BuildRequires: pygobject3
BuildRequires: vte-dev
BuildRequires: webkitgtk4-dev
BuildRequires: zenity

Requires: freedesktop-platform

# We really only provide python3, but the auto-requires picks up
# a python requirement. This is a hacky workaround for that.
Provides: python

Requires: abattis-cantarell-fonts
Requires: adwaita-icon-theme
Requires: clutter
Requires: clutter-gtk
Requires: dbus-glib
Requires: dconf
Requires: dejavu-fonts
Requires: enchant
Requires: gjs
Requires: gnome-themes-standard
Requires: gsettings-desktop-schemas
Requires: gtk2
Requires: gtk2-immodules
Requires: gtk3
Requires: gtk3-immodules
Requires: gvfs
Requires: json-glib
Requires: libnotify
Requires: librsvg2
Requires: libsecret
Requires: libsoup
Requires: pygobject3
Requires: vte
Requires: webkitgtk4
Requires: zenity

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
