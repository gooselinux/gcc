%global DATE 20100726
%global SVNREV 162526
%global gcc_version 4.4.4
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 13
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%if 0%{?fedora} >= 13 || 0%{?rhel} >= 6
%global include_gappletviewer 0
%else
%global include_gappletviewer 1
%endif
%ifarch %{ix86} x86_64 ia64 ppc ppc64 alpha
%global build_ada 1
%else
%global build_ada 0
%endif
%global build_java 1
%ifarch %{sparc}
%global build_cloog 0
%else
%global build_cloog 1
%endif
%global build_libstdcxx_docs 1
# If you don't have already a usable gcc-java and libgcj for your arch,
# do on some arch which has it rpmbuild -bc --with java_tar gcc41.spec
# which creates libjava-classes-%{version}-%{release}.tar.bz2
# With this then on the new arch do rpmbuild -ba -v --with java_bootstrap gcc41.spec
%global bootstrap_java %{?_with_java_bootstrap:%{build_java}}%{!?_with_java_bootstrap:0}
%global build_java_tar %{?_with_java_tar:%{build_java}}%{!?_with_java_tar:0}
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_4-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: libgcc_post_upgrade.c
Source2: README.libgcjwebplugin.so
Source3: protoize.1
%global fastjar_ver 0.97
Source4: http://download.savannah.nongnu.org/releases/fastjar/fastjar-%{fastjar_ver}.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
%if 0%{?fedora} >= 13
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
BuildRequires: binutils >= 2.20.51.0.2-12
%else
BuildRequires: binutils >= 2.19.51.0.14-33
%endif
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
# For VTA guality testing
BuildRequires: gdb
%if %{build_java}
BuildRequires: /usr/share/java/eclipse-ecj.jar, zip, unzip
%if %{bootstrap_java}
Source10: libjava-classes-%{version}-%{release}.tar.bz2
%else
BuildRequires: gcc-java, libgcj
%endif
%endif
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.72
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_cloog}
BuildRequires: ppl >= 0.10, ppl-devel >= 0.10, cloog-ppl >= 0.15, cloog-ppl-devel >= 0.15
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen
BuildRequires: graphviz
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
%if 0%{?fedora} >= 13
# Need binutils that support --no-add-needed
Requires: binutils >= 2.20.51.0.2-12
%else
Requires: binutils >= 2.19.51.0.14-33
%endif
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}
%endif
%if %{build_cloog}
Requires: cloog-ppl >= 0.15
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true

Patch0: gcc44-hack.patch
Patch1: gcc44-build-id.patch
Patch2: gcc44-c++-builtin-redecl.patch
Patch3: gcc44-ia64-libunwind.patch
Patch4: gcc44-java-nomulti.patch
Patch5: gcc44-ppc32-retaddr.patch
Patch6: gcc44-pr33763.patch
Patch7: gcc44-rh330771.patch
Patch8: gcc44-i386-libgomp.patch
Patch9: gcc44-sparc-config-detection.patch
Patch10: gcc44-libgomp-omp_h-multilib.patch
Patch11: gcc44-libtool-no-rpath.patch
Patch12: gcc44-cloog-dl.patch
Patch13: gcc44-unwind-debug-hook.patch
Patch14: gcc44-pr38757.patch
Patch15: gcc44-libstdc++-docs.patch
Patch16: gcc44-ppc64-aixdesc.patch
Patch17: gcc44-no-add-needed.patch
Patch18: gcc44-pr44542.patch
Patch19: gcc44-rh610785.patch
Patch20: gcc44-rh533181.patch

Patch1000: fastjar-0.97-segfault.patch
Patch1001: fastjar-0.97-len1.patch
Patch1002: fastjar-0.97-filename0.patch
Patch1003: fastjar-CVE-2010-0831.patch
Patch1004: fastjar-man.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.4 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{?_isa} = %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library. 

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libmudflap
Summary: GCC mudflap shared support library
Group: System Environment/Libraries

%description -n libmudflap
This package contains GCC shared support library which is needed
for mudflap support.

%package -n libmudflap-devel
Summary: GCC mudflap support
Group: Development/Libraries
Requires: libmudflap = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libmudflap-devel
This package contains headers for building mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap
option to GCC and when linking add -lmudflap, for threaded programs
also add -fmudflapth and -lmudflapth.

%package -n libmudflap-static
Summary: Static libraries for mudflap support
Group: Development/Libraries
Requires: libmudflap-devel = %{version}-%{release}

%description -n libmudflap-static
This package contains static libraries for building mudflap-instrumented
programs.

%package java
Summary: Java support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgcj = %{version}-%{release}
Requires: libgcj-devel = %{version}-%{release}
Requires: /usr/share/java/eclipse-ecj.jar
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%package -n libgcj
Summary: Java runtime library for gcc
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: zip >= 2.1
Requires: gtk2 >= 2.4.0
Requires: glib2 >= 2.4.0
Requires: libart_lgpl >= 2.1.0
%if %{build_java}
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: glib2-devel >= 2.4.0
%if %{include_gappletviewer}
BuildRequires: xulrunner-devel
%endif
BuildRequires: libart_lgpl-devel >= 2.1.0
BuildRequires: alsa-lib-devel
BuildRequires: libXtst-devel
BuildRequires: libXt-devel
%endif
Autoreq: true

%description -n libgcj
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%package -n libgcj-devel
Summary: Libraries for Java development using GCC
Group: Development/Languages
Requires: libgcj%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: /bin/awk
Autoreq: false
Autoprov: false

%description -n libgcj-devel
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%package -n libgcj-src
Summary: Java library sources from GCC4 preview
Group: System Environment/Libraries
Requires: libgcj = %{version}-%{release}
Autoreq: true

%description -n libgcj-src
The Java(tm) runtime library sources for use in Eclipse.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 95 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 95 libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 95 front-end to GCC. This package includes libraries,
which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 95 static libraries
Group: System Environment/Libraries
Requires: libgnat-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static
GNAT is a GNU Ada 95 front-end to GCC. This package includes static libraries.

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch1 -p0 -b .build-id~
%patch2 -p0 -b .c++-builtin-redecl~
%patch3 -p0 -b .ia64-libunwind~
%patch4 -p0 -b .java-nomulti~
%patch5 -p0 -b .ppc32-retaddr~
%patch6 -p0 -b .pr33763~
%patch7 -p0 -b .rh330771~
%patch8 -p0 -b .i386-libgomp~
%patch9 -p0 -b .sparc-config-detection~
%patch10 -p0 -b .libgomp-omp_h-multilib~
%patch11 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch12 -p0 -b .cloog-dl~
%endif
%patch13 -p0 -b .unwind-debug-hook~
%patch14 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch15 -p0 -b .libstdc++-docs~
%endif
%patch16 -p0 -b .ppc64-aixdesc~
%if 0%{?fedora} >= 13
%patch17 -p0 -b .no-add-needed~
%endif
%patch18 -p0 -b .pr44542~
%patch19 -p0 -b .rh610785~
%patch20 -p0 -b .rh533181~

# This testcase doesn't compile.
rm libjava/testsuite/libjava.lang/PR35020*

tar xzf %{SOURCE4}

%patch1000 -p0 -b .fastjar-0.97-segfault~
%patch1001 -p0 -b .fastjar-0.97-len1~
%patch1002 -p0 -b .fastjar-0.97-filename0~
%patch1003 -p0 -b .fastjar-CVE-2010-0831~
%patch1004 -p0 -b .fastjar-man~

%if %{bootstrap_java}
tar xjf %{SOURCE10}
%endif

sed -i -e 's/4\.4\.5/4.4.4/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

# Default to -gdwarf-3 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2 or 3; the default version is \)2\./\13./' gcc/doc/invoke.texi

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

%build

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
# gjar isn't usable, so even when GCC source tree no longer includes
# fastjar, build it anyway.
mkdir fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
cd fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
../configure CFLAGS="%{optflags}" --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir}
make %{?_smp_mflags}
export PATH=`pwd`${PATH:+:$PATH}
cd ../../
%endif

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_java}
%if !%{bootstrap_java}
# If we don't have gjavah in $PATH, try to build it with the old gij
mkdir java_hacks
cd java_hacks
cp -a ../../libjava/classpath/tools/external external
mkdir -p gnu/classpath/tools
cp -a ../../libjava/classpath/tools/gnu/classpath/tools/{common,javah,getopt} gnu/classpath/tools/
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/common/Messages.properties gnu/classpath/tools/common
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/getopt/Messages.properties gnu/classpath/tools/getopt
cd external/asm; for i in `find . -name \*.java`; do gcj --encoding ISO-8859-1 -C $i -I.; done; cd ../..
for i in `find gnu -name \*.java`; do gcj -C $i -I. -Iexternal/asm/; done
gcj -findirect-dispatch -O2 -fmain=gnu.classpath.tools.javah.Main -I. -Iexternal/asm/ `find . -name \*.class` -o gjavah.real
cat > gjavah <<EOF
#!/bin/sh
export CLASSPATH=`pwd`${CLASSPATH:+:$CLASSPATH}
exec `pwd`/gjavah.real "\$@"
EOF
chmod +x `pwd`/gjavah
cat > ecj1 <<EOF
#!/bin/sh
exec gij -cp /usr/share/java/eclipse-ecj.jar org.eclipse.jdt.internal.compiler.batch.GCCMain "\$@"
EOF
chmod +x `pwd`/ecj1
export PATH=`pwd`${PATH:+:$PATH}
cd ..
%endif
%endif

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object \
%if !%{build_ada}
	--enable-languages=c,c++,objc,obj-c++,java,fortran \
%else
	--enable-languages=c,c++,objc,obj-c++,java,fortran,ada \
%endif
%if !%{build_java}
	--disable-libgcj \
%else
	--enable-java-awt=gtk --disable-dssi \
%if %{include_gappletviewer}
	--enable-plugin \
%endif
	--with-java-home=%{_prefix}/lib/jvm/java-1.5.0-gcj-1.5.0.0/jre \
	--enable-libgcj-multifile \
%if !%{bootstrap_java}
	--enable-java-maintainer-mode \
%endif
	--with-ecj-jar=/usr/share/java/eclipse-ecj.jar \
	--disable-libjava-multilib \
%endif
%if %{build_cloog}
	--with-ppl --with-cloog \
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%if 0%{?rhel} >= 6
%ifarch ppc ppc64
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

#GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap

# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/boehm-gc rpm.doc/fastjar rpm.doc/libffi rpm.doc/libjava
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}
sed -e 's,@VERSION@,%{gcc_version},' %{SOURCE2} > rpm.doc/README.libgcjwebplugin.so

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
(cd boehm-gc; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar-%{fastjar_ver}; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libffi; for i in ChangeLog* README* LICENSE; do
	cp -p $i ../rpm.doc/libffi/$i.libffi
done)
(cd libjava; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
cp -p libjava/LIBGCJ_LICENSE rpm.doc/libjava/

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%if %{build_java_tar}
find libjava -name \*.h -type f | xargs grep -l '// DO NOT EDIT THIS FILE - it is machine generated' > libjava-classes.list
find libjava -name \*.class -type f >> libjava-classes.list
find libjava/testsuite -name \*.jar -type f >> libjava-classes.list
tar cf - -T libjava-classes.list | bzip2 -9 > $RPM_SOURCE_DIR/libjava-classes-%{version}-%{release}.tar.bz2
%endif

%install
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_java}
make DESTDIR=%{buildroot} -C %{gcc_target_platform}/libjava install-src.zip
%endif
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
mkdir -p %{buildroot}/lib
ln -sf ..%{_prefix}/bin/cpp %{buildroot}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/stdc++.h.gch dirs
# 1) there is no bits/stdc++.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/stdc++.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
mv $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}
mv $libstdcxx_doc_builddir/man/man3 %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f
%if %{build_java}
# gcj -static doesn't work properly anyway, unless using --whole-archive
# and saving 35MB is not bad.
find %{buildroot} -name libgcj.a -o -name libgtkpeer.a \
		     -o -name libgjsmalsa.a -o -name libgcj-tools.a -o -name libjvm.a \
		     -o -name libgij.a -o -name libgcj_bc.a -o -name libjavamath.a \
  | xargs rm -f

mv %{buildroot}%{_prefix}/lib/libgcj.spec $FULLPATH/
sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/' \
  $FULLPATH/libgcj.spec
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%ifarch ppc
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif
%ifarch ppc64
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

%if %{build_java}
pushd ../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
make install DESTDIR=%{buildroot}
popd

if [ "%{_lib}" != "lib" ]; then
  mkdir -p %{buildroot}%{_prefix}/%{_lib}/pkgconfig
  sed '/^libdir/s/lib$/%{_lib}/' %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc \
    > %{buildroot}%{_prefix}/%{_lib}/pkgconfig/`basename %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc`
fi
%endif

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.2 libobjc.so
ln -sf ../../../libstdc++.so.6.* libstdc++.so
ln -sf ../../../libgfortran.so.3.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../libgcj.so.10.* libgcj.so
ln -sf ../../../libgcj-tools.so.10.* libgcj-tools.so
ln -sf ../../../libgij.so.10.* libgij.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.2 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.* libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../../%{_lib}/libgcj.so.10.* libgcj.so
ln -sf ../../../../%{_lib}/libgcj-tools.so.10.* libgcj-tools.so
ln -sf ../../../../%{_lib}/libgij.so.10.* libgij.so
%endif
fi
%if %{build_java}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcj_bc.so $FULLLPATH/
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.*a $FULLLPATH/

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-4.4.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-4.4.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.4.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.4.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.4.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
ln -sf ../../../../../lib64/libobjc.so.2 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.* | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.3.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib/libgcj.so.10.* | sed s~/lib/~/lib64/~` 64/libgcj.so
ln -sf ../`echo ../../../../lib/libgcj-tools.so.10.* | sed s~/lib/~/lib64/~` 64/libgcj-tools.so
ln -sf ../`echo ../../../../lib/libgij.so.10.* | sed s~/lib/~/lib64/~` 64/libgij.so
ln -sf lib32/libgcj_bc.so libgcj_bc.so
ln -sf ../lib64/libgcj_bc.so 64/libgcj_bc.so
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgfortran.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
ln -sf lib32/libmudflap.a libmudflap.a
ln -sf ../lib64/libmudflap.a 64/libmudflap.a
ln -sf lib32/libmudflapth.a libmudflapth.a
ln -sf ../lib64/libmudflapth.a 64/libmudflapth.a
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.2 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.* | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.3.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib64/libgcj.so.10.* | sed s~/../lib64/~/~` 32/libgcj.so
ln -sf ../`echo ../../../../lib64/libgcj-tools.so.10.* | sed s~/../lib64/~/~` 32/libgcj-tools.so
ln -sf ../`echo ../../../../lib64/libgij.so.10.* | sed s~/../lib64/~/~` 32/libgij.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libgfortran.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
ln -sf ../lib32/libmudflap.a 32/libmudflap.a
ln -sf lib64/libmudflap.a libmudflap.a
ln -sf ../lib32/libmudflapth.a 32/libmudflapth.a
ln -sf lib64/libmudflapth.a libmudflapth.a
%if %{build_java}
ln -sf ../lib32/libgcj_bc.so 32/libgcj_bc.so
ln -sf lib64/libgcj_bc.so libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libsupc++.a 32/libsupc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflap.a 32/libmudflap.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflapth.a 32/libmudflapth.a
%if %{build_java}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcj_bc.so 32/libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adalib 32/adalib
%endif
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libmudflap.a -o -name libmudflapth.a \
		    -o -name libgcc.a -o -name libgcov.a \) -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.2.*

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

mkdir -p %{buildroot}%{_prefix}/sbin
gcc -static -Os %{SOURCE1} -o %{buildroot}%{_prefix}/sbin/libgcc_post_upgrade
strip %{buildroot}%{_prefix}/sbin/libgcc_post_upgrade

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a}
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/bin/gnative2ascii

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
%endif
%endif

%if %{build_java}
mkdir -p %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	 %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
chmod 755 %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version} \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
touch %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%endif

install -m644 %{SOURCE3} %{buildroot}%{_mandir}/man1/protoize.1
echo '.so man1/protoize.1' > %{buildroot}%{_mandir}/man1/unprotoize.1
chmod 644 %{buildroot}%{_mandir}/man1/unprotoize.1

%check
cd obj-%{gcc_target_platform}

%if %{build_java}
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp
if [ -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%preun -n cpp
if [ $1 = 0 -a -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%post java
if [ -f %{_infodir}/gcj.info.gz ]; then
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%preun java
if [ $1 = 0 -a -f %{_infodir}/gcj.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%post gnat
if [ -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%preun gnat
if [ $1 = 0 -a -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p %{_prefix}/sbin/libgcc_post_upgrade

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig

%post -n libgcj
/sbin/ldconfig
if [ -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%preun -n libgcj
if [ $1 = 0 -a -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%postun -n libgcj -p /sbin/ldconfig

%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig

%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig

%post -n libgomp
/sbin/ldconfig
if [ -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%preun -n libgomp
if [ $1 = 0 -a -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libmudflap -p /sbin/ldconfig

%postun -n libmudflap -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/protoize
%{_prefix}/bin/unprotoize
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/protoize.1*
%{_mandir}/man1/unprotoize.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/SYSCALLS.c.X
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/abmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING*

%files -n cpp -f cpplib.lang
%defattr(-,root,root,-)
/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{_prefix}/sbin/libgcc_post_upgrade
%doc gcc/COPYING.LIB

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.so.6*

%files -n libstdc++-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%if 0%{?fedora} < 14
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%endif
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%if 0%{?fedora} >= 14
%files -n libstdc++-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%files objc
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%defattr(-,root,root,-)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.so.2*

%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%endif
%doc rpm.doc/gfortran/*

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.3*

%if %{build_java}
%files java
%defattr(-,root,root,-)
%{_prefix}/bin/gcj
%{_prefix}/bin/gjavah
%{_prefix}/bin/gcjh
%{_prefix}/bin/jcf-dump
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gcjh.1*
%{_infodir}/gcj*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ecj1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jvgenmain
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj-tools.so
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgij.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgij.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgij.so
%endif
%doc rpm.doc/changelogs/gcc/java/ChangeLog*

%files -n libgcj
%defattr(-,root,root,-)
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gij
%{_prefix}/bin/gjar
%{_prefix}/bin/fastjar
%{_prefix}/bin/grepjar
%{_prefix}/bin/grmic
%{_prefix}/bin/grmid
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gtnameserv
%{_prefix}/bin/gkeytool
%{_prefix}/bin/gorbd
%{_prefix}/bin/gserialver
%{_prefix}/bin/gcj-dbtool
%if %{include_gappletviewer}
%{_prefix}/bin/gappletviewer
%{_mandir}/man1/gappletviewer.1*
%endif
%{_prefix}/bin/gjarsigner
%{_mandir}/man1/fastjar.1*
%{_mandir}/man1/grepjar.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/gtnameserv.1*
%{_infodir}/fastjar.info*
%{_infodir}/cp-tools.info*
%{_prefix}/%{_lib}/libgcj.so.*
%{_prefix}/%{_lib}/libgcj-tools.so.*
%{_prefix}/%{_lib}/libgcj_bc.so.*
%{_prefix}/%{_lib}/libgij.so.*
%dir %{_prefix}/%{_lib}/gcj-%{version}
%{_prefix}/%{_lib}/gcj-%{version}/libgtkpeer.so
%{_prefix}/%{_lib}/gcj-%{version}/libgjsmalsa.so
%{_prefix}/%{_lib}/gcj-%{version}/libjawt.so
%if %{include_gappletviewer}
%{_prefix}/%{_lib}/gcj-%{version}/libgcjwebplugin.so
%endif
%{_prefix}/%{_lib}/gcj-%{version}/libjvm.so
%{_prefix}/%{_lib}/gcj-%{version}/libjavamath.so
%dir %{_prefix}/share/java
%{_prefix}/share/java/[^sl]*
%{_prefix}/share/java/libgcj-%{version}.jar
%dir %{_prefix}/%{_lib}/security
%config(noreplace) %{_prefix}/%{_lib}/security/classpath.security
%{_prefix}/%{_lib}/logging.properties
%dir %{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%if %{include_gappletviewer}
%doc rpm.doc/README.libgcjwebplugin.so
%endif

%files -n libgcj-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/gcj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jvmpi.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.spec
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgcj_bc.so
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgcj_bc.so
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[gj]*
%{_prefix}/include/c++/%{gcc_version}/org
%{_prefix}/include/c++/%{gcc_version}/sun
%{_prefix}/%{_lib}/pkgconfig/libgcj-*.pc
%doc rpm.doc/boehm-gc/* rpm.doc/fastjar/* rpm.doc/libffi/*
%doc rpm.doc/libjava/*

%files -n libgcj-src
%defattr(-,root,root,-)
%dir %{_prefix}/share/java
%{_prefix}/share/java/src*.zip
%{_prefix}/share/java/libgcj-tools-%{version}.jar
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root,-)
%{_prefix}/bin/gnat*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adalib
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%if 0%{?fedora} >= 14
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%if 0%{?fedora} >= 14
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%if 0%{?fedora} >= 14
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif
%endif

%if 0%{?fedora} >= 14
%files -n libgnat-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif
%endif
%endif

%files -n libgomp
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%files -n libmudflap
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libmudflap.so.0*
%{_prefix}/%{_lib}/libmudflapth.so.0*

%files -n libmudflap-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%if 0%{?fedora} < 14
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflapth.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflapth.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%endif
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

%if 0%{?fedora} >= 14
%files -n libmudflap-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflapth.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflapth.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%endif
%endif

%changelog
* Mon Jul 26 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-13
- update from gcc-4_4-branch
  - PRs fortran/45019, target/42869, target/44942, testsuite/38946
- VTA backports
  - PRs debug/45015, bootstrap/45028
  - var-tracking improvements (#616050, PR debug/45003, PR debug/45006)
- fix fortran SELECT CASE handling with CHARACTER type (PR fortran/40206)
- small OpenMP debug info improvements (#533181)

* Tue Jul 13 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-12
- update from gcc-4_4-branch
  - PRs fortran/44582, fortran/44773, fortran/44847, pch/14940, target/33743
- fix inline-asm check for auto-inc-dec operands (PR testsuite/44701)
- use DW_OP_const[48]u instead of DW_OP_addr for DW_OP_GNU_push_tls_address
  operand

* Wed Jul  7 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-11
- update from gcc-4_4-branch
  - PRs target/44597, target/44705
- VTA backports
  - PR c++/44808
  - avoid outputting invalid registers in debug info (#610455)
- -Wunused-but-set-* vector assignment fix (PR c++/44780)
- fix PowerPC address reloading for inline-asms (#608768, PR target/44707)
- fix predictive commoning (#609488, PR tree-optimization/40421)
- fix SRA not to do useless sign-extensions that confuses ivopts (#610785)
- fix IPP handling in libgcj (#578382)

* Wed Jun 30 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-10
- update from gcc-4_4-branch
  - PRs fortran/43841, fortran/43843, tree-optimization/44683
  - fix qualified-id as template argument handling (#605761, PR c++/44587)
- -Wunused-but-set-* static_cast fix (PR c++/44682)
- VTA backports
  - PRs debug/44610, debug/44668, debug/44694
- unswitching fixes (PR middle-end/43866)

* Thu Jun 24 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-9
- update from gcc-4_4-branch
  - PRs bootstrap/44426, bootstrap/44544, c++/44627, fortran/44536,
	libgcj/44216, target/39690, target/43740, target/44261, target/44481,
	target/44534, target/44615, testsuite/32843, testsuite/43739,
	tree-optimization/44508
- VTA backports
  - PRs debug/43650, debug/44181, debug/44247
- -Wunused-but-set-* ->*/.* fix (PR c++/44619)
- undeprecate #ident and #sccs (#606069)
%if 0%{?fedora} >= 14
- fix up libgnat-static
%endif
- fixup dates in generated man pages even for fastjar and gcc/ man pages
- don't realign stack on x86/x86-64 just because a DECL_ALIGN was set
  too high by expansion code (#603924, PR target/44542)
- don't allow side-effects in inline-asm memory operands unless
  < or > is present in operand's constraint (#602359, PR middle-end/44492)

* Fri Jun 11 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-8
- update from gcc-4_4-branch
  - fix demangler (PR other/43838)
- VTA backports
  - further var-tracking speedup (#598310, PR debug/41371)
- for typedefs in non-template classes adjust underlying type to
  emit proper debug info (#601893)
- fix up fastjar directory traversal bugs (CVE-2010-0831)

* Tue Jun  8 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-7
- update from gcc-4_4-branch
  - PRs c++/43555, fortran/42900, fortran/44360, libfortran/41169,
	libgcj/38251, libobjc/36610, libstdc++/32499, pch/14940,
	rtl-optimization/39580, target/44075, target/44169, target/44199
- VTA backports
  - PRs debug/44367, debug/44375, rtl-optimization/44013,
	tree-optimization/44182
  - speed up var-tracking (#598310, PR debug/41371)
- -Wunused-but-set-* bugfixes
  - PRs c++/44361, c++/44362, c++/44412, c++/44443, c++/44444
- fix -mno-fused-madd -mfma4 on i?86/x86_64 (PR target/44338)
- use GCJ_PROPERTIES=jdt.compiler.useSingleThread=true when
  building classes with ecj1 (#524155)
%if 0%{?fedora} >= 14
- add some static subpackages (#556049)
%endif

* Tue May 25 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-5
- update from gcc-4_4-branch
  - PRs bootstrap/43870, debug/44205, target/43733, target/44074,
	target/44202, target/44245, tree-optimization/43845
  - fix cv-qual issue with function types (#593750, PR c++/44193)
- VTA backports
  - PRs debug/41371, debug/42801, debug/43260, debug/43521

* Tue May 18 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-4
- update from gcc-4_4-branch
  - PR fortran/44135
- C++ -Wunused-but-set-variable fix (PR c++/44108)
- avoid C++ gimplification affecting mangling (#591635, PR c++/44148)
- asm goto fixes (PRs middle-end/44102, bootstrap/42347)
- VTA backports
  - PRs debug/41371, debug/44112

* Fri May 14 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-3
- update from gcc-4_4-branch
  - PRs debug/43370, documentation/44016, fortran/44036, middle-end/43671,
	middle-end/44085, target/43744
- make comdat guards of STB_GNU_UNIQUE variables also STB_GNU_UNIQUE
  (PR c++/44059)
- VTA backports
  - PRs debug/42278, debug/43950, debug/43983,debug/44104, debug/44136
  - fix up .debug_macinfo (#479914)
- asm goto fixes (PRs middle-end/44071, middle-end/42739)
- fix up -march=native (PR target/44046)
- C++ -Wunused-but-set-{variable,parameter} support, fixes for C support
  (#538266, PRs c++/44062, c/43981)
- -march=bdver1 and -mtune=bdver1 support

* Mon May  3 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-2
- fix VTA ICE on subregs of @GOTPCREL symbols (#588154, PR debug/43972)

* Fri Apr 30 2010 Jakub Jelinek <jakub@redhat.com> 4.4.4-1
- update from gcc-4_4-branch
  - GCC 4.4.4 release
- VTA backports
  - PR target/43921

* Tue Apr 27 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-19
- Power7 backports (#584993, #585005)
  - PRs tree-optimization/43544, target/41787, target/43154, middle-end/42431,
	rtl-optimization/43413
- add @GCC_4.5.0 symbols to libgcc_s
  - PRs target/43383, other/25232
- force DW_CFA_def_cfa instead of DW_CFA_def_cfa_{register,offset{,_sf}}
  after DW_CFA_def_cfa_expression
- make sure _Unwind_DebugHook uses standard calling convention
- #pragma omp for fix (PR c/43893)

* Thu Apr 22 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-18
- update from gcc-4_4-branch
  - PRs fortran/43339, fortran/43836, libgcj/40860, libgomp/43569,
	libgomp/43706, libstdc++/40518, middle-end/43337, middle-end/43570,
	tree-optimization/43769, tree-optimization/43771
  - fix ICE when compiling 64-bit Wine (#583501, PR target/43662)
- VTA backports
  - PRs debug/40040, debug/43762
- add support for -Wunused-but-set-{parameter,variable} non-default
  warnings for C (#538266, PRs c/18624, bootstrap/43699)

* Fri Apr  9 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-16
- update from gcc-4_4-branch
  - PRs ada/41912, fortran/43539, middle-end/42956, middle-end/43614,
	target/38085, target/43458, target/43643, target/43668,
	tree-optimization/43186, tree-optimization/43560,
	tree-optimization/43607, tree-optimization/43629
- VTA backports
  - PR debug/43670
- fix xop-vpermil2p* tests (target/43103)

* Wed Apr  7 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-15
- update from gcc-4_4-branch
  - PRs libfortran/43605, target/43638
- AMD XOP fixes (#579493, PRs target/42664, target/43667)
- fix raw string support on big endian hosts (PR preprocessor/43642)
- allow -gdwarf-4 option

* Thu Apr  1 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-14
- update from gcc-4_4-branch
  - PRs other/43562, c++/41185, c++/41786, fortran/43409, fortran/43551,
	libfortran/43409, middle-end/43600, target/39254, target/43524,
	tree-optimization/43528
- update raw string support to match N3077
- VTA backports
  - PRs bootstrap/43596, debug/42977, debug/43557, debug/43593,
	target/43580

* Sat Mar 27 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-13
- update from gcc-4_4-branch
  - PRs c/43381, libfortran/43517, target/42113
- VTA backports
  - PRs debug/43516, debug/43540

* Thu Mar 25 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-12
- update from gcc-4_4-branch
  - PRs c/43385, target/43348, tree-optimization/43415
- VTA backports
  - PRs bootstrap/43511, debug/19192, debug/43479, debug/43508
- provide unwind info even for C++ thunks on x86, x86-64 and s390{,x}
  (PR target/43498)
- provide unwind info for x86 PIC thunks even when not using CFI assembler
  directives (PR debug/43293)

* Mon Mar 22 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-11
- update from gcc-4_4-branch
  - PRs c++/43116, libfortran/43265, libgomp/42942, middle-end/42718,
	middle-end/43419, rtl-optimization/43360, rtl-optimization/43438,
	target/43305, target/43417
- VTA backports
  - PRs bootstrap/43399, bootstrap/43403, debug/42873, debug/43058,
	debug/43443, target/43399

* Tue Mar 16 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-10
- update from gcc-4_4-branch
  - PRs fortran/43228, fortran/43303, libfortran/43265, libfortran/43320
- VTA backports
  - PRs debug/36728, debug/43051, debug/43092, debug/43290,
	tree-optimization/42917, tree-optimization/43317
  - fix non-localized vars handling and forwarder block merging
    (#572260, PR debug/43329)
%if 0%{?rhel} >= 6
- remove gappletviewer, gcjwebplugin and related files even for
  RHEL, as xulrunner got updated to 1.9.2.1
%endif

* Tue Mar  9 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-9
- update from gcc-4_4-branch
  - PRs ada/42253, bootstrap/43121, c/43248, tree-optimization/43220
- VTA backports
  - PRs debug/42897, debug/43176, debug/43177, debug/43229, debug/43237,
	debug/43290, debug/43299, debug/43304
- fix unwind info in i?86 PIC register setup sequences (PR debug/43293)

* Fri Feb 26 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-8
- update from gcc-4_4-branch
  - PR libstdc++/21769
- VTA backports
  - PRs debug/42800, debug/43077, debug/43150, debug/43160, debug/43161,
	debug/43165, debug/43166, debug/43190, target/43139
- fix alignment of some stack vars (PR middle-end/39315)

* Sun Feb 21 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-7
- update from gcc-4_4-branch
  - PRs c++/43024, c++/43033, fortran/41869, target/40887,
	tree-optimization/42871, tree-optimization/43074
- VTA backports (PRs debug/42918, debug/43084)
- --enable-decimal-float on s390{,x} (#565871)
- improve __builtin_expect handling, propagate branch probabilities
  during expansion even for sequences with more than one jump
  (PR middle-end/42233)

* Thu Feb 11 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-6
- update from gcc-4_4-branch
  - PR tree-optimization/42705
  - fix up -femit-struct-debug-baseonly (#561320, PR debug/43010)
  - --enable-checking=valgrind bugfixes (PRs fortran/43029, fortran/43030)
- VTA backports (#562312)
- some further --enable-checking=valgrind bugfixes (PR target/38781)

* Mon Feb  8 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-5
- update from gcc-4_4-branch
  - PRs fortran/38324, fortran/41044, fortran/41167, fortran/42309,
	fortran/42650, fortran/42736, libfortran/42901, middle-end/42898,
	middle-end/42995, rtl-optimization/42952, tree-optimization/42462,
	tree-optimization/42890, tree-optimization/42931
- VTA backports
  - PRs target/42924, debug/42896, rtl-optimization/42889
%if 0%{?fedora} >= 13
- pass --no-add-needed to the linker
%endif

* Wed Jan 27 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-4
- update from gcc-4_4-branch
  - PRs bootstrap/42786, fortran/42866, target/38697, target/42841
- fix up handling of constant pool elements in dwarf2out
- fix acats norun.lst handling
- fix asm redirection of builtin ffs on 64-bit arches (#559186)

* Mon Jan 25 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-3
- VTA improvements (#556975, PR debug/42861)

* Sat Jan 23 2010 Dennis Gilmore <dennis@ausil.us> 4.4.3-2
- use gas .section syntax (#530847)

* Thu Jan 21 2010 Jakub Jelinek <jakub@redhat.com> 4.4.3-1
- update from gcc-4_4-branch
  - GCC 4.4.3 release
- don't insert DEBUG_STMTs after stmts that can throw, instead insert them
  at the start of the next bb

* Thu Jan 21 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-28
- update from gcc-4_4-branch
  - PRs middle-end/42803, rtl-optimization/42691, target/42542, target/42774,
	tree-optimization/41826, tree-optimization/42773
  - fix DW_OP_mod handling in the unwinder
- VTA backports
  - PRs debug/42782, debug/42767
  - avoid dead VALUES to magically reappear during var-tracking
    (#557068, PR debug/42715)
  - don't assume non-addressable automatic MEMs die at each call
    during var-tracking (#556975, PR debug/42728)

* Fri Jan 15 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-27
- fix ICE with std::complex<float> copy (#555705, PR middle-end/42760)
- avoid exponential hangs in gen_lsm_tmp_name

* Fri Jan 15 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-26
- update from gcc-4_4-branch
  - PR c++/42655

* Thu Jan 14 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-25
- update from gcc-4_4-branch
  - PRs c/42721, middle-end/40281, middle-end/42667, rtl-optimization/42699
- re-add --param max-vartrack-size patch, but this time with default 50mil
  instead of 5mil (#531218, #548826)
- don't emit -Wreturn-type warnings in noreturn functions
  (PR middle-end/42674)
- march=native fixes for ix86/x86_64

* Tue Jan 12 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-24
- update from gcc-4_4-branch
  - PRs debug/42662, libjava/40859
- speed up var-tracking on various KDE sources (PR debug/41371)
- revert --param max-vartrack-size=NNNN hack
- fix up epilogue unwinding with -fsched2-use-superblocks (PR middle-end/41883)
- fix a -fcompare-debug failure (PR tree-optimization/42645)
- don't make undef symbols weak just because they are known to have C++ vague
  linkage (PR c++/42608)

* Sat Jan  9 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-23
- update from gcc-4_4-branch
  - PRs target/42511, target/42542, target/42564
- VTA backports
  - PRs debug/42630, debug/42631
- improve construction of ppc64 constants between 0x80000000 and 0xffffffff
- fix inliner and var-tracking not to drop location info needlessly in certain
  cases (#552376, PR debug/42657)

* Wed Jan  6 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-22
- add --param max-vartrack-size=NNNN parameter, give up on
  -fvar-tracking-assignments if var-tracking hash tables are over that limit
- fix VTA bugs in the vectorizer (PRs debug/42604, debug/42395)
- fix VTA bug with noreturn calls (PR middle-end/42363)

* Tue Jan  5 2010 Jakub Jelinek <jakub@redhat.com> 4.4.2-21
- update from gcc-4_4-branch
  - PRs c++/42331, middle-end/41344, middle-end/42099, other/42611,
	rtl-optimization/42475, target/40134, target/42448, target/42503,
	target/42549, tree-optimization/41956, tree-optimization/42231,
	tree-optimization/42337, tree-optimization/42614
- fix -m*=native with several sources on the command line (PR driver/42442)
- avoid code size differences from traversing decl hash tables hashed by uid
  if uid gap sizes differ
- fix .debug_ranges with -ffunction-sections (PR debug/42454)

* Tue Dec 22 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-20
- fix MEM_SIZE of reload created stack slots (#548825,
  PR rtl-optimization/42429)
%if !%{include_gappletviewer}
- remove gappletviewer, gcjwebplugin and related files for F13 (#548783)
%endif
- fix addition of one character long filenames in fastjar (#549493)

* Thu Dec 17 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-18
- update from gcc-4_4-branch
  - PRs c++/42387
- another C++ virtual dtors fix (PR c++/42386)
- VTA mode and COND_EXEC fixes (PR debug/41679)
- fix ICE in chrec_convert_1 (#547775)
- fix debuginfo for optimized out TLS vars
- use DW_AT_location with DW_OP_addr + DW_OP_stack_value instead of
  DW_AT_const_value with address in it, use DW_OP_addr + DW_OP_stack_value
  instead of DW_OP_implicit_value with address (#546017)

* Mon Dec 14 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-17
- propagate TREE_NOTHROW/TREE_READONLY/DECL_PURE_P from ipa-pure-const and
  EH opt to all same body aliases (#547286)
- don't emit DWARF location list entries with no location or DW_AT_location
  with empty blocks (PR debug/41473)
- fix up AMD LWP support
- don't crash when mangling C++ decls inside of middle-end generated functions
  (PR c++/41183)

* Fri Dec 11 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-16
- update from gcc-4_4-branch
  - PRs c++/27425, c++/34274, c++/42301, fortran/42268, java/41991,
	libstdc++/42273, rtl-optimization/41574, target/41196, target/41939
	target/42263

* Wed Dec  9 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-15
- VTA backports
  - PRs debug/42166, debug/42234, debug/42244, debug/42299
- fix handling of C++ COMDAT virtual destructors
- some x86/x86_64 FMA4, XOP, ABM and LWP fixes
- fix a decltype handling bug in templates (PR c++/42277)

* Fri Dec  4 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-14
- update from gcc-4_4-branch
  - PRs libstdc++/42261, middle-end/42049
- backport C++0x ICE fix from trunk (PR c++/42266)
- fortran !$omp workshare improvements (PR fortran/35423)
- FMA4 and XOP fixes

* Wed Dec  2 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-13
- fix security issues in libltdl bundled within libgcj (CVE-2009-3736)

* Wed Dec  2 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-12
- update from gcc-4_4-branch
  - PRs c++/42234, fortran/41278, fortran/41807, fortran/42162, target/42113,
	target/42165
  - don't ICE on -O256 (#539923)
- fix -mregnames on ppc/ppc64
- optimize even COMDAT constructors and destructors without virtual
  bases (PR c++/3187)

* Mon Nov 23 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-11
- update from gcc-4_4-branch
  - PRs c++/42059, c++/42061, libgfortran/42090
- VTA backports
  - PRs debug/41886, debug/41888, debug/41926, tree-optimization/42078
- optimize non-COMDAT constructors and destructors without virtual
  bases by making the base and complete ctor or dtor aliases of
  each other (PR c++/3187)

* Sat Nov 14 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-10
- update from gcc-4_4-branch
  - PRs c++/21008, c++/37037, c++/41972, c++/41994, middle-end/40946,
	middle-end/42029
- VTA backports
  - PR middle-end/41930
- optimize deleting destructors for size (PR c++/3187)
- try to avoid file Requires by requiring package%%{?_isa} (#533947)

* Mon Nov  9 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-9
- update from gcc-4_4-branch
  - PRs c++/35067, c++/36912, c++/36959, c++/37093, c++/38699, c++/39786,
	c++/41856, c++/41876, c++/41967, c++/9381, fortran/41772,
	fortran/41909, middle-end/41963, rtl-optimization/41917,
	target/41900, tree-optimization/41643
- selected backports from trunk
  - PRs debug/41801, middle-end/41837, target/41985, tree-optimization/41841
- initial AMD Orochi -mxop and -mlwp support
- try to avoid wrapping CONST_INTs/VOIDmode CONST_DOUBLEs into CONST

* Mon Nov  2 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-8
- update from gcc-4_4-branch
  - PRs c++/41754, fortran/41777, fortran/41850, libstdc++/40852
- fix ICE with unmatched #pragma GCC visibility push/pop (PR c++/41774)
- fix VTA ICE with -combine (#531385, PR debug/41893)
- fix RTTI for anon namespace classes
- fix incorrect uses of __restrict keyword in valarray (PR libstdc++/41763)

* Tue Oct 27 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-7
- update from gcc-4_4-branch
  - PRs c++/40808, c/41842, cp-tools/39177
- VTA backports
  - PR bootstrap/41345
- don't emit DW_AT_name: <anonymous struct> etc. into debug info
  (#530304, PR debug/41828)
- power7 ABI fixes (PR target/41787)
- fix ICE in ix86_pic_register_p (PR target/41762)

* Thu Oct 22 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-6
- update from gcc-4_4-branch
  - PR target/41702
  - fix a pod2man error in gcc.1 (#530102)
  - fix mangling of very large names
- document -print-multi-os-directory in gcc.info and gcc.1
  (#529659, PR other/25507)

* Mon Oct 19 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-5
- update from gcc-4_4-branch
  - PR fortran/41755
  - s390 z10 tuning fixes
- provide accurate attributes for powerpc builtins (PR target/23983)
- fix -fcompare-debug differences caused by DCE removal of debug stmts
- fix updating of speculation status with VTA (PR debug/41739)

* Sun Oct 18 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-4
- update from gcc-4_4-branch
  - PRs c++/37204, c++/37766, c++/37875, c++/38798, c++/40092,
	libstdc++/40654, libstdc++/40826
- fix VTA ICE on invalid pointer arithmetics (#529512)

* Sat Oct 17 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-3
- fix VTA handling in the scheduler (PR debug/41535)
- fix up %%check section to be able to find ecj1

* Fri Oct 16 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-2
- update from gcc-4_4-branch
  - PR target/40913
- VTA backports
  - PR debug/41717
- fix Ada .eh_frame generation (PR debug/40521)

* Thu Oct 15 2009 Jakub Jelinek <jakub@redhat.com> 4.4.2-1
- update from gcc-4_4-branch
  - GCC 4.4.2 release
  - PRs middle-end/22072, target/41665
- don't emit -Wpadded warnings for builtin structures
- don't generate .eh_frame, but generate .debug_frame when -g and none of
  -fasynchronous-unwind-tables/-fexceptions/-funwind-tables is used
  (PR debug/40521)

* Wed Oct 14 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-22
- update from gcc-4_4-branch
  - PRs target/26515, target/38948
  - fix s390{,x} BLKmode symbol handling
  - fix i?86 testqi splitter (#528206, PR target/41680)
- VTA backports
  - introduce debug temps (PRs debug/41264, debug/41338, debug/41343,
    debug/41447, target/41693)
  - build debug stmts on updates (PR debug/41616)
  - fix another with/without -save-temps debug info difference
    (#526841, PR preprocessor/41543)
  - fix invalid ranges in .debug_loc section (PR debug/41695)
%if 0%{?rhel} >= 6
- if -mcpu= isn't specified, default to -mcpu=power4 (#463549)
%endif

* Sat Oct 10 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-21
- update from gcc-4_4-branch
  - fix s390{,x} prefetch for pre-z10 CPUs (#524552)
- VTA backports
  - fix debug info differences with/without -save-temps
    (PR preprocessor/41445)
- fix ICE with small BLKmode returning call (#516028,
  PR rtl-optimization/41646)

* Thu Oct  8 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-20
- update from gcc-4_4-branch
  - PRs c++/39863, c++/41038
- avoid redundant DW_AT_const_value when abstract origin already has one
  (#527430)
- another VTA debug stmt renaming bugfix (#521991)

* Mon Oct  5 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-19
- update from gcc-4_4-branch
  - PRs fortran/41479, fortran/41515
- VTA backports
  - PRs debug/41353, debug/41404, rtl-optimization/41511
  - another debug info fix for decls passed by reference (#527057,
    PR debug/41558)
  - don't emit DW_AT_name on DW_TAG_const_type (#526970)
- avoid invalid folding of casts to addresses of first fields
  (#527121, PR middle-end/41317)

* Thu Oct  1 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-18
- update from gcc-4_4-branch
  - PRs ada/41100, target/22093
- VTA backports
  - PRs debug/41438, debug/41474, target/41279, testsuite/41444
- fix VTA ICE on Linux kernel (#521991)
- AMD Orochi -mfma4 support
- don't run install-info if info files are missing because of --excludedocs
  (#515921, #515960, #515962, #515965, #516000, #516008, #516014)

* Fri Sep 25 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-17
- update from gcc-4_4-branch
  - fix vectorizer for power7 (#463846)
- VTA backports
  - fix debug info for parameters passed by reference (#525709)
  - PR bootstrap/41457
- remove power7 VSX load/store with update insn support
- remove SSE5 support

* Wed Sep 23 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-16
- update from gcc-4_4-branch
  - PRs c/39779, c/41049, debug/41065, libffi/40242, libffi/41443,
	libgfortran/41328, testsuite/41288
- VTA backports
  - PRs bootstrap/41397, bootstrap/41404, bootstrap/41405, debug/41295,
	debug/41411, debug/41439
  - fix ICE caused by reload substitution of const_int into zero_extend
    in debug_insn (#524439)
- fix altivec vec_cmp{lt,gt} (#524273)
- fix -mno-sched-epilogue on ppc (#524216, PR target/40473)
- don't look at MUDFLAP_OPTIONS env var in suid/sgid programs
  (PR libmudflap/41433)

* Fri Sep 18 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-15
- for now disable out of line gpr/fpr saving on ppc with -m64 -Os -mcall-aixdesc
- fix DW_AT_decl_{file,location} for DW_TAG_structure_type for C structs
  with forward declarations (#523810)

* Wed Sep 16 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-14
- update from gcc-4_4-branch
  - PRs fortran/39876, tree-optimization/41101
- asm goto support
- VTA delayed branch scheduling fix (PR bootstrap/41349)
- power7 VSX fix (PR target/41210)
- ppc bswap fixes (PR target/41331)

* Fri Sep 11 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-13
- fix ICE in debuginfo output with BLOCK_NONLOCALIZED_VARS (#518303)
- wrap_constant when propagating for subst in debug in the combiner (#522577)
- further fix for ppc -m32 -Os out of line gpr/fpr restoring (PR target/41175)

* Thu Sep 10 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-12
- update from gcc-4_4-branch
  - PRs bootstrap/41180, target/41315
- fix ICE in tree-ssa-phiprop.c (#522277, PR tree-optimization/39827)
- ppc64 bswap fix
- fix ppc/ppc64 -mmultiple and out of line gpr/fpr saving bugs
  (#519409, PR target/40677, PR target/41175)

* Wed Sep  9 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-11
- fix ICE in tls_mem_loc_descriptor (#521991)

* Tue Sep  8 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-10
- update from gcc-4_4-branch
  - PRs fortran/41258, rtl-optimization/40861
- fix scheduler not to reorder potentially trapping insns across
  calls that might not always return (#520916, PR rtl-optimization/41239)
- merge in VTA

* Thu Sep  3 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-9
- update from gcc-4_4-branch
  - fix wide char constant stringification
- __builtin_unreachable fix

* Wed Sep  2 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-8
- fix up __builtin_object_size (#505862)
- fix Fortran GOTO warning (PR fortran/38507)

* Tue Sep  1 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-7
- update from gcc-4_4-branch
  - PRs c++/41120, c++/41127, c++/41131, fortran/41062, fortran/41102,
	fortran/41121, fortran/41126, fortran/41139, fortran/41157,
	fortran/41162, libfortran/40962, libstdc++/41005, middle-end/41094,
	middle-end/41123, middle-end/41163, target/34412, target/40718
- fix pr22033.C on ppc*/ia64/sparc*
- emit namespace DIE even if it contains just some used type (PR debug/41170)
- fix dynamic_cast (#519517)
- backport power7 changes from the trunk, instead of using the old incomplete
  backport from ibm/power7-meissner

* Tue Aug 18 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-6
- update from gcc-4_4-branch
  - PRs bootstrap/41018, c/41046, debug/37801, debug/40990, fortran/40847,
	rtl-optimization/41033, target/41015, target/41019, target/8603,
	tree-optimization/41016

* Fri Aug  7 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-5
- update from gcc-4_4-branch
  - PRs c++/40948, target/40906
- -fexceptions support for -freorder-blocks-and-partition

* Wed Aug  5 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-4
- update from gcc-4_4-branch
  - PRs build/40010, c++/39987, c++/40749, c++/40834, c++/40948, debug/39706,
	fortran/40822, fortran/40848, fortran/40851, fortran/40878,
	libfortran/40853, middle-end/40943, rtl-optimization/40924,
	target/40577, testsuite/40829, testsuite/40891,
	tree-optimization/40570
- backport __builtin_unreachable () support
- fix powerpc ICE in memory_address (#515672, PR target/40971)

* Sat Jul 25 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-3
- update from gcc-4_4-branch
  - PR fortran/40727
- fix unwind info for -freorder-blocks-and-partitions
  (PR rtl-optimization/34999)
- fix Fortran MINLOC/MAXLOC/MINVAL/MAXVAL handling of infinities and NaNs,
  speed them up (PRs fortran/40643, fortran/31067)
- fix ICE with Fortran data xfer without io unit (PR fortran/40839)

* Thu Jul 23 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-2
- update from gcc-4_4-branch
  - PRs rtl-optimization/40710, target/40832, tree-optimization/40321
- use STB_GNU_UNIQUE symbols for inline fn local statics and
  template static data members
- use strcmp for C++ typeinfo comparisons instead of pointer comparison

* Wed Jul 22 2009 Jakub Jelinek <jakub@redhat.com> 4.4.1-1
- update from gcc-4_4-branch
  - GCC 4.4.1 release

* Tue Jul 21 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-15
- update from gcc-4_4-branch
  - PRs libfortran/40714, target/39943, target/40809, tree-optimization/40792
  - fix ICE in gsi_insert_seq_nodes_after (#505798,
    PR tree-optimization/40813)
- slightly relax -D_FORTIFY_SOURCE=2 rules for flexible-array-member like
  constructs (#512689, #511573)
- vectorize unsigned int -> {float,double} conversions on x86/x86_64
  (PR target/40811)
- update for i586.rpm -> i686.rpm switch (default to -march=i686 -mtune=generic
  in i686.rpm gcc and also with -m32 in x86_64.rpm gcc)

* Fri Jul 17 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-14
- update from gcc-4_4-branch
  - PRs c++/40740, libstdc++/40691, middle-end/40747
  - fix ICE in gimplify_conversion (#511229, PR c++/40780)

* Mon Jul 13 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-13
- update from gcc-4_4-branch
  - PRs c++/36628, c++/37206, c++/40502, c++/40684, c++/40689, fortran/40440,
	rtl-optimization/40667, target/40668
- avoid overlapping entries in .debug_ranges section (PR debug/40713)

* Wed Jul  8 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-12
- update from gcc-4_4-branch
  - PRs c++/35828, c++/37816, c++/37946, c++/40557, c++/40633, c++/40639,
	debug/40666, target/38900
- use more compact DW_AT_member_location for constant offsets (PR debug/40659)

* Tue Jul  7 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-11
- update from gcc-4_4-branch
  - PRs c++/40274, c++/40342, c++/40566, c++/40595, c++/40619, c/39902,
	fortran/40443, fortran/40551, fortran/40576, fortran/40594,
	fortran/40638, libfortran/40576, libstdc++/40297, libstdc++/40600,
	middle-end/40585, middle-end/40669, other/40024, target/40587,
	tree-optimization/40493, tree-optimization/40542,
	tree-optimization/40550, tree-optimization/40579,
	tree-optimization/40582, tree-optimization/40640
- backports from trunk
  - fix debuginfo in dynamically realigned functions (PR debug/40596)
  - speed up polyhedron NF (PR middle-end/34163)
  - epilogue unwinding fixes (PRs bootstrap/40347, debug/40462)
  - fix debug info for inlines (PR debug/40573)
  - optimize assuming allocatable arrays in the innermost
    dimension are always stride 1 (PR fortran/32131)

* Tue Jun 23 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-10
- update from gcc-4_4-branch
  - PRs fortran/39800, fortran/40402, libstdc++/40497, middle-end/40389,
	middle-end/40404, middle-end/40446, middle-end/40460, objc/28050,
	target/40470, tree-optimization/40492
- decrease memory consumption and speed up var-tracking pass (#503816)
- __builtin_object_size fix for C++ (#506952)

* Mon Jun 15 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-9
- update from gcc-4_4-branch
  - PR fortran/40168
- fix up debug.exp testsuite (PR testsuite/40426)
- fix up a pasto in recent -D_FORTIFY_SOURCE changes (#506099)

* Fri Jun 12 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-8
- update from gcc-4_4-branch
  - PRs c++/40381, libfortran/40330
- add -mcrc32 support on ix86
- support -gdwarf-3 and default to it, emit DW_OP_call_frame_cfa
- fix up ix86 padding for branch mispredicts
- improve .debug_loc generation

* Tue Jun  9 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-7
- update from gcc-4_4-branch
  - PRs ada/40166, bootstrap/40027, c++/38064, c++/39754, c++/40007,
	c++/40139, c/40172, c++/40306, c++/40307, c++/40308, c++/40311,
	c++/40370, c++/40372, c++/40373, debug/40109, fortran/22423,
	fortran/38654, fortran/39893, fortran/40019, fortran/40195,
	libfortran/25561, libfortran/37754, libfortran/38668,
	libfortran/39665, libfortran/39667, libfortran/39702,
	libfortran/39709, libfortran/39782, libfortran/40334,
	libgfortran/39664, libgomp/40174, libstdc++/36211, libstdc++/40192,
	libstdc++/40296, libstdc++/40299, middle-end/32950, middle-end/40147,
	middle-end/40204, middle-end/40233, middle-end/40252,
	middle-end/40291, middle-end/40328, middle-end/40340,
	rtl-optimization/40105, target/40017, target/40153, target/40266,
	testsuite/39907, tree-optimization/39999, tree-optimization/40087,
	tree-optimization/40238, tree-optimization/40254
- support Atom for -march=native
- add -mmovbe support for Atom
- improve ix86 instruction length computation, remove some unneeded padding
- -D_FORTIFY_SOURCE improvements
- emit accurate epilogue unwinding information
- add unwind debug hook for gdb

* Thu May 14 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-5
- update from gcc-4_4-branch
  - PRs c++/17395, c/39983, fortran/38863, fortran/38956, fortran/39879,
	fortran/40018, libstdc++/39546, libstdc++/40038, middle-end/39986,
	middle-end/40021, middle-end/40023, middle-end/40043,
	middle-end/40057, middle-end/40080, target/37179,
	tree-optimization/40062, tree-optimization/40074
- fix Fortran FMT= character array arguments (#492209, PR fortran/39865)
- allow putting breakpoints on Fortran END{SUBROUTINE,FUNCTION}
  (PR fortran/34153)
- incorporate changes suggested in gcc44 package review (#498911)

* Wed May  6 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-4
- update from gcc-4_4-branch
  - PRs c++/40013, libgcj/39899, libstdc++/39868, libstdc++/39880,
	libstdc++/39881, libstdc++/39882, libstdc++/39909, middle-end/39937,
	rtl-optimization/39914, target/39565, testsuite/39769,
	testsuite/39776, testsuite/39790, testsuite/39807,
	tree-optimization/39941
  - fix phiprop tuplification (#496400, PR tree-optimization/40022)
- don't add artificial default case label if switch labels already
  cover the whole range (PR middle-end/39666)
- fix DSE with block reads (PR middle-end/40035)
- fix debuginfo for C++ typedef struct {...} T (PR debug/35463)
- remove some unnecessary padding on x86_64/i386 added for >= 4 control
  flow insns in a 16-byte block (PR target/39942)
- don't create invalid DWARF location lists containing DW_OP_reg*
  followed by DW_OP_deref*, instead use DW_OP_breg* 0 (#481675)
- add libstdc++-docs subpackage, move html manual to it, add doxygen
  generated html and man pages

* Mon Apr 27 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-3
- update from gcc-4_4-branch
  - PR bootstrap/39739
  - fix -Wunused-value (#497545, PR c/39889)
- backport further power7-meissner branch changes (#497816)
- fix reg-stack ICE on SPEC2k6 453.povray with -m32 -O3 -msse3
  (PR target/39856)
- fix x86_64 ICE on passing structure with flexible array member
  (PR target/39903)

* Fri Apr 24 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-2
- update from gcc-4_4-branch
  - PR c++/38228
- fix folding of cond expr with comparison to MAX/MIN (PR middle-end/39867)
- fix up gcc-gnat install-info arguments (#452783)

* Thu Apr 23 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-1
- update from gcc-4_4-branch
  - GCC 4.4.0 release
  - PRs libstdc++/39802, c++/39639, c/39855, rtl-optimization/39762,
	testsuite/39781, tree-optimization/39824
- fix up DSE (PR rtl-optimization/39794)
- debuginfo fixes for VLA and nested/contained functions (#459374)
- improve -ftree-switch-conversion optimization if the constant is the
  same in all cases

* Mon Apr 20 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.35
- update from gcc-4_4-branch
  - PRs middle-end/39804, target/39678, target/39767, tree-optimization/39675,
	tree-optimization/39764

* Tue Apr 14 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.34
- update from gcc-4_4-branch
  - GCC 4.4.0-rc1
  - license changes to GPLv3+ with GCC Runtime Exception for most of the
    lib* files
  - PRs c++/28301, c++/39480, c++/39742, c++/39750, c/39613, c/39614, c/39673,
	libobjc/36610, target/39740, testsuite/35621, tree-optimization/39713
- fix another -Wshadow C++ issue (PR c++/39763)

* Thu Apr  9 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.32
- update from gcc-4_4-branch
  - PRs c++/34691, c++/35146, c++/35240, c++/37806, c++/38030, c++/38850,
	c++/39608, c++/39637, c++/4926, c/37772, fortran/38152,
	fortran/39519, fortran/39594, libmudflap/38462, libstdc++/39310,
	middle-end/39573, objc/18456, objc/27377, other/39591,
	rtl-optimization/39588, rtl-optimization/39607, target/39501,
	target/39592, target/39634, testsuite/39325, tree-optimization/35011,
	tree-optimization/39595, tree-optimization/39648
  - handle .cfi_undefined(%ip) in libgcc_s unwinder (#491542)
- fix debug info for C++ static data members (#410691)
- revert fwprop fix, it causes glibc.i586 miscompilation

* Mon Mar 30 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.31
- update from gcc-4_4-branch
  - PR target/39545
  - fix Fortran bind(c) function using RESULT() (#492657)
- fix bogus warnings on strcmp/strncmp macros (#492846)

* Sat Mar 28 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.30
- update from gcc-4_4-branch
  - PRs c++/39380, c++/28274, c++/29727, c++/35652, c++/36799, c++/37647,
	c++/38638, c++/39554, libfortran/39528, middle-end/39497,
	rtl-optimization/39522, target/38034, target/39523,
	tree-optimization/39529, tree-optimization/39548,
	tree-optimization/39557
- emit debuginfo for block local externs in C (PR debug/39563)
- fix -maltivec conditional vector macro (PR target/39558)
- teach fwprop to handle asm (PR inline-asm/39543)

* Tue Mar 24 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.29
- update from trunk
  - PRs c++/28879, c++/37729, c++/39526, debug/39524, tree-optimization/39516

* Thu Mar 19 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.28
- update from trunk
  - PRs c++/39425, c++/39475, c/39495, debug/39485, middle-end/37805,
	middle-end/38609, middle-end/39378, middle-end/39447,
	middle-end/39500, target/35180, target/39063, target/39496
  - fix RA bug with global reg variables (#490509)
- use DW_LANG_C99 for -std=c99 or -std=gnu99 compiled C code (PR debug/38757)
- emit DW_AT_explicit when needed (PR debug/37959)
- optimize memmove into memcpy in more cases when we can prove src and dest
  don't overlap

* Tue Mar 17 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.27
- update from trunk
  - PRs debug/37890, debug/39471, debug/39474, libstdc++/39405, target/34299,
	target/39473, target/39476, target/39477, target/39482,
	testsuite/37628, testsuite/37630, testsuite/37960, testsuite/38526,
	tree-optimization/39455

* Sat Mar 14 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.26
- fix ppc64 regression caused by the power7 backport (#490149,
  PR target/39457)

* Fri Mar 13 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.25
- update from trunk
  - PRs debug/39086, debug/39432, libobjc/27466, middle-end/37850,
	target/39137, target/39181, target/39431, target/39445, target/5362,
	testsuite/39451, tree-optimization/39422
- fix ICE in gen_tagged_type_instantiation_die (#489308, PR debug/39412)
- fix memcmp builtin asm redirection (PR middle-end/39443)
- fix sparcv9 profiledbootstrap (PR bootstrap/39454)

* Thu Mar 12 2009 Dennis Gilmore <dennis@ausil.us>
- don't build with graphite support on sparc arches
  - still missing some deps

* Tue Mar 10 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.24
- update from trunk
  - PRs ada/39221, c++/39060, c++/39367, c++/39371, libfortran/39402,
	middle-end/38028, target/39361, tree-optimization/39394
- use system cloog-ppl instead of building a private libcloog.so.0 (#489183)
- preliminary Power7 support (#463846)

* Sat Mar  7 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.23
- update from trunk
  - PRs c++/13549, c++/29469, c++/29607, c++/33492, c++/37520, c++/38908,
	c++/9634, debug/39372, middle-end/39360, rtl-optimization/39235,
	testsuite/39357, tree-optimization/39349
  - emit DW_TAG_imported* even in main or in lexical blocks that
    contain no automatic variables (#488547, PR debug/39379)
  - fix DW_AT_decl_line on DW_TAG_imported* (#488771, PR debug/39387)
  - fix SCCVN with SSA names occurring in abnormal PHIs (#488061,
    PR tree-optimization/39362)

* Wed Mar  4 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.22
- update from trunk
  - PRs ada/39172, ada/39264, bootstrap/39257, c++/36411, c++/37789,
	c++/38880, c++/39225, c++/39242, c/12245, classpath/38417,
	classpath/38912, debug/39267, debug/39285, fortran/38914,
	fortran/39292, fortran/39295, fortran/39309, fortran/39354,
	libgcj/38861, middle-end/10109, middle-end/34443,
	middle-end/39157, middle-end/39272, middle-end/39308,
	middle-end/39335, middle-end/39345, rtl-optimization/39241,
	target/33785, target/35965, target/39256, target/39261,
	target/39327, testsuite/38164, tree-optimization/37709,
	tree-optimization/39248, tree-optimization/39259,
	tree-optimization/39260, tree-optimization/39318,
	tree-optimization/39331, tree-optimizations/39259,
	tree-optimization/39358
  - fix ivopts (#486088, PR tree-optimization/39233)
  - fix SRA (#487795, PR tree-optimization/39339)
  - fix __builtin_object_size with unions (#487702,
    PR tree-optimization/39343)
- fix ppc -m64 -O2 -mtune=cell and patterns (#485067, PR target/39226)
- -march=atom/-mtune=atom support from ix86/atom branch

* Thu Feb 19 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.21
- update from trunk
  - PRs c++/39188, c++/39219, c/35447, c/38483, target/34587,
	target/38891, target/39082, target/39179, target/39224,
	target/39228, testsuite/38165, testsuite/38166,
	tree-optimization/36922, tree-optimization/39074,
  - another bogus aliasing warning fix (#485463, PR tree-optimization/39207)
- fix tail call optimization on ppc (#485067, PR target/39240)

* Tue Feb 17 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.20
- update from trunk
  - PRs c/35446, middle-end/39214, tree-optimization/39202
  - fix ICE in compute_attic (#485708, PR tree-optimization/39204)
  - fix bogus aliasing warning (#485463, PR tree-optimization/39207)
- update for i386.rpm -> i586.rpm switch

* Mon Feb 16 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.19
- update from trunk
  - PRs c++/39070, fortran/36528, fortran/36703, fortran/38259,
	libstdc++/39168, target/37049, target/38056, target/39149,
	target/39162, target/39196
  - ix86 peephole fix (#485729, PR target/39152)
  - uglify function parameter names in gthr*.h (#485619)

* Fri Feb 13 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.18
- update from trunk
  - PRs c++/30111, c++/38950, c++/39153, c/35444, middle-end/39154,
	target/38824, target/39152
- fix ICE on ppc32 with -fpic -fvisibility=hidden (#485232, PR target/39175)

* Wed Feb 11 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.17
- update from trunk
  - fix ICE on xen (PR target/39139)
  - PRs c++/34397, c++/35147, c++/36744, c++/37737, c++/38649, c++/39109,
	c/35434, c/36432, c/39035, c/39084, middle-end/35202,
	middle-end/38953, middle-end/38981, middle-end/39124,
	middle-end/39127, target/39118, target/39119, testsuite/33300,
	tree-optimization/39132
- force emitting .debug_info for empty CUs with -g3 (#479912)

* Fri Feb  6 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.16
- update from trunk
  - don't emit thunks for versioned functions (PR c++/39106)
  - fix -fstrict-aliasing miscompilation (PR tree-optimization/39100)

* Wed Feb  4 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.15
- update from trunk
  - C++ mangling fix (PR c++/39095)
  - only complain about calling main in C++ if -pedantic
- add raw string support

* Tue Feb  3 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.14
- update from trunk
- when compiling with -march=i386, don't use __sync_* builtins in
  ext/atomicity.h

* Wed Jan 28 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.13
- fix graphite make check

* Tue Jan 27 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.12
- update from trunk
- add graphite support
- change gcc default ISA and tuning:
  i386 and x86_64 -m32:
  -march=i586 -mtune=generic from -march=i386 -mtune=generic
  x86_64 -m64 remains at:
  -march=x86-64 -mtune=generic
  s390 and s390x -m31:
  -march=z9-109 -mtune=z10 from -march=g5 -mtune=z9-109
  s390x -m64:
  -march=z9-109 -mtune=z10 from -march=z900 -mtune=z9-109

* Wed Jan 21 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.9
- rebuilt without ppc64 ada bootstrap hacks

* Tue Jan 20 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.8
- attempt to enable Ada support on ppc64

* Fri Jan 16 2009 Jakub Jelinek <jakub@redhat.com> 4.4.0-0.3
- initial 4.4 package, using newly created redhat/gcc-4_4-branch
