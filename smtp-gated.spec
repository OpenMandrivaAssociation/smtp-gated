%define user smtpgw

Summary:	SMTP Transparent Proxy
Name: 		smtp-gated
Version: 	1.4.17
Release: 	%mkrel 2
Group: 		System/Servers
License:	GPL2v+
#Requires: spamassassin-spamd clamd libpcre libspf2
#BuildRequires: libpcre-devel libspf2-devel
Provides: 	smtp-proxy
URL: 		http://smtp-proxy.klolik.org
Source0: 	http://software.klolik.org/smtp-gated/files/%{name}-%{version}.tar.gz
Source1:	smtp-gated.init
Patch0: 	smtp-gated-1.4.17-fdprintf.patch
Patch1: 	smtp-gated-1.4.17-syslog.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

%description
Transparent proxy for SMTP traffic.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .fdprintf
%patch1 -p0 -b .syslog
%build
%configure --disable-pcre --disable-spf
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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README README.PL
%doc contrib/fixed.conf contrib/nat.conf
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}

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
