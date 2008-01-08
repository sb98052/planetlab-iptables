#
# $Id: iproute.spec 7668 2008-01-08 11:49:43Z thierry $
#
%define url $URL: svn+ssh://thierry@svn.planet-lab.org/svn/iproute2/trunk/iproute.spec $

%define name iptables
%define version 1.3.8
%define taglevel 0

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %(echo %{url} | cut -d ' ' -f 2)

%define build_devel 1
%define linux_header 0

Summary: Tools for managing Linux kernel packet filtering capabilities.
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://www.netfilter.org/%{name}-%{version}.tar.bz2
%define SOURCE1 iptables.init
%define SOURCE2 iptables-config
Group: System Environment/Base
#URL: http://www.netfilter.org/
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL
BuildPrereq: /usr/bin/perl
Requires: kernel >= 2.4.20
Requires(post,postun): chkconfig
Prefix: %{_prefix}
BuildRequires: kernel-devel

%package ipv6
Summary: IPv6 support for iptables.
Group: System Environment/Base
Requires: %{name} = %{version}

%if %{build_devel}
%package devel
Summary: Development package for iptables.
Group: System Environment/Base
Requires: %{name} = %{version}
%endif

%description
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.

%description ipv6
The iptables package contains IPv6 (the next version of the IP
protocol) support for iptables. Iptables controls the Linux kernel
network packet filtering code, allowing you to set up firewalls and IP
masquerading. 

Install iptables-ipv6 if you need to set up firewalling for your
network and you are using ipv6.

%if %{build_devel}
%description devel
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.
%endif

%prep
rm -rf %{buildroot}

%setup -q

# Put it to a reasonable place
find . -type f -exec perl -pi -e "s,/usr,%{prefix},g" {} \;

%build
TOPDIR=`pwd`
OPT="$RPM_OPT_FLAGS -I$TOPDIR/include"

%define KERNEL %(rpm -q --qf '%%{VERSION}-%%{RELEASE}-%%{ARCH}\\n' kernel-devel | tail -n 1 )
count=$(rpm -q kernel-devel| wc -l)
if [ $count -gt 1 ] ; then
	echo "WARNING: choosing kernel-devel-%{KERNEL}"
	echo "  but there are other kernel-devel packages installed: $(rpm -q kernel-devel)"
fi
	
%define KERNEL_DIR "/usr/src/kernels/%{KERNEL}"

make COPT_FLAGS="$OPT" KERNEL_DIR=%{KERNEL_DIR} LIBDIR=/%{_lib}
make COPT_FLAGS="$OPT" KERNEL_DIR=%{KERNEL_DIR} LIBDIR=/%{_lib} iptables-save iptables-restore
make COPT_FLAGS="$OPT" KERNEL_DIR=%{KERNEL_DIR} LIBDIR=/%{_lib} ip6tables-save ip6tables-restore

%install
make install DESTDIR=%{buildroot} KERNEL_DIR=%{KERNEL_DIR} BINDIR=/sbin LIBDIR=/%{_lib} MANDIR=%{_mandir}
%if %{build_devel}
make install-devel DESTDIR=%{buildroot} KERNEL_DIR=%{KERNEL_DIR} BINDIR=/sbin LIBDIR=%{_libdir} MANDIR=%{_mandir} INCDIR=%{_includedir}
%endif
cp ip{6,}tables-{save,restore} $RPM_BUILD_ROOT/sbin
cp iptables-*.8 $RPM_BUILD_ROOT%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -c -m755 %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/iptables
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE1} > ip6tables.init
install -c -m755 ip6tables.init $RPM_BUILD_ROOT/etc/rc.d/init.d/ip6tables
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
install -c -m755 %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/iptables-config
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE2} > ip6tables-config
install -c -m755 ip6tables-config $RPM_BUILD_ROOT/etc/sysconfig/ip6tables-config

%clean
rm -rf $RPM_BUILD_ROOT 

%post
/sbin/chkconfig --add iptables

%preun
if [ "$1" = 0 ]; then
	/sbin/chkconfig --del iptables
fi

%post ipv6
/sbin/chkconfig --add ip6tables

%preun ipv6
if [ "$1" = 0 ]; then
	/sbin/chkconfig --del ip6tables
fi

%files
%defattr(-,root,root,0755)
%doc COPYING INSTALL INCOMPATIBILITIES
%config %attr(0755,root,root) /etc/rc.d/init.d/iptables
%config(noreplace) %attr(0600,root,root) /etc/sysconfig/iptables-config
/sbin/iptables*
%{_mandir}/man8/iptables*
%dir /%{_lib}/iptables
/%{_lib}/iptables/libipt*
/sbin/ipset*
%{_mandir}/man8/ipset*
%dir /%{_lib}/ipset
/%{_lib}/ipset/libipset*

%files ipv6
%defattr(-,root,root,0755)
%config %attr(0755,root,root) /etc/rc.d/init.d/ip6tables
%config(noreplace) %attr(0600,root,root) /etc/sysconfig/ip6tables-config
/sbin/ip6tables*
%{_mandir}/man8/ip6tables*
/%{_lib}/iptables/libip6t*

%if %{build_devel}
%files devel
%defattr(-,root,root,0755)
%{_includedir}/libipq.h
%{_libdir}/libipq.a
#%{_libdir}/libiptc.a
%{_mandir}/man3/*
%endif

%changelog
* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Thomas Woerner <twoerner@redhat.com> 1.2.9-2.3
- fixed iptables-restore -c fault if there are no counters (#116421)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan  25 2004 Dan Walsh <dwalsh@redhat.com> 1.2.9-1.2
- Close File descriptors to prevent SELinux error message

* Wed Jan  7 2004 Thomas Woerner <twoerner@redhat.com> 1.2.9-1.1
- rebuild

* Wed Dec 17 2003 Thomas Woerner <twoerner@redhat.com> 1.2.9-1
- vew version 1.2.9
- new config options in ipXtables-config:
  IPTABLES_MODULES_UNLOAD
- more documentation in ipXtables-config
- fix for netlink security issue in libipq (devel package)
- print fix for libipt_icmp (#109546)

* Thu Oct 23 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-13
- marked all messages in iptables init script for translation (#107462)
- enabled devel package (#105884, #106101)
- bumped build for fedora for libipt_recent.so (#106002)

* Tue Sep 23 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-12.1
- fixed lost udp port range in ip6tables-save (#104484)
- fixed non numeric multiport port output in ipXtables-savs

* Mon Sep 22 2003 Florian La Roche <Florian.LaRoche@redhat.de> 1.2.8-11
- do not link against -lnsl

* Wed Sep 17 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-10
- made variables in rmmod_r local

* Tue Jul 22 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-9
- fixed permission for init script

* Sat Jul 19 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-8
- fixed save when iptables file is missing and iptables-config permissions

* Tue Jul  8 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-7
- fixes for ip6tables: module unloading, setting policy only for existing 
  tables

* Thu Jul  3 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-6
- IPTABLES_SAVE_COUNTER defaults to no, now
- install config file in /etc/sysconfig
- exchange unload of ip_tables and ip_conntrack
- fixed start function

* Wed Jul  2 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-5
- new config option IPTABLES_SAVE_ON_RESTART
- init script: new status, save and restart
- fixes #44905, #65389, #80785, #82860, #91040, #91560 and #91374

* Mon Jun 30 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-4
- new config option IPTABLES_STATUS_NUMERIC
- cleared IPTABLES_MODULES in iptables-config

* Mon Jun 30 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-3
- new init scripts

* Sat Jun 28 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove check for very old kernel versions in init scripts
- sync up both init scripts and remove some further ugly things
- add some docu into rpm

* Thu Jun 26  2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-2
- rebuild

* Mon Jun 16 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-1
- update to 1.2.8

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Bill Nottingham <notting@redhat.com> 1.2.7a-1
- update to 1.2.7a
- add a plethora of bugfixes courtesy Michael Schwendt <mschewndt@yahoo.com>

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 1.2.6a-3
- Fix multilib

* Wed Aug 07 2002 Karsten Hopp <karsten@redhat.de>
- fixed iptables and ip6tables initscript output, based on #70511
- check return status of all iptables calls, not just the last one
  in a 'for' loop.

* Mon Jul 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.6a-1
- 1.2.6a (bugfix release, #69747)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.5-3
- Add some fixes from CVS, fixing bug #60465

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.5-2
- Merge ip6tables improvements from Ian Prowell <iprowell@prowell.org>
  #59402
- Update URL (#59354)
- Use /sbin/chkconfig rather than chkconfig in %postun script

* Fri Jan 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.5-1
- 1.2.5

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-2
- Fix %preun script

* Tue Oct 30 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-1
- Update to 1.2.4 (various fixes, including security fixes; among others:
  #42990, #50500, #53325, #54280)
- Fix init script (#31133)

* Mon Sep  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-1
- 1.2.3 (5 security fixes, some other fixes)
- Fix updating (#53032)

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-4
- Fix #50990
- Add some fixes from current CVS; should fix #52620

* Mon Jul 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-3
- Add some fixes from the current CVS tree; fixes #49154 and some IPv6
  issues

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-2
- Fix iptables-save reject-with (#45632), Patch from Michael Schwendt
  <mschwendt@yahoo.com>

* Tue May  8 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-1
- 1.2.2

* Wed Mar 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.2.1a, fixes #28412, #31136, #31460, #31133

* Thu Mar  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Yet another initscript fix (#30173)
- Fix the fixes; they fixed some issues but broke more important
  stuff :/ (#30176)

* Tue Feb 27 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up initscript (#27962)
- Add fixes from CVS to iptables-{restore,save}, fixing #28412

* Fri Feb 09 2001 Karsten Hopp <karsten@redhat.de>
- create /etc/sysconfig/iptables mode 600 (same problem as #24245)

* Mon Feb 05 2001 Karsten Hopp <karsten@redhat.de>
- fix bugzilla #25986 (initscript not marked as config file)
- fix bugzilla #25962 (iptables-restore)
- mv chkconfig --del from postun to preun

* Thu Feb  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix check for ipchains

* Mon Jan 29 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Some fixes to init scripts

* Wed Jan 24 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add some fixes from CVS, fixes among other things Bug #24732

* Wed Jan 17 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add missing man pages, fix up init script (Bug #17676)

* Mon Jan 15 2001 Bill Nottingham <notting@redhat.com>
- add init script

* Mon Jan 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.2
- fix up ipv6 split
- add init script
- Move the plugins from /usr/lib/iptables to /lib/iptables.
  This needs to work before /usr is mounted...
- Use -O1 on alpha (compiler bug)

* Sat Jan  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.2
- Add IPv6 support (in separate package)

* Thu Aug 17 2000 Bill Nottingham <notting@redhat.com>
- build everywhere

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.1

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- move iptables to /sbin.
- excludearch alpha for now, not building there because of compiler bug(?)

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- don't obsolete ipchains either
- update to 1.1.0

* Mon Jun  4 2000 Bill Nottingham <notting@redhat.com>
- remove explicit kernel requirement

* Tue May  2 2000 Bernhard Rosenkränzer <bero@redhat.com>
- initial package
