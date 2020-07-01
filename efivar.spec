%define major 1

%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define libefiboot %mklibname efiboot %{major}
%define devefiboot %mklibname efiboot -d

%define minor %(echo %{version} |cut -d. -f2)

%global optflags %{optflags} -Oz

Name:		efivar
Version:	37
Release:	3
Summary:	EFI variables management tool
License:	LGPLv2.1
Group:		System/Kernel and hardware
Url:		https://github.com/rhboot/efivar
Source0:	https://github.com/rhboot/%{name}/releases/download/%{minor}/%{name}-%{version}.tar.bz2
Source1:        efivar.patches

%include %{SOURCE1}

# Source1 patches reflect a git snapshot, this is a separate fix on top
# with a gap in between
Patch100:       0001-Fix-sys-block-sysfs-parsing-for-eMMC-s.patch

BuildRequires:	efi-srpm-macros
BuildRequires:	pkgconfig(popt)
BuildRequires:	kernel-release-devel
BuildRequires:	glibc-static-devel
BuildRequires:	git-core

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

%description -n %{libname}
Shared library support for the efitools, efivar and efibootmgr.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%package -n %{libefiboot}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libefiboot}
Shared library support for the efitools, efivar and efibootmgr.

%files -n %{libefiboot}
%{_libdir}/libefiboot.so.%{major}*

#------------------------------------------------------------------

%package -n %{devname}
Summary:	The libefivar development files
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
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

%description -n %{devefiboot}
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
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

# (tpg) 2020-07-01 looks like LLD does not support --add-needed
sed -i -e 's#-Wl,--add-needed##g' src/include/defaults.mk

%build
%set_build_flags
%make_build libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}" COMPILER=%{__cc} CC=%{__cc} OPTIMIZE="%{optflags}" LDFLAGS="%{build_ldflags}" gcc_ccldflags="%{build_ldflags}" V=1 -j1

%install
%make_install libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}"
