#
# Conditional build:
%bcond_with	tests	# test suite

%define		kdeplasmaver	6.4.3
%define		qt_ver		6.7.0
%define		kf_ver		6.5.0
%define		kpname		breeze
Summary:	Artwork, styles and assets for the Breeze visual style for the Plasma Desktop
Summary(pl.UTF-8):	Grafika, style i zasoby dla stylu Breeze środowiska Plasma Desktop
Name:		kp6-%{kpname}
Version:	6.4.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	ab7ff4225c75ba1112522b8b7a29896d
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Network-devel >= %{qt_ver}
BuildRequires:	Qt6OpenGL-devel >= %{qt_ver}
BuildRequires:	Qt6Quick-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-tools
BuildRequires:	hardlink >= 1.0-3
BuildRequires:	kf6-extra-cmake-modules >= 5.102.0
BuildRequires:	kf6-frameworkintegration-devel >= %{kf_ver}
BuildRequires:	kf6-kcmutils-devel >= %{kf_ver}
BuildRequires:	kf6-kcolorscheme-devel >= %{kf_ver}
BuildRequires:	kf6-kconfig-devel >= %{kf_ver}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kf_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kguiaddons-devel >= %{kf_ver}
BuildRequires:	kf6-ki18n-devel >= %{kf_ver}
BuildRequires:	kf6-kiconthemes-devel >= %{kf_ver}
BuildRequires:	kf6-kirigami-devel >= %{kf_ver}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kwindowsystem-devel >= %{kf_ver}
BuildRequires:	kp6-kdecoration-devel
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{kpname}-cursor-theme = %{version}-%{release}
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6DBus >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6Quick >= %{qt_ver}
Requires:	Qt6Widgets >= %{qt_ver}
Requires:	kf6-breeze-icons
Requires:	kf6-frameworkintegration >= %{kf_ver}
Requires:	kf6-kcmutils >= %{kf_ver}
Requires:	kf6-kcolorscheme >= %{kf_ver}
Requires:	kf6-kconfig >= %{kf_ver}
Requires:	kf6-kcoreaddons >= %{kf_ver}
Requires:	kf6-kguiaddons >= %{kf_ver}
Requires:	kf6-ki18n >= %{kf_ver}
Requires:	kf6-kiconthemes >= %{kf_ver}
Requires:	kf6-kirigami >= %{kf_ver}
Requires:	kf6-kwidgetsaddons >= %{kf_ver}
Requires:	kf6-kwindowsystem >= %{kf_ver}
Requires:	kp6-breeze-data = %{version}-%{release}
Obsoletes:	kp5-breeze < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Artwork, styles and assets for the Breeze visual style for the Plasma
Desktop.

%description -l pl.UTF-8
Grafika, style i zasoby dla stylu Breeze środowiska Plasma Desktop.

%package data
Summary:	Data files for %{kpname}
Summary(pl.UTF-8):	Dane dla %{kpname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Obsoletes:	kp5-breeze-data < 6
BuildArch:	noarch

%description data
Data for %{kpname}.

%description data -l pl.UTF-8
Dane dla %{kpname}.

%package devel
Summary:	Breeze development files
Summary(pl.UTF-8):	Pliki programistyczne stylu Breeze
Group:		Development
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-breeze-devel < 6

%description devel
Development files for Breeze style data.

%description devel -l pl.UTF-8
Pliki programistyczne danych stylu Breeze.

%package -n %{kpname}-cursor-theme
Summary:	Breeze cursor theme
Summary(pl.UTF-8):	Motyw kursora Breeze
Group:		Themes
Conflicts:	breeze-icon-theme < 5.4.0-7
Conflicts:	kp6-breeze < 5.4.0-5
BuildArch:	noarch

%description -n %{kpname}-cursor-theme
Breeze cursor theme.

%description -n %{kpname}-cursor-theme -l pl.UTF-8
Motyw kursora Breeze.

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

# breeze_kwin_deco, breeze_style_config domains
%find_lang %{kpname} --all-name

hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/icons/breeze_cursors
hardlink -c -v $RPM_BUILD_ROOT%{_datadir}/icons/Breeze_Snow

%clean
rm -rf $RPM_BUILD_ROOT

%post	data
%update_icon_cache hicolor
%update_desktop_database_post

%postun	data
%update_icon_cache hicolor
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/breeze-settings6
%attr(755,root,root) %{_bindir}/kcursorgen
%dir %{_libdir}/qt6/plugins/kstyle_config
%attr(755,root,root) %{_libdir}/qt6/plugins/kstyle_config/breezestyleconfig.so
%attr(755,root,root) %{_libdir}/qt6/plugins/org.kde.kdecoration3.kcm/kcm_breezedecoration.so
%attr(755,root,root) %{_libdir}/qt6/plugins/org.kde.kdecoration3/org.kde.breeze.so
%attr(755,root,root) %{_libdir}/qt6/plugins/styles/breeze6.so

%files data -f %{kpname}.lang
%defattr(644,root,root,755)
%dir %{_datadir}/QtCurve
%{_datadir}/QtCurve/Breeze.qtcurve
%dir %{_datadir}/color-schemes
%{_datadir}/color-schemes/BreezeClassic.colors
%{_datadir}/color-schemes/BreezeDark.colors
%{_datadir}/color-schemes/BreezeLight.colors
%{_datadir}/kstyle/themes/breeze.themerc
%{_datadir}/wallpapers/Next
%{_desktopdir}/breezestyleconfig.desktop
%{_desktopdir}/kcm_breezedecoration.desktop
%{_iconsdir}/hicolor/scalable/apps/breeze-settings.svgz

%files -n %{kpname}-cursor-theme
%defattr(644,root,root,755)
%{_iconsdir}/Breeze_Light
%{_iconsdir}/breeze_cursors

%files devel
%defattr(644,root,root,755)
%{_libdir}/cmake/Breeze
