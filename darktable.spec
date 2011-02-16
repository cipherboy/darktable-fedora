#without --enable_gegl "until gegl is fast enough" as developers tell
%define with_gegl 0

Name:		darktable
Version:	0.8
Release:	1%{?dist}
Summary:	Utility to organize and develop raw images

Group:		Applications/Multimedia
License:	GPLv3+
URL:		http://darktable.sourceforge.net/index.shtml
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:	pkgconfig >= 0.22
BuildRequires:	intltool, gettext
BuildRequires:	sqlite-devel
BuildRequires:	libjpeg-devel, libpng-devel, libtiff-devel
BuildRequires:	librsvg2-devel >= 2.26
BuildRequires:	GConf2-devel, gtk2-devel, cairo-devel, libglade2-devel
BuildRequires:	lcms-devel
BuildRequires:  lcms2-devel
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


%build
[ ! -d "buildFedora" ] && mkdir buildFedora
cd buildFedora
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_BUILD_TYPE=Release -DINSTALL_IOP_EXPERIMENTAL=Off -DINSTALL_IOP_LEGACY=Off .. && make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
cd buildFedora
make install DESTDIR=$RPM_BUILD_ROOT
install -D ../data/darktable.schemas $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/darktable.schemas
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
 
%files -f buildFedora/%{name}.lang 
%defattr(-,root,root,-)
%{_bindir}/darktable
%{_libdir}/darktable
%{_datadir}/applications/darktable.desktop
%{_datadir}/darktable
%{_datadir}/icons/hicolor/*/apps/darktable.*
%{_datadir}/man/man1/darktable.1.gz
%{_sysconfdir}/gconf/schemas/darktable.schemas


%changelog
* Tue Feb 15 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-1
- Upgrade to version 0.8
- Rebuilt using cmake

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Edouard Bourguignon <madko@linuxed.net> - 0.7.1-3
- Change exiv2 headers to use the new umbrella header (#666887)

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.7.1-2
- rebuild (exiv2)

* Tue Dec 14 2010 Edouard Bourguignon <madko@linuxed.net> - 0.7.1-1
- Upgrade to version 0.7.1

* Mon Nov 29 2010 Edouard Bourguignon <madko@linuxed.net> - 0.7-1
- Upgrade to darktable 0.7

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
