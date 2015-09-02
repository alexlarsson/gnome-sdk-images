%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:          zenity
Version:       3.14.0
Release:       1%{?dist}
Summary:       Display dialog boxes from shell scripts
Group:         Applications/System
License:       LGPLv2+
URL:           https://wiki.gnome.org/Projects/Zenity
Source:        https://download.gnome.org/sources/zenity/%{release_version}/zenity-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: gtk3-dev
BuildRequires: libnotify-dev
BuildRequires: itstool

%description
Zenity lets you display Gtk+ dialog boxes from the command line and through
shell scripts. It is similar to gdialog, but is intended to be saner. It comes
from the same family as dialog, Xdialog, and cdialog.

%prep
%setup -q


%build
%configure --disable-webkitgtk
make V=1 %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# we don't want a perl dependency just for this
rm $RPM_BUILD_ROOT%{_bindir}/gdialog

%find_lang zenity --with-gnome


%files -f zenity.lang
%doc COPYING AUTHORS NEWS THANKS README
%{_bindir}/zenity
%{_datadir}/zenity
%{_mandir}/man1/zenity.1.gz


%changelog
* Thu Nov 27 2014 Alexander Larsson <alexl@redhat.com> - 3.14.0-1
- Initial version, based on F21
