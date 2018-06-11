Name:		startup
Version: 	0.1
Release:	1%{?dist}
Summary: 	A collection of configuration changes

Group:		NTI-320
License:	GPL2+
URL:		https://github.com/nic-instruction/hello-NTI-320
Source0:        https://github.com/nic-instruction/hello-NTI-320/startup-0.1.tar.gz

BuildRequires:	gcc, python >= 1.3
Requires:	bash, net-snmp, net-snmp-utils, nrpe, nagios-plugins-all

%description
This package contains customization for a monitoring server, a trending server and a   logserver on the nti320 network.

%prep
%setup -q	
		
%build					
%define _unpackaged_files_terminate_build 0

%install

rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib64/nagios/plugins/
mkdir -p %{buildroot}/etc/nrpe.d/

install -m 0755 nti-sanity.sh %{buildroot}/usr/lib64/nagios/plugins/

install -m 0744 nti320.cfg %{buildroot}/etc/nrpe.d/

%clean

%files					
%defattr(-,root,root)	
/usr/lib64/nagios/plugins/nti-sanity.sh


%config
/etc/nrpe.d/nti320.cfg

%doc			



%post

touch /thisworked
systemctl enable snmpd
systemctl start snmpd
sed -i 's,/dev/hda1,/dev/sda1,'  /etc/nagios/nrpe.cfg


# nrpe client ##
apt-get install -y nagios-nrpe-server nagios-plugins
sed -i 's/allowed_hosts=127.0.0.1/allowed_hosts=127.0.0.1, 10.142.0.15/g' /etc.nagios/nrpe.cfg
/etc/init.d/nagios-nrpe-server restart
wget https://raw.githubusercontent.com/carlosaguilar1928/Monitoring-/master/check_mem.sh
mv check_mem.sh /usr/lib/nagios/plugins
sed -i "s,command[check_hda1]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /dev/hda1,command[check_disk]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /dev/sda1,g" /etc/nagios/nrpe.cfg
echo "command[check_mem]=/usr/lib/nagios/plugins/check_mem.sh -w 80 -c 90" >> /etc/nagios/nrpe.cfg
/etc/init.d/nagios-nrpe-server restart

#rsyslog 
echo "*.info;mail.none;authpriv.none;cron.none   @10.142.0.11" >> /etc/rsyslog.conf && systemctl restart rsyslog.service



#snmp
sudo su       
yum install -y net-snmp
systemctl enable snmpd
systemctl start snmpd
yum install -y net-snmp-utils















%postun
rm /thisworked
rm /etc/nrpe.d/nti320.cfg
%changelog				# changes you (and others) have made and why
