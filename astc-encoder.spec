#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	nosimd		# no SIMD backend
%bcond_without	sse2		# SSE2 backend
%bcond_without	sse41		# SSE4.1 backend
%bcond_without	avx2		# AVX2 backend
%bcond_without	static_libs	# static libraries
#
%ifnarch %{x8664} x32 i686 pentium4
%undefine	with_sse2
%endif
%ifnarch %{x8664} x32 i686
%undefine	with_sse41
%endif
%ifnarch %{x8664}
%undefine	with_avx2
%endif
%ifarch	%{x8664} x32
%undefine	with_simd_none
%endif
%define	backends	%{?with_nosimd:none} %{?with_sse2:sse2} %{?with_sse41:sse41} %{?with_avx2:avx2}

Summary:	ARM Adaptive Scalable Texture Compression (ASTC) Encoder
Summary(pl.UTF-8):	Koder ASTC (Adaptive Scalable Texture Compression) firmy ARM
Name:		astc-encoder
Version:	5.7.1
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/ARM-software/astc-encoder/releases
Source0:	https://github.com/ARM-software/astc-encoder/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	685ea0afd26fca153e3e106b497e3d43
Patch0:		%{name}-32bit.patch
URL:		https://github.com/ARM-software/astc-encoder
BuildRequires:	cmake >= 3.15
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpmbuild(macros) >= 2.047
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Arm(R) Adaptive Scalable Texture Compression (ASTC) Encoder, is
a command-line tool and library for compressing and decompressing
images using the ASTC texture compression standard.

%description -l pl.UTF-8
Koder ASTC (Adaptive Scalable Texture Compression) firmy Arm® to
narzędzie linii poleceń i biblioteka do kompresji i dekompresji
obrazów przy użyciu standardu kompresji tekstur ASTC.

%package devel
Summary:	Header files for ASTC Encoder library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ASTC Encoder
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for ASTC Encoder library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ASTC Encoder.

%prep
%setup -q
%patch -P0 -p1

%build
# BUILD_SHARED_LIBS=OFF to build veneer libs as static (the rest have explicit SHARED/STATIC)
%cmake -B build \
	-DBUILD_SHARED_LIBS=OFF \
	-DASTCENC_ISA_NONE=%{__ON_OFF nosimd} \
	-DASTCENC_ISA_SSE2=%{__ON_OFF sse2} \
	-DASTCENC_ISA_SSE41=%{__ON_OFF sse41} \
	-DASTCENC_ISA_AVX2=%{__ON_OFF avx2} \
	-DASTCENC_SHAREDLIB=ON

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/astcenc
cp -p Source/astcenc.h $RPM_BUILD_ROOT%{_includedir}/astcenc

ln -sf libastcenc-$(echo %{backends} | cut -d' ' -f1)-shared.so $RPM_BUILD_ROOT%{_libdir}/libastcenc.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md Docs/{ChangeLog-*.md,ChangeLogImg}
%if %{with nosimd}
%attr(755,root,root) %{_bindir}/astcenc-none
%{_libdir}/libastcenc-none-shared.so
%endif
%if %{with sse2}
%attr(755,root,root) %{_bindir}/astcenc-sse2
%{_libdir}/libastcenc-sse2-shared.so
%endif
%if %{with sse41}
%attr(755,root,root) %{_bindir}/astcenc-sse4.1
%{_libdir}/libastcenc-sse4.1-shared.so
%endif
%if %{with avx2}
%attr(755,root,root) %{_bindir}/astcenc-avx2
%{_libdir}/libastcenc-avx2-shared.so
%endif

%files devel
%defattr(644,root,root,755)
%doc Docs/{Encoding.md,FileFormat.md,FormatOverview.md,FormatOverviewImg}
%{_libdir}/libastcenc.so
%{_includedir}/astcenc
