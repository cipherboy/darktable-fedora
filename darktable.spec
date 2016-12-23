# osm-gps-map-devel > 1.0 available only in Fedora
%if 0%{?fedora}
%global with_osm_gps_map_devel 1
%endif

Name: darktable
Version: 2.0.7
Release: 2%{?dist}

Summary: Utility to organize and develop raw images

License: GPLv3+
URL: http://www.darktable.org/
Source0: https://github.com/darktable-org/darktable/releases/download/release-%{version}/darktable-%{version}.tar.xz

BuildRequires: cairo-devel
BuildRequires: cmake
BuildRequires: colord-gtk-devel
BuildRequires: colord-devel
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: exiv2-devel
BuildRequires: flickcurl-devel
BuildRequires: GraphicsMagick-devel
BuildRequires: gtk3-devel
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: json-glib-devel
BuildRequires: lcms2-devel
BuildRequires: lensfun-devel
BuildRequires: libappstream-glib
BuildRequires: libcurl-devel >= 7.18.0
BuildRequires: libgphoto2-devel >= 2.4.5
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel >= 2.26
BuildRequires: libsecret-devel
BuildRequires: libsoup-devel
BuildRequires: libtiff-devel
BuildRequires: libwebp-devel
BuildRequires: opencl-headers
BuildRequires: OpenEXR-devel >= 1.6
BuildRequires: openjpeg-devel
%if 0%{?with_osm_gps_map_devel}
BuildRequires: osm-gps-map-devel >= 1.0
%endif
BuildRequires: perl
BuildRequires: pkgconfig >= 0.22
BuildRequires: po4a
BuildRequires: /usr/bin/pod2man
BuildRequires: pugixml-devel
BuildRequires: SDL-devel
BuildRequires: sqlite-devel

# Concerning rawspeed bundled library, see
# https://fedorahosted.org/fpc/ticket/550#comment:9
Provides: bundled(rawspeed)
Provides: bundled(lua)


# uses xmmintrin.h
ExclusiveArch: x86_64


%description
Darktable is a virtual light-table and darkroom for photographers:
it manages your digital negatives in a database and lets you view them
through a zoom-able light-table.
It also enables you to develop raw images and enhance them.


%prep
echo directory: %{name}-%{version}
%setup -q -n 'darktable-%{version}'

# Remove bundled OpenCL headers.
rm -rf src/external/CL
sed -i -e 's, \"external/CL/\*\.h\" , ,' src/CMakeLists.txt

# Remove bundled lua.
# Line commented because we temporarily enabled bundled Lua while waiting for
# a compat-lua-52 package
# rm -rf src/external/lua/

%build
mkdir %{_target_platform} 
pushd %{_target_platform} 
%cmake \
        -DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
        -DUSE_GEO:BOOLEAN=ON \
        -DCMAKE_BUILD_TYPE:STRING=Release \
        -DBINARY_PACKAGE_BUILD=1 \
        -DDONT_USE_INTERNAL_LUA=OFF \
        -DPROJECT_VERSION:STRING="%{name}-%{version}-%{release}" \
        ..


make %{?_smp_mflags} VERBOSE=1
popd
pushd tools/noise
make %{?_smp_mflags}


%install
pushd %{_target_platform} 
make install DESTDIR=%{buildroot}
popd
find %{buildroot} -name '*.la' -exec rm -f {} ';'
%find_lang %{name}
rm -rf %{buildroot}%{_datadir}/doc/darktable
mkdir -p %{buildroot}%{_libexecdir}/darktable/tools/noise
rm tools/noise/*.c
rm tools/noise/Makefile
cp tools/noise/* %{buildroot}%{_libexecdir}/darktable/tools/noise/
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/darktable.appdata.xml


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang 
%license doc/LICENSE
%doc doc/README doc/AUTHORS doc/TRANSLATORS
%{_bindir}/darktable
%{_bindir}/darktable-cli
%{_bindir}/darktable-cltest
%{_bindir}/darktable-cmstest
%{_bindir}/darktable-generate-cache
%{_bindir}/darktable-viewer
%{_libdir}/darktable
%{_datadir}/darktable
%{_datadir}/applications/darktable.desktop
%{_datadir}/appdata/darktable.appdata.xml
%{_datadir}/icons/hicolor/*/apps/darktable*
%{_mandir}/man1/darktable*.1.gz
%{_mandir}/*/man1/darktable*.1.gz
%{_libexecdir}/darktable/

%changelog
* Fri Nov 25 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.7-2
- Enabled bundled Lua, while discussing the creation of a compat-lua-52 package with Fedora Lua Special Interest Group

* Tue Oct 25 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.7-1
- Minor update

* Wed Sep 07 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.6-1
- Minor update

* Tue Jul 05 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.5-1
- Minor update

* Tue May 03 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.4-1
- Minor update

* Mon Apr 25 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.3-3
- Added app-data-validate usage. See https://fedoraproject.org/wiki/Packaging:AppData#app-data-validate_usage

* Sat Apr 02 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.3-2
- Changed %if 0%{with_osm_gps_map_devel} to %if 0%{?with_osm_gps_map_devel}

* Fri Apr 01 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.3-1
- Minor update

* Mon Mar 07 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.2-1
- Minor update

* Sun Feb 07 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.1-2
- Fixed Openstreetmap support

* Wed Feb 03 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.1-1
- Minor update with a lot of fixes. Further infos at https://github.com/darktable-org/darktable/releases/tag/release-2.0.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 09 2016 Germano Massullo <germano.massullo@gmail.com> - 2.0.0-1
- dartable-generate-nopatents-tarball.sh no longer requires since squid is no longer present in Darktable
- Added %{_libexecdir}/darktable/ to fix bugreport #1278142
- Added %{_bindir}/darktable-generate-cache
- Adjusted dependencies to reflect Darktable 2.0 dependencies
- Replaced %{_datadir}/man/man1/darktable.1.gz and %{_datadir}/man/man1/darktable-cli.1.gz with %{_mandir}/man1/darktable*.1.gz and %{_mandir}/*/man1/darktable*.1.gz
- Sorted BuildRequire list in alphabetical order

* Sat Nov 07 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.9-5
- Removed -DCUSTOM_CFLAGS=ON Please read https://bugzilla.redhat.com/show_bug.cgi?id=1278064#c18

* Sat Nov 07 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.9-4
- Added -DCUSTOM_CFLAGS=ON

* Fri Nov 06 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.9-3
- Removed x86 32 bit CPU support

* Wed Nov 04 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.6.9-2
- Rework bundled opencl-headers handling in %%prep (RHBZ#1264933).

* Wed Oct 21 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.9-1
- Update to 1.6.9

* Thu Sep 10 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.8-3
- spec file: removed BuildRequires: lua-devel because Darktable supports only LUA 5.2 version

* Tue Sep 08 2015 Kalev Lember <klember@redhat.com> - 1.6.8-2
- Build with system lua
- Remove bundled lua in prep to make sure it's not used

* Tue Sep 08 2015 Kalev Lember <klember@redhat.com> - 1.6.8-1
- Update to 1.6.8
- Modernize spec file for current rpmbuild
- Drop GConf handling now that darktable no longer uses it
- Drop unused build deps
- Build with libsecret support, instead of libgnome-keyring
- Use license macro

* Tue Jul  7 2015 Tom Callaway <spot@fedoraproject.org> - 1.6.7-4
- unbundle opencl headers (and use system opencl headers)

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.6.7-3
- rebuild (exiv2)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 9 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.7-1
- Corrected Darktable website in spec file
- Minor update

* Thu May 14 2015 Nils Philippsen <nils@redhat.com> - 1.6.6-2
- rebuild for lensfun-0.3.1

* Sun Apr 26 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.6-1
- Minor update. Full changelog at https://github.com/darktable-org/darktable/releases/tag/release-1.6.6

* Sat Apr 4 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.4-1
- Minor update. Full changelog at https://github.com/darktable-org/darktable/releases/tag/release-1.6.4
- Removed patch for Canon EOS Rebel, because the fixed code is in the upstream stable release.

* Wed Mar 18 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.3-2
- Backport of fix for bugreport #1202105

* Mon Mar 02 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.3-1
- Darktable 1.6.3
- Fixed date of Feb 22 2015 changelog.

* Sun Feb 22 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.2-5
- Removed LUA support due missing LUA 5.3 support by Darktable. This will avoid breaking build tree.

* Wed Feb 04 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.2-4
- Removed "Requires: lua-devel"

* Wed Feb 04 2015 Germano Massullo <germano.massullo@gmail.com> - 1.6.2-3
- Added LUA support

* Wed Feb 04 2015 Edouard Bourguignon <madko@linuxed.net> - 1.6.2-2
- Aesthetic changes (useless spaces)
- Use mkdir %{_target_platform} instead of buildFedora
- Consistence use of %var instead of $VAR
 
* Mon Feb 02 2015 Edouard Bourguignon <madko@linuxed.net> - 1.6.2-1
- Darktable 1.6.2

* Sun Feb 01 2015 Edouard Bourguignon <madko@linuxed.net> - 1.6.1-1
- Darktable 1.6.1

* Wed Jan 21 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.0-2
- Rebuild (libgpohoto2) 

* Tue Dec 09 2014 Edouard Bourguignon <madko@linuxed.net> - 1.6.0-1
- Darktable 1.6.0 stable 

* Sat Dec 06 2014 Edouard Bourguignon <madko@linuxed.net> - 1.5.1-0.2
- Add missing darktable-cmstest

* Sat Dec 06 2014 Edouard Bourguignon <madko@linuxed.net> - 1.5.1-0.1
- Darktable 1.6 rc1

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 1.4.2-4
- rebuild (openexr)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Edouard Bourguignon <madko@linuxed.net> - 1.4.2-1
- Upgrade to 1.4.2

* Mon Mar  3 2014 Edouard Bourguignon <madko@linuxed.net> - 1.4.1-3
- Remove wrong library path

* Mon Mar  3 2014 Edouard Bourguignon <madko@linuxed.net> - 1.4.1-2
- Restore rpath for internal lib

* Wed Feb 12 2014 Edouard Bourguignon <madko@linuxed.net> - 1.4.1-1
- Upgrade to 1.4.1
- Remove tools source files

* Tue Jan 14 2014 Edouard Bourguignon <madko@linuxed.net> - 1.4-2
- Add OpenJPEG and WebP support
- Add missing buildrequires on pod2man

* Wed Jan  1 2014 Edouard Bourguignon <madko@linuxed.net> - 1.4-1
- Upgrade to 1.4

* Mon Dec  2 2013 Edouard Bourguignon <madko@linuxed.net> - 1.4-0.1.rc1
- Upgrade to 1.4~rc1

* Sun Nov 24 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2.3-2
- Add colord-devel support

* Sun Sep 15 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2.3-1
- Upgrade to 1.2.3

* Tue Jun 25 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2.2-1
- Upgrade to 1.2.2

* Tue Jun 11 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2.1-4
- Remove patented code (DXT/squish)

* Mon Jun 10 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2.1-3
- Patch to make squish optional

* Mon Jun 10 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2.1-2
- fix for CVE-2013-2126 (Thanks to Alex Tutubalin's patch)
- Do not use squish (bug #972604)

* Sun May 26 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2.1-1
- Upgrade to 1.2.1

* Thu May  2 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2-2
- Add profiling sensor and photon noise tools

* Sat Apr  6 2013 Edouard Bourguignon <madko@linuxed.net> - 1.2-1
- Upgrade to 1.2

* Sun Mar 10 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.4-2
- Rebuild

* Sun Mar 10 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.4-1
- Upgrade to 1.1.4

* Fri Feb 22 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.3-2
- Add some missing dependancies

* Mon Feb 11 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.3-1
- Upgrade to 1.1.3

* Fri Feb  1 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.2+26~ge1f2980
- Pre 1.1.3

* Mon Jan 21 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.2-2
- Add missing gtk2-engine dependancy (bug #902288)

* Sat Jan 12 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.2-1
- Upgrade to 1.1.2

* Sun Jan  6 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.1-2
- Add map mode

* Wed Nov 28 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1.1-1
- Upgrade to 1.1.1 

* Sat Nov 24 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1-1
- Upgrade to 1.1

* Wed Nov 14 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1-0.1.rc2
- Upgrade to 1.1~rc2

* Wed Oct 31 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1-0.1.rc1
- Upgrade to 1.1~rc1

* Thu Jul 26 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.5-1
- Upgrade to 1.0.5

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Jindrich Novy <jnovy@redhat.com> - 1.0.4-2
- rebuild because of new libgphoto2

* Sat Jun 30 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.4-1
- Upgrade to 1.0.4

* Sun Apr 29 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.3-1
- Upgrade to 1.0.3

* Sat Apr 28 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.1-1
- Upgrade to 1.0.1

* Thu Mar 15 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-1
- Upgrade to stable 1.0

* Sun Mar 11 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.4.rc2
- Remove pre script

* Sat Mar 10 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.3.rc2
- Patch for uninitialised variables

* Sat Mar 10 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.2.rc2
- Remove useless darktable gconf schemas

* Sat Mar 10 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.1.rc2
- Upgrade to rc2

* Wed Mar  7 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.2.rc1
- Correct invalid type in darktable gconf schemas

* Sun Mar  4 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.1.rc1
- Darktable 1.0 RC1

* Mon Dec  5 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.3-2
- Add SDL-devel for darktable-viewer

* Mon Nov  7 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.3-1
- Upgrade to 0.9.3

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.9.2-2
- rebuild (exiv2)

* Fri Aug 26 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.2-1
- Upgrade to 0.9.2

* Thu Jul 28 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.1-1
- Upgrade to 0.9.1
- Remove some old patches

* Sat Jul  2 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9-1
- Upgrade to 0.9

* Mon May 23 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-11
- Add a patch for BINARY_PACKAGE_BUILD (preventing march=native)

* Fri Apr 22 2011 Dan Horák <dan[at]danny.cz> - 0.8-10
- make it x86-only

* Fri Apr 22 2011 Dan Horák <dan[at]danny.cz> - 0.8-9
- don't use x86-only compiler flags on non-x86 arches

* Tue Apr 19 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-8
- Change build option

* Mon Apr 11 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.8-7.1
- rebuild (exiv2)

* Wed Mar 30 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-7
- Change cmake options

* Tue Mar 22 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-6
- Keep rpath for internal libs 

* Wed Feb 23 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-5
- Change build options
- Change permission on gconf darktable.schemas
- Add patch and cmake option to remove relative path (thanks to Karl Mikaelsson)

* Sat Feb 19 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-4
- Add missing doc files

* Sat Feb 19 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-3
- Clean up set but unused variables patch for GCC 4.6 (Karl Mikaelsson)

* Thu Feb 17 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-2
- Add flickcurl support
- Add patch to fix unused but set variables

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

* Tue Feb 02 2010 İbrahim Eser <ibrahimeser@gmx.com.tr> - 0.4-1
- Initial package.
