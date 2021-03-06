%define _topdir   .
%define buildroot ./builddir

Name:   tis-waptagent
Version:        %{_version}
Release:        %{waptedition}%{?dist}
Summary:        WAPT Agent
BuildArch:      x86_64
Conflicts:      tis-waptserver

Group:          Development/Tools
License:        %{licence}
URL:            https://wapt.fr
Source0:        ./waptagent/
Prefix:         /opt

Requires: dialog policycoreutils-python

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
# to be cleanedup
%global __provides_exclude_from /
%global __requires_exclude_from /

%description

%clean
echo "No clean"

%build
%define is_enterprise %( if [ '%{waptedition}' = 'enterprise' ]; then echo 1; else echo 0; fi; )

%install
set -e

mkdir -p %{buildroot}/opt/wapt

mkdir -p %{buildroot}/usr/lib/systemd/

(cd .. && python2 ./createrpm.py)

%files
%defattr(644,root,root,755)
/usr/lib/systemd/system/waptservice.service
/etc/profile.d/wapt_session_setup.sh
/opt/wapt/waptservice
/opt/wapt/lib
/opt/wapt/lib64
/usr/bin/waptpython
/etc/logrotate.d/waptservice
/etc/rsyslog.d/waptservice.conf
/opt/wapt/waptpackage.py*
/opt/wapt/version-full
/opt/wapt/waptcrypto.py*
/opt/wapt/common.py*
/opt/wapt/waptutils.py*
/opt/wapt/custom_zip.py*
/opt/wapt/wapt-get.py*
/opt/wapt/templates
%if %is_enterprise
/opt/wapt/waptenterprise
%endif

%attr(755,root,root)/opt/wapt/bin/
%attr(755,root,root)/opt/wapt/runwaptservice.sh
%attr(755,root,root)/opt/wapt/wapt-get.sh
%attr(755,root,root)/opt/wapt/setuphelpers.py*
%attr(755,root,root)/opt/wapt/setuphelpers_linux.py*
%attr(755,root,root)/opt/wapt/setuphelpers_unix.py*
%attr(755,wapt,root)/opt/wapt/conf
%attr(755,wapt,root)/opt/wapt/db
%attr(755,wapt,root)/opt/wapt/log

%pre
echo "No preinst"

%postun

if [ "$1" = 0 ] ; then
    rm -f /usr/bin/waptservice
    rm -f /usr/bin/wapt-get
fi

%post
systemctl enable  waptservice
touch /var/log/waptservice.log
touch /var/run/waptservice.pid
chown root:root /var/log/waptservice.log
chmod 640 /var/log/waptservice.log

find /opt/wapt -type f -exec chmod 644 {} +
find /opt/wapt -type d ! -name conf ! -name log -exec chmod 755 {} +
find /opt/wapt -type d ! -name conf ! -name log -exec chown root:root {} +
chown -R root:root /opt/wapt/conf
chown -R root:root /opt/wapt/db
chmod 750 /opt/wapt/conf
chown -R root:root /opt/wapt/log
chmod 755 /opt/wapt/log
chmod 755 /opt/wapt/bin/*
chmod 755 /opt/wapt/runwaptservice.sh
chmod 755 /usr/bin/waptpython
chmod 755 /opt/wapt/wapt-get.sh
mkdir -p /opt/wapt/ssl/server
mkdir -p /opt/wapt/private
chown root -R /opt/wapt/private
chmod 700 -R /opt/wapt/private


ln -sf /opt/wapt/runwaptservice.sh /usr/bin/waptservice
ln -sf /opt/wapt/wapt-get.sh /usr/bin/wapt-get

cat << EOF > /opt/wapt/.profile
# for python virtualenv
export PYTHONHOME=/opt/wapt
export PYTHONPATH=/opt/wapt
export PATH=/opt/wapt/bin:$PATH
EOF

FILE=/opt/wapt/wapt-get.ini
if [[ -f "$FILE" ]]; then
    systemctl restart waptservice.service || true
fi

### end
