# TODO: tests + dependencies
#
# Conditional build:
%bcond_without	doc	# ri/rdoc documentation

Summary:	Implementation of the AsciiDoc text processor and publishing toolchain
Summary(pl.UTF-8):	Implementacja procesora tekstu i systemu publikacji AsciiDoc
Name:		ruby-asciidoctor
Version:	2.0.15
Release:	1
License:	MIT
#Source0Download: https://github.com/asciidoctor/asciidoctor/releases
Source0:	https://github.com/asciidoctor/asciidoctor/archive/v%{version}/asciidoctor-%{version}.tar.gz
# Source0-md5:	e3ebbf64cf4014bae0e467befce92db2
Group:		Development/Languages
URL:		https://asciidoctor.org/
BuildRequires:	ruby >= 1:2.3
BuildRequires:	ruby-rubygems
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
%if %{with doc}
BuildRequires:	ruby-rdoc
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fast, open source text processor and publishing toolchain for
converting AsciiDoc content to HTML 5, DocBook 5, and other formats.

%description -l pl.UTF-8
Szybki, mający otwarte źródła procesor tekstu i system publikowania do
konwersji treści AsciiDoc do HTML-a 5, DocBooka 5 i innych formatów.

%package rdoc
Summary:	HTML documentation for Ruby asciidoctor module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu języka Ruby asciidoctor
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby asciidoctor module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby asciidoctor.

%package ri
Summary:	ri documentation for Ruby asciidoctor module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby asciidoctor
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby asciidoctor module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby asciidoctor.

%prep
%setup -q -n asciidoctor-%{version}

%{__sed} -i -e '1s,/usr/bin/env ruby,%{__ruby},' bin/asciidoctor

%build
gem build asciidoctor.gemspec

gem install asciidoctor-%{version}.gem --install-dir $(pwd)/.gem
%{__rm} -r .gem/gems/asciidoctor-%{version}/{LICENSE,*.adoc,*.gemspec,man}

%if %{with doc}
rdoc --ri --op ri lib
rdoc --op rdoc lib
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{ruby_gemdir}/gems,%{ruby_specdir}}

install .gem/bin/asciidoctor $RPM_BUILD_ROOT%{_bindir}
cp -p man/asciidoctor.1 $RPM_BUILD_ROOT%{_mandir}/man1

cp -pr .gem/gems/asciidoctor-%{version} $RPM_BUILD_ROOT%{ruby_gemdir}/gems
cp -p .gem/specifications/asciidoctor-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/Asciidoctor $RPM_BUILD_ROOT%{ruby_ridir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.adoc LICENSE README.adoc
%lang(de) %doc README-de.adoc
%lang(fr) %doc README-fr.adoc
%lang(jp) %doc README-jp.adoc
%lang(zh_CN) %doc README-zh_CN.adoc
%attr(755,root,root) %{_bindir}/asciidoctor
%dir %{ruby_gemdir}/gems/asciidoctor-%{version}
%dir %{ruby_gemdir}/gems/asciidoctor-%{version}/bin
%attr(755,root,root) %{ruby_gemdir}/gems/asciidoctor-%{version}/bin/asciidoctor
%{ruby_gemdir}/gems/asciidoctor-%{version}/data
%{ruby_gemdir}/gems/asciidoctor-%{version}/lib
%{ruby_specdir}/asciidoctor-%{version}.gemspec
%{_mandir}/man1/asciidoctor.1*

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Asciidoctor
%endif
