Name:           gnome-platform-base
Version:        0.1
Release:        1%{?dist}
Summary:        Base platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

# Yocto builds without the normal find-provides, we supply those provides in the gnome-platform-base package
Provides: %(./find_prov.sh /self/gnome-platform/usr)

%description
The base platform files

%prep


%build


%install

%files

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
