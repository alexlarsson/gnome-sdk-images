Name:           gnome-platform-base
Version:        0.1
Release:        1%{?dist}
Summary:        Base platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Source: gnomeos-contents-platform-x86_64.tar.gz

%description
The base platform files

%prep
rm -rf gnome-platform-base
mkdir -p gnome-platform-base


%build
cd gnome-platform-base
tar -xf %{SOURCE0}
mv etc usr


%install
cd gnome-platform-base
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cp -ar usr $RPM_BUILD_ROOT/



%files
%defattr(-,root,root)
/*

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
