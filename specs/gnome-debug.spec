Name:           gnome-debug
Version:        3.18
Release:        1%{?dist}
Summary:        Gnome sdk debug info

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: freedesktop-sdk
BuildRequires: freedesktop-debug

Requires: freedesktop-debug
Requires: gtk3-debuginfo
Requires: gvfs-debuginfo

%description
Meta package for debug info

%prep


%build


%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/debug

%files
%doc
%{_libdir}/debug

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
