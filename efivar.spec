%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%bcond_with	uclibc

Name:		efivar
Version:	0.15
Release:	6
Summary:	EFI variables management tool
License:	LGPLv2.1
Group:		System/Kernel and hardware
Url:		https://github.com/vathpela/efivar
Source0:	https://github.com/vathpela/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

Patch0:		efivar-0.15-increase-buffer-size.patch
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	pkgconfig(popt)
%if %{with uclibc}
BuildRequires:	uClibc-devel
BuildRequires:	uclibc-popt-devel
%endif

%description
efivar is a command line interface to the EFI variables in '/sys/firmware/efi'.

%files
%doc COPYING README
%{_bindir}/efivar
%{_mandir}/man1/*

%if %{with uclibc}
%package -n	uclibc-%{name}
Summary:	EFI variables management tool (uClibc build)
Group:		System/Kernel and hardware

%description -n	uclibc-%{name}
efivar is a command line interface to the EFI variables in '/sys/firmware/efi'.

%files -n	uclibc-%{name}
%{uclibc_root}%{_bindir}/efivar
%endif

#------------------------------------------------------------------

%package -n	%{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n	%{libname}
Shared library support for the efitools, efivar and efibootmgr.

%files -n	%{libname}
%{_libdir}/lib%{name}.so.%{major}*

%if %{with uclibc}
%package -n	uclibc-%{libname}
Summary:	Shared library for %{name} (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
Shared library support for the efitools, efivar and efibootmgr.

%files -n	uclibc-%{libname}
%{uclibc_root}%{_libdir}/lib%{name}.so.%{major}*

%package -n	uclibc-%{devname}
Summary:	libefivar development files
Group:		Development/Other
Requires:	%{devname} = %{EVRD}
Requires:	uclibc-%{libname} = %{EVRD}
Provides:	uclibc-%{name}-devel = %{EVRD}
Conflicts:	%{devname} < 0.15-4

%description -n	uclibc-%{devname}
Development files for libefivar.

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/libefivar.so
%endif

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
%if %{with uclibc}
mkdir .uclibc
cp -a * .uclibc
%endif

%build
%setup_compile_flags
export CC=gcc

%make libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}" V=1 -j1

%if %{with uclibc}
pushd .uclibc
export CC=%{uclibc_cc}
export CFLAGS="%{uclibc_cflags}"
%make libdir="%{uclibc_root}%{_libdir}" bindir="%{uclibc_root}%{_bindir}" mandir="%{_mandir}" V=1 -j1
popd
%endif

%install
%makeinstall_std libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}"
%if %{with uclibc}
%makeinstall_std -C .uclibc libdir="%{uclibc_root}%{_libdir}" bindir="%{uclibc_root}%{_bindir}" mandir="%{_mandir}"
rm %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig/efivar.pc

%endif
