%define pkgname Event-ExecFlow
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1

Name:      perl-Event-ExecFlow
Summary:   Event-RPC - High level API for event-based execution flow control
Version:   0.63
Release:   %mkrel 1
License:   Artistic
Group:     Development/Perl
URL:       http://www.exit1.org/Event-ExecFlow/
SOURCE:    http://search.cpan.org/CPAN/authors/id/J/JR/JRED/Event-ExecFlow-%version.tar.bz2
Buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
Buildarch: noarch
BuildRequires: perl-devel
BuildRequires: perl-AnyEvent
BuildRequires: perl-libintl-perl

%description
Event::ExecFlow provides a ligh level API for defining complex flow
controls with asynchronous execution of external programs.

%prep
%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

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

