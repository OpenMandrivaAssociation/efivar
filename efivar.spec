%define major 1

%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define libefiboot %mklibname efiboot %{major}
%define devefiboot %mklibname efiboot -d

%define minor %(echo %{version} |cut -d. -f2)

Name:		efivar
Version:	37
Release:	1
Summary:	EFI variables management tool
License:	LGPLv2.1
Group:		System/Kernel and hardware
Url:		https://github.com/rhinstaller/efivar
Source0:	https://github.com/rhinstaller/%{name}/releases/download/%{minor}/%{name}-%{version}.tar.bz2
Patch0:		workaround-for-bug64.patch
BuildRequires:	pkgconfig(popt)
BuildRequires:	kernel-release-devel-latest
BuildRequires:	glibc-static-devel

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
Summary:	The libefivar development files
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
Summary:	The libefiboot development files
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
%autosetup -p1

%build
%setup_compile_flags
%make_build libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}" CFLAGS="%{optflags}" LDFLAGS="%{ldflags}" gcc_ccldflags="%{ldflags}" V=1 -j1

%install
%make_install libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}"
