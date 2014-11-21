Name:           gnome-sdk-base
Version:        0.1
Release:        1%{?dist}
Summary:        Base sdk

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

# Yocto builds without the normal find-provides, we supply those provides in the gnome-sdk-base package

Provides: %(./find_prov.sh /usr)

%description
The base sdk files

%prep


%build


%install

%files
%doc

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
