Name:           nvidia-settings-390xx
Version:        390.129
Release:        1%{?dist}
Summary:        Configure the NVIDIA 390xx series graphics driver

License:        GPLv2+
URL:            https://download.nvidia.com/XFree86/nvidia-settings/
Source0:        %{url}/nvidia-settings-%{version}.tar.bz2
Source1:        nvidia-settings-user.desktop
Source2:        nvidia-settings.appdata.xml

ExclusiveArch:  i686 x86_64 armv7hl

Conflicts:      nvidia-settings

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  hostname

BuildRequires:  gtk2-devel
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires:  gtk3-devel
BuildRequires:  libappstream-glib
%endif
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  libvdpau-devel
BuildRequires:  m4
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(dbus-1)


%description
The nvidia-settings utility is a tool for configuring the NVIDIA graphics
driver.  It operates by communicating with the NVIDIA X driver, querying
and updating state as appropriate.

This communication is done with the NV-CONTROL X extension.
nvidia-settings is compatible with driver %{version}.


%prep
%autosetup -n nvidia-settings-%{version}
# We are building from source
rm -rf src/libXNVCtrl/libXNVCtrl.a

sed -i -e 's|/usr/local|%{_prefix}|g' utils.mk
sed -i -e 's|/lib$|/%{_lib}|g' utils.mk
sed -i -e 's|-lXxf86vm|-lXxf86vm -ldl -lm|g' Makefile


%build
# no job control
export CFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"
pushd src/libXNVCtrl
  make \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  X_CFLAGS="${CFLAGS}"

popd
make  \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  STRIP_CMD=true NV_KEEP_UNSTRIPPED_BINARIES=1 \
  X_LDFLAGS="-L%{_libdir}" \
  CC_ONLY_CFLAGS="%{optflags}"
(cd src/_out/Linux_*/ ; for i in nvidia-settings libnvidia-gtk{2,3}.so ; do cp $i.unstripped $i; done ; cd -)


%install
%make_install

# Desktop entry for nvidia-settings
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 doc/nvidia-settings.desktop \
  %{buildroot}%{_datadir}/applications

sed -i -e 's|__UTILS_PATH__/||' -e 's|__PIXMAP_PATH__/||' \
  -e 's|nvidia-settings.png|nvidia-settings|' \
  -e 's|__NVIDIA_SETTINGS_DESKTOP_CATEGORIES__|System;Settings;|' \
  %{buildroot}%{_datadir}/applications/nvidia-settings.desktop

desktop-file-validate \
  %{buildroot}%{_datadir}/applications/nvidia-settings.desktop

# Pixmap installation
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -pm 0644 doc/nvidia-settings.png \
  %{buildroot}%{_datadir}/pixmaps

# User settings installation
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
install -pm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/nvidia-settings-user.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/nvidia-settings-user.desktop

%if 0%{?fedora}
# AppData installation
mkdir -p %{buildroot}%{_metainfodir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
%endif

%ldconfig_scriptlets


%files
%doc doc/*.txt
%config %{_sysconfdir}/xdg/autostart/nvidia-settings-user.desktop
%{_bindir}/nvidia-settings
%{_libdir}/libnvidia-gtk?.so.*
%if 0%{?fedora} || 0%{?rhel} > 6
%exclude %{_libdir}/libnvidia-gtk2.so.*
%endif
%{_datadir}/pixmaps/nvidia-settings.png
%{_datadir}/applications/nvidia-settings.desktop
%if 0%{?fedora}
%{_metainfodir}/nvidia-settings.appdata.xml
%endif
%{_mandir}/man1/nvidia-settings.1.*


%changelog
* Tue Aug 06 2019 Leigh Scott <leigh123linux@gmail.com> - 390.129-1
- Update to 390.129

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 390.116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 390.116-1
- Update to 390.116

* Sun Oct 7 2018 Richard Shaw <hobbes1069@gmail.com> - 390.87-1
- Initial packaging of 390.87 series.
