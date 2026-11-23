%{?mingw_package_header}
%global unversion 2_5_0

Name:           mingw-expat
Version:        %(echo %{unversion} | sed 's/_/./g')
Release:        7%{?dist}
Summary:        MinGW Windows port of expat XML parser library

License:        MIT
URL:            https://libexpat.github.io/
Source0:        https://github.com/libexpat/libexpat/archive/R_%{unversion}.tar.gz#/expat-%{version}.tar.gz

BuildArch:      noarch
ExclusiveArch: %{ix86} x86_64

BuildRequires: autoconf, automake, libtool, xmlto, gcc-c++, docbook2X
BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils

Patch0: expat-2.5.0-CVE-2023-52425.patch
Patch1: expat-2.5.0-CVE-2024-28757.patch
Patch2: expat-2.5.0-CVE-2024-45490.patch
Patch3: expat-2.5.0-CVE-2024-45491.patch
Patch4: expat-2.5.0-CVE-2024-45492.patch
Patch5: expat-2.5.0-CVE-2024-50602.patch
Patch6: expat-2.5.0-CVE-2024-8176.patch
Patch7: expat-2.5.0-CVE-2025-59375.patch
Patch8: expat-2.5.0-CVE-2026-45186.patch
Patch9: expat-2.5.0-CVE-2026-50219.patch
Patch10: expat-2.5.0-CVE-2026-56132.patch
Patch11: expat-2.5.0-CVE-2026-93990.patch
# The next patch also fixes CVE-2026-76641
Patch12: expat-2.5.0-CVE-2026-66046.patch
Patch13: expat-2.5.0-CVE-2026-77214.patch
Patch14: expat-2.5.0-CVE-2026-102633.patch
Patch15: expat-2.5.0-CVE-2026-118370.patch
Patch16: expat-2.5.0-CVE-2026-117610.patch
# https://issues.redhat.com/browse/RHEL-290449
# https://github.com/libexpat/libexpat/pull/1433
# https://github.com/libexpat/libexpat/pull/1439
Patch17: expat-2.5.0-CVE-2026-115506.patch


%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

# Win32
%package -n mingw32-expat
Summary:        MinGW Windows port of expat XML parser library

%description -n mingw32-expat
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package -n mingw32-expat-static
Summary:        Static version of the MinGW Windows expat XML parser library
Requires:       mingw32-expat = %{version}-%{release}

%description -n mingw32-expat-static
Static version of the MinGW Windows expat XML parser library.

# Win64
%package -n mingw64-expat
Summary:        MinGW Windows port of expat XML parser library

%description -n mingw64-expat
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package -n mingw64-expat-static
Summary:        Static version of the MinGW Windows expat XML parser library
Requires:       mingw64-expat = %{version}-%{release}

%description -n mingw64-expat-static
Static version of the MinGW Windows expat XML parser library.


%?mingw_debug_package


%prep
%setup -q -n libexpat-R_%{unversion}/expat
pushd ..
%patch -P0 -p1 -b .CVE-2023-52425
%patch -P1 -p1 -b .CVE-2024-28757
%patch -P2 -p1 -b .CVE-2024-45490
%patch -P3 -p1 -b .CVE-2024-45491
%patch -P4 -p1 -b .CVE-2024-45492
%patch -P5 -p1 -b .CVE-2024-50602
%patch -P6 -p1 -b .CVE-2024-8176
%patch -P7 -p1 -b .CVE-2025-59375
%patch -P8 -p1 -b .CVE-2026-45186
%patch -P9 -p1 -b .CVE-2026-50219
%patch -P10 -p1 -b .CVE-2026-56132
%patch -P11 -p1 -b .CVE-2026-93990
%patch -P12 -p1 -b .CVE-2026-66046
%patch -P13 -p1 -b .CVE-2026-77214
%patch -P14 -p1 -b .CVE-2026-102633
%patch -P15 -p1 -b .CVE-2026-118370
%patch -P16 -p1 -b .CVE-2026-117610
%patch -P17 -p1 -b .CVE-2026-115506
popd

sed -i 's/install-data-hook/do-nothing-please/' lib/Makefile.am
autoreconf -fi

%build
%mingw_configure
%mingw_make %{?_smp_mflags}


%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

# Remove .la files
find $RPM_BUILD_ROOT -name "*.la" -delete

# Remove documentation which duplicates that found in the native package.
rm -r $RPM_BUILD_ROOT%{mingw32_docdir}
rm -r $RPM_BUILD_ROOT%{mingw32_mandir}/man1
rm -r $RPM_BUILD_ROOT%{mingw64_docdir}
rm -r $RPM_BUILD_ROOT%{mingw64_mandir}/man1

# Win32
%files -n mingw32-expat
%license COPYING
%{mingw32_bindir}/libexpat-1.dll
%{mingw32_bindir}/xmlwf.exe
%{mingw32_libdir}/libexpat.dll.a
%{mingw32_libdir}/pkgconfig/expat.pc
%{mingw32_includedir}/expat.h
%{mingw32_includedir}/expat_config.h
%{mingw32_includedir}/expat_external.h
# Add CMake config files
%{mingw32_libdir}/cmake/expat-%{version}/*

%files -n mingw32-expat-static
%{mingw32_libdir}/libexpat.a

# Win64
%files -n mingw64-expat
%license COPYING
%{mingw64_bindir}/libexpat-1.dll
%{mingw64_bindir}/xmlwf.exe
%{mingw64_libdir}/libexpat.dll.a
%{mingw64_libdir}/pkgconfig/expat.pc
%{mingw64_includedir}/expat.h
%{mingw64_includedir}/expat_config.h
%{mingw64_includedir}/expat_external.h
# Add CMake config files
%{mingw64_libdir}/cmake/expat-%{version}/*

%files -n mingw64-expat-static
%{mingw64_libdir}/libexpat.a


%changelog
* Wed Nov 18 2026 RHEL Packaging Agent <redhat-ymir-agent@redhat.com> - 2.5.0-7
- CVE-2026-115506 mingw-expat: expat: Denial of Service via delayed entity amplification detection
  Resolves: RHEL-290449

* Wed Nov 04 2026 RHEL Packaging Agent <redhat-ymir-agent@redhat.com> - 2.5.0-6
- CVE-2026-117610 mingw-expat: expat: Denial of Service via NULL pointer
  dereference in external entity parsing
  Resolves: RHEL-300710

* Wed Nov 04 2026 RHEL Packaging Agent <redhat-ymir-agent@redhat.com> - 2.5.0-5
- CVE-2026-118370 mingw-expat: expat: Denial of Service via integer overflow during XML attribute parsing
  Resolves: RHEL-300767

* Sun Oct 25 2026 Uri Lublin <uril@redhat.com> - 2.5.0-4
- fix the following CVEs: CVE-2026-77214 CVE-2026-102633
  Resolves: RHEL-277499

* Thu Oct 01 2026 Uri Lublin <uril@redhat.com> - 2.5.0-3
- Fix the following CVEs:
  CVE-2026-45186 CVE-2026-50219 CVE-2026-56132.patch
  CVE-2026-93990 CVE-2026-66046 CVE-2026-76641
  Resolves: RHEL-177987
  Resolves: RHEL-269007
  Resolves: RHEL-260139
  Resolves: RHEL-269276

* Wed Nov 26 2025 Lili Zhu <lizhu@redhat.com> - 2.5.0-2
- Add xmlwf.exe back to mingw-expat.

* Thu Nov 20 2025 Lili Zhu <lizhu@redhat.com> - 2.5.0-1
- Rebase to version 2.5.0
- Fix the following CVEs
  CVE-2023-52425 CVE-2024-28757 CVE-2024-45490
  CVE-2024-45491 CVE-2024-45492 CVE-2024-50602
  CVE-2024-8176 CVE-2025-59375
- Resolves: RHEL-114628

* Wed Jun 10 2020 Uri Lublin <uril@redhat.com> - 2.2.4-5
- Rebuild
- Resolves: rhbz#1773899

* Wed May 06 2020 Uri Lublin <uril@redhat.com> - 2.2.4-4
- Fix CVE-2018-20843
- Resolves: rhbz#1773899

* Tue Aug 14 2018 Victor Toso <victortoso@redhat.com> - 2.2.4-3
- ExclusiveArch: i686, x86_64
- Related: rhbz#1615874

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 2.2.4-1
- Update to 2.2.4

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 24 2016 Kalev Lember <klember@redhat.com> - 2.2.0-1
- Update to 2.2.0
- Don't set group tags
- Use license macro for COPYING

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.1.0-3
- Added static subpackages

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Dropped the autoconf/libtool regeneration pieces

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-12
- Added win64 support
- Dropped unneeded RPM tags

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.0.1-11
- Remove .la files

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-10
- Renamed the source package to mingw-expat (RHBZ #800377)
- Use mingw macros without leading underscore
- Use the RPM magic to automatically generate provides/requires tags
- Automatically generate a debuginfo subpackage

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-9
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-6
- Fix Source0 URL.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-4
- Remove +x permissions on COPYING file.

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-3
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-2
- Include license.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-1
- Initial RPM release.
