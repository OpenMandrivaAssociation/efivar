%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:		efivar
Version:	0.15
Release:	1
Summary:	EFI variables management tool
License:	LGPLv2.1
Group:		System/Kernel and hardware
Url:		https://github.com/vathpela/efivar
Source0:	https://github.com/vathpela/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2


Requires:	%{libname} = %{version}-%{release}
BuildRequires:  popt-devel

%description
efivar is a command line interface to the EFI variables in /sys/firmware/efi

#------------------------------------------------------------------

%package -n     %{libname}
Summary:        Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Shared library support for the efitools, efivar and efibootmgr

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#------------------------------------------------------------------

%package -n     %{devname}
Summary:        foo development files
Group:		Development/Other
Requires:       %{libname} = %{EVRD}
Provides:       %{name}-devel = %{EVRD}

%description -n %{devname}
Development files for libefivar

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/*.so

#------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}

%build
%make libdir=%{_libdir} bindir=%{_bindir} %{optflags}

%install
%makeinstall_std

%files
%doc COPYING README
%{_bindir}/efivar
%{_mandir}/man1/*

%files -n %{develname}
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{libname}
%{_libdir}/*.so.%{major}*

