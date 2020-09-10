%global repo go-dbus-generator
%global with_debug 1
%global _unpackaged_files_terminate_build 0

%if 0%{?with_debug}
%global debug_package   %{nil}
%endif

Name:           deepin-dbus-generator
Version:        0.6.6
Release:        1
Summary:        Convert dbus interfaces to go-lang or qml wrapper code
License:        GPLv3+
URL:            https://github.com/linuxdeepin/go-dbus-generator
Source0:        https://github.com/linuxdeepin/%{repo}/archive/%{version}/%{repo}-%{version}.tar.gz

ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
BuildRequires:  golang compiler(go-compiler) pkgconfig(glib-2.0) pkgconfig(gobject-2.0) pkgconfig(Qt5) pkgconfig(Qt5Qml)

%description
Static dbus binding generator for dlib.

%prep
%setup -q -n %{repo}-%{version}
# qmake path
sed -i 's|qmake|qmake-qt5|' build_test.go template_qml.go

%build
export GOPATH=%{_builddir}/%{name}-%{version}-%{release_name}/vendor
BUILD_ID="0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
function gobuild { go build -mod=vendor -a -ldflags "-B $BUILD_ID" -v -x "$@"; }
gobuild -o dbus-generator

%install
install -Dm755 dbus-generator %{buildroot}%{_bindir}/dbus-generator

%files
%doc README.md
%license LICENSE
%{_bindir}/dbus-generator

%changelog
* Thu Sep 10 2020 chenbo pan <panchenbo@uniontech.com> - 0.6.6-1
- Initial build
