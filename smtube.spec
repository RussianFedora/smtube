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
Requires:       hicolor-icon-theme

%description
This is a YouTube browser for SMPlayer. You can browse, search
and play YouTube videos.

%prep
%setup -q

# correction for wrong-file-end-of-line-encoding
sed -i 's/\r//' *.txt
# fix files which are not UTF-8 
#iconv -f Latin1 -t UTF-8 -o Changelog.utf8 Changelog
#mv Changelog.utf8 Changelog
sed -i 's/.*DOC_PATH.*//g' Makefile
sed -i "s|PREFIX=/usr/local|PREFIX=%{_prefix}|" Makefile

%build
pushd src
    %{qmake_qt5}
    %make_build TRANSLATION_PATH=\\\"%{_datadir}/%{name}/translations\\\"
    %{_bindir}/lrelease-qt5 %{name}.pro
popd

%install
%make_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc Changelog Readme.txt Release_notes.txt
%license Copying.txt
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}

%changelog
* Fri Jun 17 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.6.0-2
- Clean spec for Fedora

* Fri Feb 26 2016 Ricardo Villalba <rvm@users.sourceforge.net> - 16.1.0
- Initial Release

