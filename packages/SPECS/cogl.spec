Name:          cogl
Version:       1.18.2
Release:       1%{?dist}
Summary:       A library for using 3D graphics hardware to draw pretty pictures

Group:         Development/Libraries
License:       LGPLv2+
URL:           http://www.clutter-project.org/
Source0:       http://download.gnome.org/sources/cogl/1.18/cogl-%{version}.tar.xz

BuildRequires: gnome-sdk-base
BuildRequires: cairo-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: libXrandr-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: pango-devel

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

%package devel
Summary:       %{name} development environment
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
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

%files devel
%{_includedir}/cogl
%{_libdir}/libcogl*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Cogl*.gir

%changelog
* Thu Dec 11 2014 Alexander Larsson <alexl@redhat.com> - 1.18.2-1
- Initial version
