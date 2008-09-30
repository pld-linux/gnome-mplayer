Summary:	GNOME Frontend for MPlayer
Summary(pl.UTF-8):	Frontend GNOME dla MPlayera
Name:		gnome-mplayer
Version:	0.8.0
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://gnome-mplayer.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	a431750fe518f4dba882318b680e8e0f
URL:		http://kdekorte.googlepages.com/gnomemplayer
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
Requires(post,postun):	desktop-file-utils
Requires(post,preun):	GConf2
Requires:	mplayer
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install %{name}.schemas
%update_desktop_database_post

%preun
%gconf_schema_uninstall %{name}.schemas

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README DOCS/keyboard_shortcuts.txt DOCS/tech/*.*
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
