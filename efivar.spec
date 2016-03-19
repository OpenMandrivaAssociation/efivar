%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define libefiboot %mklibname efiboot %{major}
%define devefiboot %mklibname efiboot -d

Name:		efivar
Version:	0.23
Release:	1
Summary:	EFI variables management tool
License:	LGPLv2.1
Group:		System/Kernel and hardware
Url:		https://github.com/vathpela/efivar
Source0:	https://github.com/vathpela/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	pkgconfig(popt)
BuildRequires:	kernel-devel-latest

%description
efivar is a command line interface to the EFI variables in '/sys/firmware/efi'.

%files
%doc COPYING README.md TODO
%{_bindir}/efivar
%{_mandir}/man1/*

#------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n	%{libname}
Shared library support for the efitools, efivar and efibootmgr.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%package -n %{libefiboot}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n	%{libefiboot}
Shared library support for the efitools, efivar and efibootmgr.

%files -n %{libefiboot}
%{_libdir}/libefiboot.so.%{major}*

#------------------------------------------------------------------

%package -n %{devname}
Summary:	libefivar development files
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
Development files for libefivar.

%files -n %{devname}
%{_includedir}/efivar/efivar-dp.h
%{_includedir}/efivar/efivar-guids.h
%{_includedir}/efivar/efivar.h
%{_libdir}/libefivar.so
%{_libdir}/pkgconfig/efivar.pc
%{_mandir}/man3/*

%package -n %{devefiboot}
Summary:	libefiboot development files
Group:		Development/Other
Requires:	%{libefiboot} = %{EVRD}
Provides:	libefiboot-devel = %{EVRD}
Provides:	efiboot-devel = %{EVRD}

%description -n	%{devefiboot}
Development files for libefiboot.

%files -n %{devefiboot}
%{_includedir}/efivar/efiboot-creator.h
%{_includedir}/efivar/efiboot-loadopt.h
%{_includedir}/efivar/efiboot.h
%{_libdir}/libefiboot.so
%{_libdir}/pkgconfig/efiboot.pc

#------------------------------------------------------------------

%prep
%setup -q

%build
# (tpg) /usr/bin/x86_64-mandriva-linux-gnu-ld: --default-symver: unknown option
%global ldflags %ldflags -Wl,-fuse-ld=bfd
%global optflags %optflags -fno-strict-aliasing

%setup_compile_flags
# (tpg) https://github.com/rhinstaller/efivar/issues/47
export CC=gcc
%make libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}" ccldflag="%{ldflags}" V=1 -j1

%install
%makeinstall_std libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}"
