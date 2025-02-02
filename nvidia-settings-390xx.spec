Name:           nvidia-settings-390xx
Version:        390.157
Release:        5%{?dist}
Summary:        Configure the NVIDIA 390xx series graphics driver

License:        GPLv2+
URL:            https://download.nvidia.com/XFree86/nvidia-settings/
Source0:        %{url}/nvidia-settings-%{version}.tar.bz2
Source1:        nvidia-settings-user.desktop
Source2:        nvidia-settings-390xx.appdata.xml
Patch0:         https://github.com/NVIDIA/nvidia-settings/commit/a7c1f5fce6303a643fadff7d85d59934bd0cf6b6.patch#/gcc-10.patch

ExclusiveArch:  x86_64 armv7hl

Conflicts:      nvidia-settings

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  hostname

BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  libappstream-glib
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
%autosetup -p1 -n nvidia-settings-%{version}
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

# Fix appdata conflict with nvidia main
mv %{buildroot}%{_datadir}/applications/nvidia-settings.desktop \
 %{buildroot}%{_datadir}/applications/nvidia-settings-390xx.desktop
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/nvidia-settings-390xx.desktop

# Pixmap installation
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -pm 0644 doc/nvidia-settings.png \
  %{buildroot}%{_datadir}/pixmaps

# User settings installation
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
install -pm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/nvidia-settings-user.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/nvidia-settings-user.desktop

# AppData installation
mkdir -p %{buildroot}%{_metainfodir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

%ldconfig_scriptlets


%files
%doc doc/*.txt
%config %{_sysconfdir}/xdg/autostart/nvidia-settings-user.desktop
%{_bindir}/nvidia-settings
%{_libdir}/libnvidia-gtk3.so.*
%exclude %{_libdir}/libnvidia-gtk2.so.*
%{_datadir}/pixmaps/nvidia-settings.png
%{_datadir}/applications/nvidia-settings-390xx.desktop
%{_metainfodir}/nvidia-settings-390xx.appdata.xml
%{_mandir}/man1/nvidia-settings.1.*


%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 390.157-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 390.157-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 390.157-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 390.157-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 28 2022 Leigh Scott <leigh123linux@gmail.com> - 390.154-1
- Update to 390.154

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 390.151-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Sat Jun 18 2022 Henrik Nordstrom <henrik@henriknordstrom.net> - 390.151-1
- Update to 390.151

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 390.147-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 29 2022 Henrik Nordstrom <henrik@henriknordstrom.net> - 390.147-1
- Update to 390.147

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 390.144-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 23 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 390.144-1
- Update to 390.144

* Tue Apr 20 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 390.143-1
- Update to 390.143

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 390.141-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 390.141-1
- Update to 390.141

* Sun Sep 20 2020 Leigh Scott <leigh123linux@gmail.com> - 390.138-4
- Use 390xx in appdata name

* Sun Sep 20 2020 Leigh Scott <leigh123linux@gmail.com> - 390.138-3
- Fix appdata conflict with nvidia main

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 390.138-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Leigh Scott <leigh123linux@gmail.com> - 390.138-1
- Update to 390.138

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 390.132-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 09 2019 Leigh Scott <leigh123linux@gmail.com> - 390.132-1
- Update to 390.132

* Tue Aug 06 2019 Leigh Scott <leigh123linux@gmail.com> - 390.129-1
- Update to 390.129

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 390.116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 390.116-1
- Update to 390.116

* Sun Oct 7 2018 Richard Shaw <hobbes1069@gmail.com> - 390.87-1
- Initial packaging of 390.87 series.
