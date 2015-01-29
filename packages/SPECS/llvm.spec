%bcond_without doxygen clang crt ocaml gold lldb

%global llvmdocdir() %{_docdir}/%1

#global prerel rc3

Name:           llvm
Version:        3.5.0
Release:        1%{?dist}
Summary:        The Low Level Virtual Machine

Group:          Development/Languages
License:        NCSA
URL:            http://llvm.org/

# source archives
Source0:        http://llvm.org/releases/%{version}/llvm-%{version}.src.tar.xz
#Source1:        http://llvm.org/releases/%{version}/cfe-%{version}.src.tar.xz
#Source2:        http://llvm.org/releases/%{version}/compiler-rt-%{version}.src.tar.xz
#Source3:        http://llvm.org/releases/%{version}/lldb-%{version}.src.tar.xz

# patches
Patch1:         llvm-3.5.0-build-fix.patch

BuildRequires: gnome-sdk-base
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
LLVM is a compiler infrastructure designed for compile-time,
link-time, runtime, and idle-time optimization of programs from
arbitrary programming languages.  The compiler infrastructure includes
mirror sets of programming tools as well as libraries with equivalent
functionality.

%package dev
Summary:        Libraries and header files for LLVM
Group:          Development/Languages
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description dev
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.


%package doc
Summary:        Documentation for LLVM
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for the LLVM compiler infrastructure.

%package libs
Summary:        LLVM shared libraries
Group:          System Environment/Libraries

%description libs
Shared libraries for the LLVM compiler infrastructure.

%package static
Summary:        LLVM static libraries
Group:          Development/Languages
Requires:       %{name}-dev%{?_isa} = %{version}-%{release}

%description static
Static libraries for the LLVM compiler infrastructure.  Not recommended
for general consumption.

%prep
%setup -q -n llvm-%{version}.src
rm -rf tools/clang tools/lldb projects/compiler-rt

%patch1 -p1

# fix library paths
sed -i 's|/lib /usr/lib $lt_ld_extra|%{_libdir} $lt_ld_extra|' configure
sed -i 's|(PROJ_prefix)/lib|(PROJ_prefix)/%{_lib}/%{name}|g' Makefile.config.in
sed -i 's|/lib\>|/%{_lib}/%{name}|g' tools/llvm-config/llvm-config.cpp

%build

# clang is lovely and all, but fedora builds with gcc
# -fno-devirtualize shouldn't be necessary, but gcc has scary template-related
# bugs that make it so.  gcc 5 ought to be fixed.
export CC=gcc
export CXX=g++
%configure \
  --with-extra-options="-fno-devirtualize" \
  --with-extra-ld-options=-Wl,-Bsymbolic \
  --libdir=%{_libdir}/%{name} \
  --disable-polly \
  --disable-libcpp \
  --enable-cxx11 \
  --enable-clang-arcmt \
  --enable-clang-static-analyzer \
  --enable-clang-rewriter \
  --enable-optimized \
  --disable-profiling \
  --disable-assertions \
  --disable-werror \
  --disable-expensive-checks \
  --enable-debug-runtime \
  --enable-keep-symbols \
  --enable-jit \
  --enable-docs \
  --disable-doxygen \
  --enable-threads \
  --enable-pthreads \
  --enable-zlib \
  --enable-pic \
  --enable-shared \
  --disable-embed-stdcxx \
  --enable-timestamps \
  --enable-backtraces \
  --enable-targets=x86,powerpc,arm,aarch64,cpp,nvptx,systemz,r600 \
  --enable-bindings=none \
  --enable-libffi \
  --enable-ltdl-install \
  \
  --with-c-include-dirs=%{_includedir}:$(echo %{_prefix}/lib/gcc/%{_target_cpu}*/*/include) \
  --with-optimize-option=-O3

make %{?_smp_mflags} REQUIRES_RTTI=1 VERBOSE=1
#make REQUIRES_RTTI=1 VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=%{buildroot} PROJ_docsdir=/moredocs

# you have got to be kidding me
rm -f %{buildroot}%{_bindir}/{FileCheck,count,not}

# Create ld.so.conf.d entry
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf << EOF
%{_libdir}/%{name}
EOF

# Get rid of erroneously installed example files.
rm %{buildroot}%{_libdir}/%{name}/*LLVMHello.*

# remove executable bit from static libraries
find %{buildroot}%{_libdir} -name "*.a" -type f -print0 | xargs -0 chmod -x

# Install documentation documentation
find %{buildroot}/moredocs/ -name "*.tar.gz" -print0 | xargs -0 rm -rf
mkdir -p %{buildroot}%{_docdir}

# llvm-doc
mkdir -p %{buildroot}%{llvmdocdir %{name}-doc}
cp -ar examples %{buildroot}%{llvmdocdir %{name}-doc}/examples
find %{buildroot}%{llvmdocdir %{name}-doc} -name Makefile -o -name CMakeLists.txt -o -name LLVMBuild.txt -print0 | xargs -0 rm -f

# delete the rest of installed documentation (because it's bad)
rm -rf %{buildroot}/moredocs

# install CMake modules
mkdir -p %{buildroot}%{_datadir}/llvm/cmake/
cp -p cmake/modules/*.cmake %{buildroot}%{_datadir}/llvm/cmake/

# remove RPATHs
file %{buildroot}/%{_bindir}/* | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
file %{buildroot}/%{_libdir}/%{name}/*.so | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d

%check
# the Koji build server does not seem to have enough RAM
# for the default 16 threads

# the || : is wrong, i know, but the git snaps fail to make check due to
# broken makefiles in the doc dirs.

# LLVM test suite failing on ARM, PPC64 and s390(x)
mkdir -p %{buildroot}%{llvmdocdir %{name}-dev}
make -k check LIT_ARGS="-v -j4" | tee %{buildroot}%{llvmdocdir %{name}-dev}/testlog-%{_arch}.txt || :


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%doc CREDITS.TXT
%doc README.txt
%dir %{_datadir}/llvm
%{_bindir}/bugpoint
%{_bindir}/llc
%{_bindir}/lli
%{_bindir}/lli-child-target
%exclude %{_bindir}/llvm-config
%{_bindir}/llvm*
%{_bindir}/macho-dump
%{_bindir}/opt

%files dev
%doc %{llvmdocdir %{name}-dev}/
%{_bindir}/llvm-config
%{_includedir}/%{name}
%{_includedir}/%{name}-c
%{_datadir}/llvm/cmake

%files libs
%doc LICENSE.TXT
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so

%files static
%{_libdir}/%{name}/*.a

%files doc
%doc %{llvmdocdir %{name}-doc}/

%changelog
* Thu Jan 22 2015 Alexander Larsson <alexl@redhat.com> - 3.5.0-1
- Initial version
