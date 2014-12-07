%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

Name:		efivar
Version:	0.15
Release:	2
Summary:	EFI variables management tool
License:	LGPLv2.1
Group:		System/Kernel and hardware
Url:		https://github.com/vathpela/efivar
Source0:	https://github.com/vathpela/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
#Patch1:		001-fix-multi-arch-build.patch
ExclusiveArch:	%{ix86} ia64 x86_64
BuildRequires:	pkgconfig(popt)

%description
efivar is a command line interface to the EFI variables in '/sys/firmware/efi'.

%files
%doc COPYING README
%{_bindir}/efivar
%{_mandir}/man1/*


#------------------------------------------------------------------

%package -n	%{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n	%{libname}
Shared library support for the efitools, efivar and efibootmgr.

%files -n	%{libname}
%{_libdir}/lib%{name}.so.%{major}*

#------------------------------------------------------------------

%package -n	%{devname}
Summary:	libefivar development files
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
Development files for libefivar.

%files -n	%{devname}
%{_includedir}/efivar.h
%{_includedir}/efivar-guids.h
%{_libdir}/libefivar.so
%{_libdir}/pkgconfig/efivar.pc
%doc
%{_mandir}/man3/*

#------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
%setup_compile_flags
sed -i -e s'#libdir.*#libdir=%{_libdir}#' Make.defaults
#sed -i -e s'#CFLAGS.*#CFLAGS=%{optflags}#' Make.defaults

%make libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}" V=1 -j1

%install
%makeinstall_std
