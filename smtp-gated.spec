%define user smtpgw

Summary:	SMTP Transparent Proxy
Name: 		smtp-gated
Version: 	1.4.17
Release: 	7
Group: 		System/Servers
License:	GPL2v+
#Requires: spamassassin-spamd clamd libpcre libspf2
BuildRequires:  pcre-devel 
BuildRequires:  libspf2-devel
Provides: 	smtp-proxy
URL: 		https://smtp-proxy.klolik.org
Source0: 	http://software.klolik.org/smtp-gated/files/%{name}-%{version}.tar.gz
Source1:	smtp-gated.init
Patch0: 	smtp-gated-1.4.17-fdprintf.patch
Patch1: 	smtp-gated-1.4.17-syslog.patch
Patch2:		smtp-gated-1.4.17-linkage.patch
Requires(pre):		rpm-helper
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper

%description
Transparent proxy for SMTP traffic.

%prep
%setup -q
%patch0 -p0 -b .fdprintf
%patch1 -p0 -b .syslog
%patch2 -p0 -b .linkage
%build
%configure --enable-pcre=%{_includedir} --enable-spf=%{_includedir}/spf2

%make

%install
%makeinstall

install -d %{buildroot}{/var/spool/%{name}/{msg,lock}}
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}%{_initrddir}

install %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

src/%{name} -t | sed 's/^\([^#]\)/; &/' > %{buildroot}%{_sysconfdir}/%{name}.conf

mkdir -p %{buildroot}/var/spool/%{name}/msg
mkdir -p %{buildroot}/var/spool/%{name}/lock
mkdir -p %{buildroot}/var/run/%{name}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README README.PL
%doc contrib/fixed.conf contrib/nat.conf
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}/man*/*

%defattr(0755,root,root,0755)
%{_sbindir}/%{name}
%{_initrddir}/%{name}

%defattr(0750,smtpgw,smtpgw,0750)
/var/spool/%{name}
/var/run/%{name}

%pre
%_pre_useradd %{user} /var/spool/%{name} /bin/false

%postun
%_postun_userdel %{user}
%_postun_groupdel %{user}

%preun
%_preun_service %{name}

%post
%_post_service %{name}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.17-5mdv2012.0
+ Revision: 773077
- relink against libpcre.so.1

* Mon May 30 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.4.17-4
+ Revision: 681778
- Rebuild

* Mon May 30 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.4.17-3
+ Revision: 681768
- P2 to let gcc link

* Fri Mar 25 2011 zamir <zamir@mandriva.org> 1.4.17-2
+ Revision: 648514
- add rebuild init file
- cosmetic fix

* Tue Mar 22 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.4.17-1
+ Revision: 647595
- cosmetics

* Tue Mar 22 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.4.17-0
+ Revision: 647594
- P1 syslog patch
- add p0 to fix fdprintf sintax

  + zamir <zamir@mandriva.org>
    - del vendor
    - first build
    - create smtp-gated

