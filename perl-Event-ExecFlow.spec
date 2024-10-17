%define pkgname Event-ExecFlow
%define filelist %{pkgname}-%{upstream_version}-filelist
%define NVR %{pkgname}-%{upstream_version}-%{release}
%define maketest 1
%define upstream_version 0.64

Name:      perl-Event-ExecFlow
Summary:   Event-RPC - High level API for event-based execution flow control
Version:   %perl_convert_version %upstream_version
Release:   5
License:   Artistic
Group:     Development/Perl
URL:       https://www.exit1.org/Event-ExecFlow/
SOURCE:    http://search.cpan.org/CPAN/authors/id/J/JR/JRED/Event-ExecFlow-%upstream_version.tar.bz2
Buildroot: %{_tmppath}/%{name}-%{upstream_version}-%(id -u -n)
Buildarch: noarch
BuildRequires: perl-devel
BuildRequires: perl-AnyEvent
BuildRequires: perl-libintl-perl

%description
Event::ExecFlow provides a ligh level API for defining complex flow
controls with asynchronous execution of external programs.

%prep
%setup -q -n %{pkgname}-%{upstream_version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{upstream_version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '` INSTALLDIRS=vendor
%{__make} 
%check
chmod 755 bin/*
%{__make} test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README Changes
%_bindir/execflow
%{perl_vendorlib}/Event/ExecFlow*
%_mandir/man3/Event::ExecFlow*



%changelog
* Fri Jan 20 2012 Götz Waschk <waschk@mandriva.org> 0.640.0-3mdv2012.0
+ Revision: 763021
- rebuild

* Tue Jul 26 2011 Götz Waschk <waschk@mandriva.org> 0.640.0-2
+ Revision: 691693
- rebuild

* Wed Jan 06 2010 Götz Waschk <waschk@mandriva.org> 0.640.0-1mdv2011.0
+ Revision: 486564
- update to new version 0.64

* Tue Jul 28 2009 Götz Waschk <waschk@mandriva.org> 0.630.0-1mdv2010.0
+ Revision: 401505
- use perl version macro

* Thu Jul 31 2008 Thierry Vignaud <tv@mandriva.org> 0.63-3mdv2009.0
+ Revision: 256812
- rebuild

* Thu Dec 20 2007 Olivier Blin <blino@mandriva.org> 0.63-1mdv2008.1
+ Revision: 135841
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Apr 17 2007 Götz Waschk <waschk@mandriva.org> 0.63-1mdv2007.1
+ Revision: 13562
- new version


* Sun Jun 18 2006 Götz Waschk <waschk@mandriva.org> 0.62-1mdk
- New release 0.62

* Mon Apr 03 2006 Götz Waschk <waschk@mandriva.org> 0.61-2mdk
- fix buildrequires
- fix URL

* Mon Apr 03 2006 Götz Waschk <waschk@mandriva.org> 0.61-1mdk
- initial package

