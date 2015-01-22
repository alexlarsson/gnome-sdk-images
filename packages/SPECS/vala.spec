%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')
%global api_ver 0.28

Name:           vala
Version:        0.27.1
Release:        1%{?dist}
Summary:        A modern programming language for GNOME

# Most files are LGPLv2.1+, curses.vapi is 2-clause BSD
License:        LGPLv2+ and BSD
URL:            http://live.gnome.org/Vala
#VCS:           git:git://git.gnome.org/vala
Source0:        http://download.gnome.org/sources/vala/%{release_version}/vala-%{version}.tar.xz

BuildRequires:  gnome-sdk-base
BuildRequires:  glib2-devel

%description
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

valac, the Vala compiler, is a self-hosting compiler that translates
Vala source code into C source and header files. It uses the GObject
type system to create classes and interfaces declared in the Vala source
code. It's also planned to generate GIDL files when gobject-
introspection is ready.

The syntax of Vala is similar to C#, modified to better fit the GObject
type system.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains development files for %{name}. This is not
necessary for using the %{name} compiler.


%package        tools
Summary:        Tools for creating projects and bindings for %{name}
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gnome-common
Requires:       gobject-introspection-devel

%description    tools
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains tools to generate Vala projects, as well as API
bindings from existing C libraries, allowing access from Vala programs.


%package        doc
Summary:        Documentation for %{name}
License:        LGPLv2+

BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains documentation in a devhelp HTML book.

%prep
%setup -q


%build
%configure --enable-unversioned
# Don't use rpath!
sed -i 's|/lib /usr/lib|/lib /usr/lib /lib64 /usr/lib64|' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# own this directory for third-party *.vapi files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vala/vapi
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%posttrans
/sbin/ldconfig

%preun
/sbin/ldconfig

%files
%doc AUTHORS COPYING MAINTAINERS NEWS README THANKS
%{_bindir}/vala
%{_bindir}/valac
%{_bindir}/vala-%{api_ver}
%{_bindir}/valac-%{api_ver}
# owning only the directories, they should be empty
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala-%{api_ver}
%{_libdir}/libvala-%{api_ver}.so.*
%{_mandir}/man1/valac-%{api_ver}.1.gz
%{_mandir}/man1/valac.1.gz

%files devel
%{_includedir}/vala-%{api_ver}
%{_libdir}/libvala-%{api_ver}.so
%{_libdir}/pkgconfig/libvala-%{api_ver}.pc
# directory owned by filesystem
%{_datadir}/aclocal/vala.m4

%files tools
%{_bindir}/vala-gen-introspect
%{_bindir}/vapicheck
%{_bindir}/vapigen
%{_bindir}/vala-gen-introspect-%{api_ver}
%{_bindir}/vapicheck-%{api_ver}
%{_bindir}/vapigen-%{api_ver}
%{_libdir}/vala-%{api_ver}
%{_datadir}/aclocal/vapigen.m4
%{_datadir}/pkgconfig/vapigen*.pc
%{_datadir}/vala/Makefile.vapigen
%{_mandir}/man1/vala-gen-introspect.1.gz
%{_mandir}/man1/vapigen.1.gz
%{_mandir}/man1/vala-gen-introspect-%{api_ver}.1.gz
%{_mandir}/man1/vapigen-%{api_ver}.1.gz

%files doc
%doc %{_datadir}/devhelp/books/vala-%{api_ver}

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 0.26.1-1
- Initial version based on F21
