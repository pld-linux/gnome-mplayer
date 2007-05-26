Summary:	GNOME Frontend for MPlayer
Name:		gnome-mplayer
Version:	0.4.6
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dekorte.homeip.net/download/gnome-mplayer/%{name}-%{version}.tar.gz
# Source0-md5:	d3f3565286d62dad0618b215feac792a
URL:		http://dekorte.homeip.net/download/gnome-mplayer/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
Requires:	mplayer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME MPlayer is a simple GUI for MPlayer. It is based heavily on the
mplayerplug-in source code and can basically be seen as a standalone
version of that. GNOME MP layer is currently changing alot. However,
it is good enough that I can use it as my default viewer for media on
my personal machine.

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

%preun
%gconf_schema_uninstall %{name}.schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README DOCS/tech/*.*
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
