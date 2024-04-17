#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.0.4
%define		qtver		5.15.2
%define		kpname		breeze
Summary:	Artwork, styles and assets for the Breeze visual style for the Plasma Desktop
Name:		kp6-%{kpname}
Version:	6.0.4
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	2f67b472e4d64d65245f906fe051a482
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Quick-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	fftw3-devel
BuildRequires:	gettext-devel
BuildRequires:	hardlink >= 1.0-3
BuildRequires:	kf6-attica-devel
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-frameworkintegration-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kcodecs-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-kguiaddons-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	kp6-kdecoration-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	qt6-qmake
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{kpname}-cursor-theme = %{version}-%{release}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	kf6-breeze-icons
Requires:	kp6-breeze-data = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Artwork, styles and assets for the Breeze visual style for the Plasma
Desktop.

%package data
Summary:	Data files for %{kpname}
Summary(pl.UTF-8):	Dane dla %{kpname}
Group:		X11/Applications
BuildArch:	noarch

%description data
Data for %{kpname}.

%description data -l pl.UTF-8
Dane dla %{kpname}.

%package devel
Summary:	Breeze devel
Summary(pl.UTF-8):	Breeze devel
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description devel
Artwork, styles and assets for the Breeze visual style for the Plasma
Desktop. Devel files

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%package -n %{kpname}-cursor-theme
Summary:	Breeze cursor theme
Group:		Themes
Conflicts:	breeze-icon-theme < 5.4.0-7
Conflicts:	kp6-breeze < 5.4.0-5
BuildArch:	noarch

%description -n %{kpname}-cursor-theme
Breeze cursor theme.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DBUILD_QT6=ON \
	-DBUILD_QT5=OFF
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_iconsdir}/{breeze-dark,breeze}
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/icons/breeze_cursors
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/icons/Breeze_Snow

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/breeze-settings6
%attr(755,root,root) %{_libdir}/qt6/plugins/kstyle_config/breezestyleconfig.so
%attr(755,root,root) %{_libdir}/qt6/plugins/org.kde.kdecoration2.kcm/kcm_breezedecoration.so
%attr(755,root,root) %{_libdir}/qt6/plugins/org.kde.kdecoration2/org.kde.breeze.so
%attr(755,root,root) %{_libdir}/qt6/plugins/styles/breeze6.so

%files data -f %{kpname}.lang
%defattr(644,root,root,755)
%{_iconsdir}/hicolor/scalable/apps/breeze-settings.svgz
%dir %{_datadir}/QtCurve
%{_datadir}/QtCurve/Breeze.qtcurve
%dir %{_datadir}/color-schemes
%{_datadir}/color-schemes/BreezeDark.colors
%{_datadir}/kstyle/themes/breeze.themerc
%{_datadir}/wallpapers/Next
%{_datadir}/color-schemes/BreezeLight.colors
%{_datadir}/color-schemes/BreezeClassic.colors
%{_desktopdir}/breezestyleconfig.desktop
%{_desktopdir}/kcm_breezedecoration.desktop

%files -n %{kpname}-cursor-theme
%defattr(644,root,root,755)
%{_iconsdir}/breeze_cursors
%{_iconsdir}/Breeze_Light

%files devel
%defattr(644,root,root,755)
%{_libdir}/cmake/Breeze
