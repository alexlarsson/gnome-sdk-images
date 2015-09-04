Name: python3-cairo
Version: 1.10.0
Release: 1%{?dist}
License: MPLv1.1 or LGPLv2
Group: Development/Languages
Summary: Python 3 bindings for the cairo library
URL: http://cairographics.org/pycairo

Source: http://cairographics.org/releases/pycairo-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: cairo-dev

%description
Python 3 bindings for the cairo library.

%package dev
Summary: Libraries and headers for python3-cairo
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: cairo-dev

%description dev
This package contains files required to build wrappers for cairo add-on
libraries so that they interoperate with python3-cairo.

%prep
%setup -q -n pycairo-%{version}

python3 ./waf --version

sed -i "s|='-O'|='-q'|g" .waf*/waflib/Tools/python.py


%build
# FIXME: we should be using the system version of waf (e.g. %{_bindir}/waf)
export CFLAGS="$RPM_OPT_FLAGS"
export PYTHON=/usr/bin/python3

python3 ./waf --prefix=%{_usr} \
              --libdir=%{_libdir} \
              configure

# do not fail on utf-8 encoded files
LANG=en_US.utf8 python3 ./waf build -v

# remove executable bits from examples
find ./examples/ -type f -print0 | xargs -0 chmod -x

%install

DESTDIR=$RPM_BUILD_ROOT python3 ./waf install -v
# add executable bit to the .so libraries so we strip the debug info
find $RPM_BUILD_ROOT -name '*.so' | xargs chmod +x

find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f

%files
%doc AUTHORS COPYING* NEWS README
%doc examples doc/faq.rst doc/overview.rst doc/README
%{_libdir}/python3.*/site-packages/cairo/

%files dev
%{_includedir}/pycairo/py3cairo.h
%{_libdir}/pkgconfig/py3cairo.pc

%changelog
* Tue Feb  3 2015 Alexander Larsson <alexl@redhat.com> - 1.10.0-1
- initial version
