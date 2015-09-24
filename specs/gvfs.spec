%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Summary: Backends for the gio framework in GLib
Name: gvfs
Version: 1.26.0
Release: 1%{?dist}
License: GPLv3 and LGPLv2+ and BSD and MPLv1.1
Group: System Environment/Libraries
URL: http://www.gtk.org

Source: http://download.gnome.org/sources/gvfs/%{release_version}/gvfs-%{version}.tar.xz
BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: dbus-glib-dev

# Remove warnings from failed remote monitors that don't
# actually exist on the host
Patch0:		%{name}-remote-monitor-remove-warning.patch

# for post-install update-gio-modules and overall functionality
Requires: glib2%{?_isa}

%description
The gvfs package provides backend implementations for the gio
framework in GLib. It includes ftp, sftp, cifs.

%package dev
Summary: Development files for gvfs
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
The gvfs-dev package contains headers and other files that are
required to develop applications using gvfs.

%prep
%setup -q
%patch0 -p1 -b .remote-monitor-remove-warning

%build
%configure \
        --disable-hal \
        --disable-gdu \
        --disable-gcr \
        --disable-obexftp \
        --disable-avahi \
        --disable-documentation
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Copy *all* the monitors in case they are supported on the host
# This is a bit iffy, this info should come from the daemon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gvfs/remote-volume-monitors
cp -p monitor/*/*.monitor $RPM_BUILD_ROOT%{_datadir}/gvfs/remote-volume-monitors/

rm $RPM_BUILD_ROOT%{_libdir}/gvfs/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

# Remove daemon side stuff
rm $RPM_BUILD_ROOT%{_libdir}/gvfs/libgvfsdaemon.*
rm $RPM_BUILD_ROOT%{_libexecdir}/gvfsd*
rm $RPM_BUILD_ROOT%{_datadir}/dbus-1/services/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/gvfs/mounts
rm -rf $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

# trashlib is GPLv3, include the license
cp -p daemon/trashlib/COPYING COPYING.GPL3

%find_lang gvfs

%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%postun
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%files -f gvfs.lang
%doc AUTHORS COPYING COPYING.GPL3 NEWS README
%dir %{_datadir}/gvfs
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gvfs*
%{_libdir}/gvfs/libgvfscommon.so
%{_libdir}/gio/modules/libgioremote-volume-monitor.so
%{_libdir}/gio/modules/libgvfsdbus.so
%{_datadir}/gvfs/remote-volume-monitors/
%{_bindir}/gvfs-cat
%{_bindir}/gvfs-copy
%{_bindir}/gvfs-info
%{_bindir}/gvfs-less
%{_bindir}/gvfs-ls
%{_bindir}/gvfs-mime
%{_bindir}/gvfs-mkdir
%{_bindir}/gvfs-monitor-dir
%{_bindir}/gvfs-monitor-file
%{_bindir}/gvfs-mount
%{_bindir}/gvfs-move
%{_bindir}/gvfs-open
%{_bindir}/gvfs-rename
%{_bindir}/gvfs-rm
%{_bindir}/gvfs-save
%{_bindir}/gvfs-trash
%{_bindir}/gvfs-tree
%{_bindir}/gvfs-set-attribute

%files dev
%dir %{_includedir}/gvfs-client
%dir %{_includedir}/gvfs-client/gvfs
%{_includedir}/gvfs-client/gvfs/gvfsurimapper.h
%{_includedir}/gvfs-client/gvfs/gvfsuriutils.h


%changelog
* Tue Nov 25 2014 Alexander Larsson <alexl@redhat.com> - 1.22.2-1
- Initial version
