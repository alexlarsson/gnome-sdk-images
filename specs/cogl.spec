%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:          cogl
Version:       1.22.0
Release:       1%{?dist}
Summary:       A library for using 3D graphics hardware to draw pretty pictures

Group:         Development/Libraries
License:       LGPLv2+
URL:           http://www.clutter-project.org/
Source0:       http://download.gnome.org/sources/cogl/%{release_version}/cogl-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: cairo-dev
BuildRequires: gdk-pixbuf2-dev
BuildRequires: glib2-dev
BuildRequires: gobject-introspection-dev
BuildRequires: libXrandr-dev
BuildRequires: libXcomposite-dev
BuildRequires: libXdamage-dev
BuildRequires: libXext-dev
BuildRequires: libXfixes-dev
BuildRequires: mesa-libGL-dev
BuildRequires: mesa-libEGL-dev
BuildRequires: mesa-libgbm-dev
BuildRequires: pango-dev
BuildRequires: libwayland-server-dev
BuildRequires: libwayland-client-dev
BuildRequires: libwayland-cursor-dev
BuildRequires: mesa-libwayland-egl-dev
BuildRequires: mesa-libgbm-dev
BuildRequires: libxkbcommon-dev

%description
Cogl is a small open source library for using 3D graphics hardware to draw
pretty pictures. The API departs from the flat state machine style of
OpenGL and is designed to make it easy to write orthogonal components that
can render without stepping on each others toes.

As well aiming for a nice API, we think having a single library as opposed
to an API specification like OpenGL has a few advantages too; like being
able to paper over the inconsistencies/bugs of different OpenGL
implementations in a centralized place, not to mention the myriad of OpenGL
extensions. It also means we are in a better position to provide utility
APIs that help software developers since they only need to be implemented
once and there is no risk of inconsistency between implementations.

Having other backends, besides OpenGL, such as drm, Gallium or D3D are
options we are interested in for the future.

%package dev
Summary:       %{name} development environment
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description dev
Header files and libraries for building and developing apps with %{name}.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure \
  --enable-cairo=yes \
  --enable-cogl-pango=yes \
  --enable-gdk-pixbuf=yes \
  --enable-glx=yes \
  --disable-gtk-doc \
  --enable-introspection=yes \
  --enable-kms-egl-platform \
  --enable-wayland-egl-platform \
  --enable-wayland-egl-server \
  --enable-xlib-egl-platform

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -delete

# This gets installed by mistake
rm %{buildroot}%{_datadir}/cogl/examples-data/crate.jpg

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc COPYING NEWS README ChangeLog
%{_libdir}/libcogl*.so.20*
%{_libdir}/girepository-1.0/Cogl*.typelib

%files dev
%{_includedir}/cogl
%{_libdir}/libcogl*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Cogl*.gir

%changelog
* Thu Dec 11 2014 Alexander Larsson <alexl@redhat.com> - 1.18.2-1
- Initial version
