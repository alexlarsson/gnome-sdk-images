%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')
%global bin_version 3.0.0

Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name: gtk3
Version: 3.15.7
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
#VCS: git:git://git.gnome.org/gtk+

Source: http://download.gnome.org/sources/gtk+/%{release_version}/gtk+-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: gnome-common
BuildRequires: atk-dev
BuildRequires: at-spi2-atk-dev
BuildRequires: glib2-dev
BuildRequires: cairo-dev
BuildRequires: cairo-gobject-dev
BuildRequires: pango-dev
BuildRequires: gdk-pixbuf2-dev
BuildRequires: libXi-dev
#BuildRequires: cups-dev
#BuildRequires: rest-dev
#BuildRequires: json-glib-dev
BuildRequires: libXrandr-dev
BuildRequires: libXrender-dev
BuildRequires: libXcursor-dev
BuildRequires: libXfixes-dev
BuildRequires: libXinerama-dev
BuildRequires: libXcomposite-dev
BuildRequires: libXdamage-dev
BuildRequires: libXi-dev
BuildRequires: gobject-introspection-dev
BuildRequires: mesa-libGL-dev
BuildRequires: mesa-libEGL-dev
BuildRequires: libepoxy-dev
#BuildRequires: colord-dev
#BuildRequires: avahi-gobject-dev
BuildRequires: mesa-libwayland-egl-dev
BuildRequires: libwayland-client-dev
BuildRequires: libwayland-cursor-dev
BuildRequires: libxkbcommon-dev

# required for icon theme apis to work
Requires: hicolor-icon-theme

# We need to prereq these so we can run gtk-query-immodules-3.0
Requires(post): glib2%{?_isa}
Requires(post): atk%{?_isa}
Requires(post): pango%{?_isa}

Requires: cairo%{?_isa}
Requires: cairo-gobject%{?_isa}
Requires: libXrandr%{?_isa}
Requires: libwayland-client%{?_isa}
Requires: libwayland-cursor%{?_isa}
Requires: mesa-libwayland-egl

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 3 of GTK+.

%package immodules
Summary: Input methods for GTK+
Group: System Environment/Libraries
Requires: gtk3%{?_isa} = %{version}-%{release}

%description immodules
The gtk3-immodules package contains standalone input methods that
are shipped as part of GTK+ 3.

%package immodule-xim
Summary: XIM support for GTK+
Group: System Environment/Libraries
Requires: gtk3%{?_isa} = %{version}-%{release}

%description immodule-xim
The gtk3-immodule-xim package contains XIM support for GTK+ 3.

%package dev
Summary: Development files for GTK+
Group: Development/Libraries
Requires: gtk3%{?_isa} = %{version}-%{release}

%description dev
This package contains the libraries and header files that are needed
for writing applications with version 3 of the GTK+ widget toolkit. If
you plan to develop applications with GTK+, consider installing the
gtk3-dev-docs package.

%package dev-docs
Summary: Developer documentation for GTK+
Group: Development/Libraries
Requires: gtk3 = %{version}-%{release}

%description dev-docs
This package contains developer documentation for version 3 of the GTK+
widget toolkit.

%prep
%setup -q -n gtk+-%{version}

%build

(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
        --enable-xkb \
        --enable-xinerama \
        --enable-xrandr \
        --enable-xfixes \
        --enable-xcomposite \
        --enable-xdamage \
        --enable-x11-backend \
        --enable-wayland-backend

#        --enable-colord \
)

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT        \
             RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk30
%find_lang gtk30-properties

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gtk-query-immodules-3.0 gtk-query-immodules-3.0-%{__isa_bits}
)

echo ".so man1/gtk-query-immodules-3.0.1" > $RPM_BUILD_ROOT%{_mandir}/man1/gtk-query-immodules-3.0-%{__isa_bits}.1

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/*/*.la

touch $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/immodules.cache

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/theming-engines

%post
/sbin/ldconfig
gtk-query-immodules-3.0-%{__isa_bits} --update-cache
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post dev
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%post immodule-xim
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gtk-query-immodules-3.0-%{__isa_bits} --update-cache
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun dev
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%postun immodule-xim
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%files -f gtk30.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gtk-query-immodules-3.0*
%{_bindir}/gtk-launch
%{_bindir}/gtk-update-icon-cache
%{_libdir}/libgtk-3.so.*
%{_libdir}/libgdk-3.so.*
%{_libdir}/libgailutil-3.so.*
%dir %{_libdir}/gtk-3.0
%dir %{_libdir}/gtk-3.0/%{bin_version}
%dir %{_datadir}/gtk-3.0
%{_libdir}/gtk-3.0/%{bin_version}/theming-engines
%dir %{_libdir}/gtk-3.0/%{bin_version}/immodules
%{_libdir}/gtk-3.0/%{bin_version}/printbackends
%{_libdir}/gtk-3.0/modules
%{_libdir}/gtk-3.0/immodules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_libdir}/girepository-1.0
%ghost %{_libdir}/gtk-3.0/%{bin_version}/immodules.cache
%{_mandir}/man1/gtk-query-immodules-3.0*
%{_mandir}/man1/gtk-launch.1.gz
%exclude %{_mandir}/man1/gtk-update-icon-cache.1.gz
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.exampleapp.gschema.xml
%{_mandir}/man1/broadwayd.1*

%files immodules
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-viqr.so
%if 0%{?with_broadway}
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-broadway.so
%endif
%config(noreplace) %{_sysconfdir}/gtk-3.0/im-multipress.conf

%files immodule-xim
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-xim.so

%files dev -f gtk30-properties.lang
%{_libdir}/lib*.so
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk3-demo
%{_bindir}/gtk3-icon-browser
%{_bindir}/gtk-encode-symbolic-svg
%{_datadir}/applications/gtk3-demo.desktop
%{_datadir}/applications/gtk3-icon-browser.desktop
%{_datadir}/applications/gtk3-widget-factory.desktop
%{_datadir}/icons/hicolor/*/apps/gtk3-demo.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory.png
%{_datadir}/icons/hicolor/*/apps/gtk3-demo-symbolic.symbolic.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory-symbolic.symbolic.png
%{_bindir}/gtk3-demo-application
%{_bindir}/gtk3-widget-factory
%{_datadir}/gtk-3.0/gtkbuilder.rng
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo.gschema.xml
%{_mandir}/man1/gtk3-demo.1*
%{_mandir}/man1/gtk3-icon-browser.1*
%{_mandir}/man1/gtk3-widget-factory.1*
%{_mandir}/man1/gtk3-demo-application.1*
%{_mandir}/man1/gtk-encode-symbolic-svg.1*

%files dev-docs
%{_datadir}/gtk-doc

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 3.14.5-1
- Initial version based on F21
