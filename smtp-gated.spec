%define user smtpgw

Summary: SMTP Transparent Proxy
Name: smtp-gated
Version: 1.4.17
Release: 0
Group: System/Servers
License: GNU GPL
Vendor: Bartlomiej Korupczynski <bartek@klolik.org>
#Requires: spamassassin-spamd clamd libpcre libspf
Requires:  libspf
#BuildRequires: libpcre-devel libspf-devel
BuildRequires: libspf-devel
Provides: smtp-proxy
URL: http://smtp-proxy.klolik.org
Source: http://software.klolik.org/smtp-gated/files/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Transparent proxy for SMTP traffic.

%prep
%setup -q -n %{name}-%{version}


%build
%configure --disable-pcre
%make

%install
%makeinstall

install -d $RPM_BUILD_ROOT{/var/spool/%{name}/{msg,lock}}
install -d $RPM_BUILD_ROOT/var/run/%{name}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

install contrib/redhat.init $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

src/%{name} -t | sed 's/^\([^#]\)/; &/' > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

pushd $RPM_BUILD_ROOT

mkdir -p var/spool/%{name}/msg
mkdir -p var/spool/%{name}/lock
mkdir -p var/run/%{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README README.PL
%doc contrib/fixed.conf contrib/nat.conf
%config(noreplace)	%{_sysconfdir}/%{name}.conf
%{_mandir}

%defattr(0755,root,root,0755)
%{_sbindir}/%{name}
/etc/rc.d/init.d/%{name}

%defattr(0750,smtpgw,smtpgw,0750)
/var/spool/%{name}
/var/run/%{name}


%pre
id %{user} >/dev/null 2>&1 && exit 0

groupadd -r -f %{user} || {
	echo "Group %{user} account could not be created" >&2
	exit 1
}

useradd -g %{user} -d /var/spool/%{name}/ -s /bin/false -c "SMTP Proxy" -M -n -r %{user} || {
	echo "User %{user} account could not be created" >&2
	exit 1
}


%post
chkconfig --add %{name}
/etc/rc.d/init.d/%{name} condrestart

%preun
if [ $1 == 0 ]; then
        /etc/rc.d/init.d/%{name} stop >/dev/null 2>&1
        chkconfig --del %{name}
fi
