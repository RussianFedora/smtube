Name:           smtube
Version:        16.6.0
Release:        1%{?dist}
Summary:        YouTube browser for SMPlayer

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.smtube.org
Source0:        http://downloads.sourceforge.net/smtube/smtube-%{version}.tar.bz2

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  pkgconfig(Qt5Designer)

Requires:       smplayer

%description
This is a YouTube browser for SMPlayer. You can browse, search
and play YouTube videos.

%prep
%setup -q

# correction for wrong-file-end-of-line-encoding
%{__sed} -i 's/\r//' *.txt
# fix files which are not UTF-8 
iconv -f Latin1 -t UTF-8 -o Changelog.utf8 Changelog 
mv Changelog.utf8 Changelog

%build
make \
    QMAKE=%{_qt5_qmake} \
    LRELEASE=%{_bindir}/lrelease-qt5 \
    PREFIX=%{_prefix} \
    DOC_PATH="\\\"%{_docdir}/%{name}/\\\""

#touch src/smtube
#touch src/translations/smtube_es.qm

%install
make PREFIX=%{_prefix} DESTDIR=%{buildroot}/ DOC_PATH=%{_docdir}/%{name}/ install

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null || :

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null || :

%files
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%dir %{_datadir}/icons/hicolor/*/
%dir %{_datadir}/icons/hicolor/*/apps/
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}
#%{_mandir}/man1/smtube.1.gz
%{_docdir}/%{name}

%changelog
* Fri Jun 17 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.6.0-1
- Clean spec for Fedora

* Fri Feb 26 2016 Ricardo Villalba <rvm@users.sourceforge.net> - 16.1.0
- Initial Release

