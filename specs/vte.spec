%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')
%global apiver 2.91

Name:           vte
Version:        0.40.0
Release:        1%{?dist}
Summary:        Terminal emulator library

License:        LGPLv2+
URL:            http://www.gnome.org/
Source0:        http://download.gnome.org/sources/vte/%{release_version}/vte-%{version}.tar.xz
Patch2:         vte-Only-show-the-cursor-on-motion-if-moved.patch

BuildRequires:  freedesktop-sdk-base
BuildRequires:  gobject-introspection-dev
BuildRequires:  gtk3-dev
BuildRequires:  vala-tools

Requires:       vte-profile

%description
VTE is a library implementing a terminal emulator widget for GTK+. VTE
is mainly used in gnome-terminal, but can also be used to embed a
console/terminal in games, editors, IDEs, etc.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%package -n     vte-profile
Summary:        Profile script for VTE terminal emulator library
License:        GPLv3+

%description -n vte-profile
The vte-profile package contains a profile.d script for the VTE terminal
emulator library.

%prep
%setup -q -n vte-%{version}
%patch2 -p1 -b .motion

%build

# We disable gnome-pty-helper as we don't want setuid binaries
CFLAGS="%optflags -fPIE -DPIE"; export CFLAGS;
CXXFLAGS="$CFLAGS"; export CXXFLAGS;
LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now -pie -lssp"; export LDFLAGS;
%configure \
        --disable-static \
        --with-gtk=3.0 \
        --libexecdir=%{_libdir}/vte-%{apiver} \
        --disable-gtk-doc \
        --disable-gnome-pty-helper \
        --enable-introspection
make %{?_smp_mflags} V=1

%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang vte-%{apiver}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f vte-%{apiver}.lang
%doc COPYING NEWS README
%{_libdir}/libvte-%{apiver}.so.0*
%{_libdir}/girepository-1.0/

%files dev
%{_bindir}/vte-%{apiver}
%{_includedir}/vte-%{apiver}/
%{_libdir}/libvte-%{apiver}.so
%{_libdir}/pkgconfig/vte-%{apiver}.pc
%{_datadir}/gir-1.0/
%doc %{_datadir}/gtk-doc/
%{_datadir}/vala/

%files -n vte-profile
%{_sysconfdir}/profile.d/vte.sh

%changelog
* Tue Nov 25 2014 Alexander Larsson <alexl@redhat.com> - 0.38.2-1
- Initial version, based on F21
