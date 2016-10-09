Summary:	Shared library build of Chromium’s Content module
Name:		libchromiumcontent
Version:	47.0.2526.110
Release:	0.1
License:	MIT
Group:		Libraries
Source0:	https://build.opensuse.org/source/home:MargueriteSu:branches:devel:languages:nodejs/libchromiumcontent/%{name}-%{version}.tar.xz
Source1:	https://build.opensuse.org/source/home:MargueriteSu:branches:devel:languages:nodejs/libchromiumcontent/chromium-%{version}.tar.xz
Patch0:		no-download.patch
Patch1:		no-sysroot.patch
Patch2:		gcc5.patch
Patch3:		no-bitfield-width.patch
Patch4:		dist-no-zip.patch
URL:		https://github.com/atom/libchromiumcontent
BuildRequires:	GConf2-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	binutils
BuildRequires:	bison
BuildRequires:	clang
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	gperf
BuildRequires:	gtk+2-devel
BuildRequires:	heimdal-devel
BuildRequires:	libexif-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libstdc++-devel
BuildRequires:	nss-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkg-config
BuildRequires:	pulseaudio-devel
BuildRequires:	python
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xz
Conflicts:	chromium
ExclusiveArch:	%{x8664} %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define		target x64
%endif
%ifarch %{ix86}
%define		target ia32
%endif

%description
A single, shared library that includes the Chromium Content module and
all its dependencies.

%package devel
Summary:	Development files for libchromiumcontent
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for libchromiumcontent

%package static
Summary:	Static files for libchromiumcontent
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static files for libchromiumcontent

%prep
%setup -q -a1
# unpack chromium source
mkdir -p vendor/chromium
cp -a chromium-%{version} vendor/chromium/src
# use system clang
mkdir -p vendor/chromium/src/third_party/llvm-build/Release+Asserts/{bin,lib}
ln -s %{_bindir}/clang vendor/chromium/src/third_party/llvm-build/Release+Asserts/bin/clang
ln -s %{_bindir}/clang++ vendor/chromium/src/third_party/llvm-build/Release+Asserts/bin/clang++

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
script/update -t %{target}
script/build -t %{target}
script/create-dist -t %{target}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/{shared_library,static_library,src}
cp -a dist/main/shared_library/* $RPM_BUILD_ROOT%{_libdir}/%{name}/shared_library
cp -a dist/main/static_library/* $RPM_BUILD_ROOT%{_libdir}/%{name}/static_library
cp -a dist/main/src/* $RPM_BUILD_ROOT%{_libdir}/%{name}/src

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE.txt
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/shared_library
%exclude %{_libdir}/%{name}/shared_library/gen
%exclude %{_libdir}/%{name}/shared_library/*.a

%files devel
%defattr(644,root,root,755)
%{_libdir}/%{name}/src
%{_libdir}/%{name}/shared_library/gen

%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}/shared_library/*.a
%{_libdir}/%{name}/static_library
