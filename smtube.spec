%global debug_package %{nil}

Name:           smtube
Version:        16.6.0
Release:        2%{?dist}
Summary:        YouTube browser for SMPlayer

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.smtube.org
Source0:        http://downloads.sourceforge.net/smtube/%{name}-%{version}.tar.bz2

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

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}
#%{_mandir}/man1/smtube.1.gz
%{_docdir}/%{name}

%changelog
* Fri Jun 17 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.6.0-2
- Clean spec for Fedora

* Fri Feb 26 2016 Ricardo Villalba <rvm@users.sourceforge.net> - 16.1.0
- Initial Release

