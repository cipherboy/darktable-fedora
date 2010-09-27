#without --enable_gegl "until gegl is fast enough" as developers tell
%define with_gegl 0

Name:		darktable
Version:	0.6
Release:	9%{?dist}
Summary:	Utility to organize and develop raw images

Group:		Applications/Multimedia
License:	GPLv3+
URL:		http://darktable.sourceforge.net/index.shtml
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		darktable_desktop.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	pkgconfig >= 0.22
BuildRequires:	intltool, gettext
BuildRequires:	sqlite-devel
BuildRequires:	libjpeg-devel, libpng-devel, libtiff-devel
BuildRequires:	GConf2-devel, gtk2-devel, cairo-devel, libglade2-devel
BuildRequires:	lcms-devel
BuildRequires:	exiv2-devel
BuildRequires:	lensfun-devel
BuildRequires:	GConf2
BuildRequires:	OpenEXR-devel >= 1.6
BuildRequires:	libgphoto2-devel >= 2.4.5	
BuildRequires:	libcurl-devel >= 7.18.0
BuildRequires:	dbus-glib-devel >= 0.80 
BuildRequires:	gnome-keyring-devel >= 2.28.0
BuildRequires:	desktop-file-utils
%if 0%{?with_gegl}
BuildRequires:	gegl-devel
%endif

%description
Darktable is a virtual light-table and darkroom for photographers:
it manages your digital negatives in a database and lets you view them
through a zoom-able light-table.
It also enables you to develop raw images and enhance them.


%prep
%setup -q
%patch0 -p1 -b desktop.rej


%build
%configure	--disable-static \
%if 0%{?with_gegl}
		--enable-gegl
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%find_lang %{name}
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/darktable.desktop
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/darktable


%clean
rm -rf $RPM_BUILD_ROOT


%pre
%gconf_schema_prepare %{name} 

%post
%gconf_schema_upgrade %{name} 

update-desktop-database &> /dev/null ||:                                        
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun                                                                         
update-desktop-database &> /dev/null || :                                       
if [ $1 -eq 0 ] ; then                                                          
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null                     
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :            
fi                                                                              

%posttrans                                                                      
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%preun
%gconf_schema_remove %{name} 
 
%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS LICENSE TRANSLATORS
%{_bindir}/darktable
%{_libdir}/darktable
%{_datadir}/applications/darktable.desktop
%{_datadir}/darktable
%{_datadir}/icons/hicolor/*/apps/darktable.*
%{_datadir}/man/man1/darktable.1.gz
%{_sysconfdir}/gconf/schemas/darktable.schemas


%changelog
* Mon Sep 20 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-9
- Only use RPM_BUILD_ROOT
- Remove duplicated doc

* Mon Sep 20 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-8
- Change gegl-devel buildrequires
- Correct with_gegl option
- Correct typo in changelog
- Remove useless configure option (--disable-schemas)
- Add buildrequires on pkgconfig

* Fri Sep 10 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-7
- Remove useless removal of *.a files
- Change name of desktop patch (no version)

* Tue Aug 31 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 0.6-6
- disable static lib and schemas
- update desktop database and icon cache
- disable gegl support 

* Mon Aug 30 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-5
- Upgrade to Darktable 0.6
- Change to tar.gz for source0
- Remove rpath patch
- Add BuildRequires on missing devel packages
- Change path to libdarktable.so
- Add icons
- Make a clean desktop file
- Add desktop file validation

* Mon Aug 23 2010 Edouard Bourguignon <madko@linuxed.net> - 0.5-4
- Use Gconf scriplets to hangle gconf schema
- Add a patch to remove rpath from Dmitrij S. Kryzhevich

* Wed Jul  7 2010 Edouard Bourguignon <madko@linuxed.net> - 0.5-3
- Removing rpath

* Fri Apr 23 2010 Edouard Bourguignon <madko@linuxed.net> - 0.5-2
- Update to 0.5
- Shorten file list
- Use devel packages for building
- Correct URL for Source0

* Thu Feb 02 2010 İbrahim Eser <ibrahimeser@gmx.com.tr> - 0.4-1
- Initial package.
