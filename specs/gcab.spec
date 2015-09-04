Name:           gcab
Version:        0.6
Release:        1%{?dist}
Summary:        Cabinet file library and tool

License:        LGPLv2+
#VCS:           git:git://git.gnome.org/gcab
URL:            http://ftp.gnome.org/pub/GNOME/sources/gcab
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gcab/%{version}/%{name}-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: vala-tools
BuildRequires: glib2-dev
BuildRequires: gobject-introspection-dev

%description
gcab is a tool to manipulate Cabinet archive.

%package -n libgcab1
Summary:        Library to create Cabinet archives

%description -n libgcab1
libgcab is a library to manipulate Cabinet archive using GIO/GObject.

%package -n libgcab1-dev
Summary:        Devopment files to create Cabinet archives
Requires:       libgcab1%{?_isa} = %{version}-%{release}
Requires:       glib2-dev
Requires:       pkgconfig

%description -n libgcab1-dev
libgcab is a library to manipulate Cabinet archive.

Libraries, includes, etc. to compile with the gcab library.

%prep
%setup -q

%build
# --enable-fast-install is needed to fix libtool "cannot relink `gcab'"
%configure --disable-silent-rules --disable-static --enable-fast-install
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%find_lang %{name}

%post -n libgcab1 -p /sbin/ldconfig
%postun -n libgcab1 -p /sbin/ldconfig

%files
%doc COPYING NEWS
%{_bindir}/gcab
%{_mandir}/man1/gcab.1*

%files -n libgcab1 -f %{name}.lang
%doc COPYING NEWS
%{_libdir}/girepository-1.0/GCab-1.0.typelib
%{_libdir}/libgcab-1.0.so.*

%files -n libgcab1-dev
%{_datadir}/gir-1.0/GCab-1.0.gir
%{_datadir}/gtk-doc/html/gcab/*
%{_datadir}/vala/vapi/libgcab-1.0.vapi
%{_includedir}/libgcab-1.0/*
%{_libdir}/libgcab-1.0.so
%{_libdir}/pkgconfig/libgcab-1.0.pc

%changelog
* Tue Sep  8 2015 Alexander Larsson <alexl@redhat.com> - 0.6-1
- Initial version
