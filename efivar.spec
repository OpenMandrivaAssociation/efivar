%define major 1

%define oldlibname %mklibname %{name} 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%define minor %(echo %{version} |cut -d. -f2)

%global optflags %{optflags} -Oz

Summary:	EFI variables management tool
Name:		efivar
Version:	38
Release:	5
License:	LGPLv2.1
Group:		System/Kernel and hardware
Url:		https://github.com/rhboot/efivar
Source0:	https://github.com/rhboot/%{name}/releases/download/%{minor}/%{name}-%{version}.tar.bz2
Patch0:		0000-Add-T-workaround-for-GNU-ld-2.36.patch
Patch1:		0001-Add-extern-C-to-headers-for-easier-use-by-C.patch
Patch2:		0002-Avoid-format-error-on-i686.patch
Patch3:		0003-Fix-the-march-issue-for-riscv64.patch
Patch4:		0004-efisecdb-fix-build-with-musl-libc.patch
Patch5:		0005-efisecdb-do-not-free-optarg.patch
Patch6:		0006-Fix-invalid-free-in-main.patch
Patch7:		0007-Remove-deprecated-add-needed-linker-flag.patch
Patch8:		0008-src-Makefile-build-util.c-separately-for-makeguids.patch
Patch9:		0009-Adjust-dependency-for-libefivar-and-libefiboot-objec.patch
Patch10:	0010-Set-LC_ALL-C-to-force-English-output-from-ld.patch
Patch11:	https://github.com/rhboot/efivar/commit/1f247260c9b4bd6fcda30f3e4cc358852aeb9e4d.patch
Patch12:	https://patch-diff.githubusercontent.com/raw/rhboot/efivar/pull/235.patch
Patch13:	https://github.com/rhboot/efivar/commit/bc65d63ebf8fe6ac8a099ff15ca200986dba1565.patch
Patch101:	http://svnweb.mageia.org/packages/cauldron/efivar/current/SOURCES/0001-Mageia-does-not-have-mandoc.patch
Patch102:	efivar-38-fix-underlinking.patch
BuildRequires:	efi-srpm-macros
BuildRequires:	pkgconfig(popt)
BuildRequires:	kernel-devel
BuildRequires:	glibc-static-devel
ExclusiveArch:	%{efi}

%description
efivar is a command line interface to the EFI variables in '/sys/firmware/efi'.

%files
%doc COPYING README.md TODO
%{_bindir}/*
%doc %{_mandir}/man1/*

#------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}efiboot1 < 38-2
%rename %{_lib}efiboot1
%rename %{oldlibname}

%description -n %{libname}
Shared library support for the efitools, efivar and efibootmgr.

%files -n %{libname}
%{_libdir}/libefi*.so.%{major}*

%package -n %{devname}
Summary:	The libefivar development files
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Conflicts:	%{_lib}efiboot-devel < 38-2
%rename  %{_lib}efiboot-devel

%description -n %{devname}
Development files for libefivar.

%files -n %{devname}
%{_includedir}/efivar/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc %{_mandir}/man3/*

#------------------------------------------------------------------

%prep
%autosetup -p1
sed -i -e 's!-march=native!!g' src/include/defaults.mk

%build
%set_build_flags
%make_build CC="%{__cc}" COMPILER="%{__cc}" OPTIMIZE="%{optflags}" libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}" V=1 -j1

%install
%make_install libdir="%{_libdir}" bindir="%{_bindir}" mandir="%{_mandir}"
