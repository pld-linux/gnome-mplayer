# TODO:
# - nautilus-gnome-mplayer subpackage
# - double-check gnome-power-manager BR
#
# Conditional build:
%bcond_without  gtk3            # build without GTK+3

Summary:	GNOME Frontend for MPlayer
Summary(pl.UTF-8):	Frontend GNOME dla MPlayera
Name:		gnome-mplayer
Version:	1.0.9a
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://gnome-mplayer.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	7199f93760cbf7c63144244451b7b57a
Patch0:		%{name}-desktop.patch
URL:		http://kdekorte.googlepages.com/gnomemplayer
BuildRequires:	GConf2
BuildRequires:	GConf2-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
Requires(post,postun):	glib2 >= 1:2.26.0
# BuildRequires:	gnome-power-manager
BuildRequires:	gettext-tools
BuildRequires:	gmtk-devel >= 1.0.8
%if %{with gtk3}
BuildRequires:	gtk+3-devel
%else
BuildRequires:	gtk+2-devel
%endif
BuildRequires:	libgpod-devel
BuildRequires:	libmusicbrainz3-devel
BuildRequires:	libnotify-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	which
Requires(post,postun):	desktop-file-utils
Requires(post,preun):	GConf2
Requires:	mplayer
Suggests:	dconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME MPlayer is a simple GUI for MPlayer. It is based heavily on the
mplayerplug-in source code and can basically be seen as a standalone
version of that. GNOME MPlayer is currently changing a lot. However,
it is good enough that I can use it as my default viewer for media on
my personal machine.

%description -l pl.UTF-8
GNOME MPlayer to prosty graficzny interfejs dla MPlayera. Jest w dużym
stopniu oparty na kodzie źródłowym wtyczki mplayerplug-in i można go
zasadniczo postrzegać jako jej samodzielną wersję. GNOME MPlayer
aktualnie znacząco się zmienia. Jest jednak już wystarczająco dobry do
używania jako domyślna przeglądarka multimediów na komputerze
osobistym autora.

%prep
%setup -q
%patch0 -p1
%{__sed} -i 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure.in
%{__sed} -i 's/AM_PROG_CC_STDC/AC_PROG_CC/g' configure.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_gtk3:--disable-gtk3}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas
cp -p %{name}.schemas $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas

install -d $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
cp -p apps.gecko-mediaplayer.preferences.gschema.xml $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
cp -p apps.gnome-mplayer.preferences.enums.xml $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
cp -p apps.gnome-mplayer.preferences.gschema.xml $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

# gnome2
%{__rm} $RPM_BUILD_ROOT%{_datadir}/gnome-control-center/default-apps/gnome-mplayer.xml

# not packaged
%{__rm} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/gnome-mplayer.svg

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install %{name}.schemas
%update_desktop_database_post
%glib_compile_schemas

%preun
%gconf_schema_uninstall %{name}.schemas

%postun
%update_desktop_database_postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README DOCS/keyboard_shortcuts.txt DOCS/tech/*.*
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_datadir}/glib-2.0/schemas/*.xml
%{_iconsdir}/hicolor/*/apps/*.png
%{_desktopdir}/*.desktop
%{_mandir}/man1/*.1*
