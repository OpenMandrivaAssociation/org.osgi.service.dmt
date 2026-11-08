Name:		org.osgi.service.dmt
Version:	2.0.2
Release:	1
Summary:	OSGi Device Management Tree API
Group:		Development/Java
License:	ASL 2.0
URL:		https://docs.osgi.org/
Source0:	https://repo1.maven.org/maven2/org/osgi/org.osgi.service.dmt/%{version}/org.osgi.service.dmt-%{version}-sources.jar
Source1:	https://raw.githubusercontent.com/osgi/osgi/r8-cmpn-final/LICENSE#/org.osgi.service.dmt-%{version}-LICENSE

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.osgi:org.osgi.annotation.versioning)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
OSGi Device Management Tree 2.0.2. DmtAdmin, DmtSession, the data
plugin SPI, notification, and the security permissions. The API
package version is 2.0.2. Notification, its SPI, security, and the
data SPI are version 2.0. Versioning annotations are compile-time
only. This build targets Java 8.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
rm -rf META-INF
cp -p %{SOURCE1} LICENSE
mkdir -p src/main/java
mv org src/main/java/
python - <<'PY'
from pathlib import Path

root = Path("src/main/java")
names = sorted(str(path.relative_to(root)) for path in root.rglob("*.java"))
expect = [
    "org/osgi/service/dmt/Acl.java",
    "org/osgi/service/dmt/DmtAdmin.java",
    "org/osgi/service/dmt/DmtConstants.java",
    "org/osgi/service/dmt/DmtData.java",
    "org/osgi/service/dmt/DmtEvent.java",
    "org/osgi/service/dmt/DmtEventListener.java",
    "org/osgi/service/dmt/DmtException.java",
    "org/osgi/service/dmt/DmtIllegalStateException.java",
    "org/osgi/service/dmt/DmtSession.java",
    "org/osgi/service/dmt/MetaNode.java",
    "org/osgi/service/dmt/Uri.java",
    "org/osgi/service/dmt/notification/AlertItem.java",
    "org/osgi/service/dmt/notification/NotificationService.java",
    "org/osgi/service/dmt/notification/package-info.java",
    "org/osgi/service/dmt/notification/spi/RemoteAlertSender.java",
    "org/osgi/service/dmt/notification/spi/package-info.java",
    "org/osgi/service/dmt/package-info.java",
    "org/osgi/service/dmt/security/AlertPermission.java",
    "org/osgi/service/dmt/security/DmtPermission.java",
    "org/osgi/service/dmt/security/DmtPrincipalPermission.java",
    "org/osgi/service/dmt/security/package-info.java",
    "org/osgi/service/dmt/spi/DataPlugin.java",
    "org/osgi/service/dmt/spi/ExecPlugin.java",
    "org/osgi/service/dmt/spi/MountPlugin.java",
    "org/osgi/service/dmt/spi/MountPoint.java",
    "org/osgi/service/dmt/spi/ReadWriteDataSession.java",
    "org/osgi/service/dmt/spi/ReadableDataSession.java",
    "org/osgi/service/dmt/spi/TransactionalDataSession.java",
    "org/osgi/service/dmt/spi/package-info.java",
]
if names != expect:
    raise SystemExit("java files " + " ".join(names))
versions = {
    "org/osgi/service/dmt/package-info.java": '@Version("2.0.2")',
    "org/osgi/service/dmt/notification/package-info.java": '@Version("2.0")',
    "org/osgi/service/dmt/notification/spi/package-info.java": '@Version("2.0")',
    "org/osgi/service/dmt/security/package-info.java": '@Version("2.0")',
    "org/osgi/service/dmt/spi/package-info.java": '@Version("2.0")',
}
for rel, marker in versions.items():
    text = (root / rel).read_text(encoding="utf-8")
    if marker not in text:
        raise SystemExit("package-info version changed " + rel)
if list(Path(".").rglob("packageinfo")):
    raise SystemExit("unexpected packageinfo")
if "Apache License" not in Path("LICENSE").read_text(encoding="utf-8"):
    raise SystemExit("LICENSE is not the Apache license")
if list(Path(".").rglob("*.jar")) or list(Path(".").rglob("*.class")):
    raise SystemExit("prebuilt binary remains")
for pom in Path(".").rglob("pom.xml"):
    pom.unlink()

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.osgi</groupId>
  <artifactId>org.osgi.service.dmt</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>org.osgi:org.osgi.service.dmt</name>
  <description>OSGi Device Management Tree.</description>
  <url>https://docs.osgi.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.annotation.versioning</artifactId>
      <version>1.1.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>org.osgi.service.dmt</artifactId>",
    "<artifactId>org.osgi.annotation.versioning</artifactId>",
    "<version>1.1.0</version>",
    "<scope>provided</scope>",
    "<version>%{version}</version>",
    "<release>8</release>",
    "</project.build.sourceEncoding>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
if pom.count("<version>2.0.2</version>") != 1:
    raise SystemExit("project version count")
if pom.count("<version>1.1.0</version>") != 1:
    raise SystemExit("annotation version count")
for needle in (
    "junit",
    "SNAPSHOT",
    "<source>",
    "<target>",
    "<parent>",
    "felix",
    "maven-bundle-plugin",
    "<artifactId>osgi.annotation</artifactId>",
    "<artifactId>osgi.core</artifactId>",
    "<version>8.0.1</version>",
    "<version>8.1.0</version>",
    "projectbuild.sourceEncoding",
):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/org.osgi.service.dmt-%{version}.jar --describe-module org.osgi.service.dmt > module-describe.txt
grep -q '^org.osgi.service.dmt' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }
python - <<'PY'
import zipfile
from pathlib import Path
jar = Path("target/org.osgi.service.dmt-%{version}.jar")
with zipfile.ZipFile(jar) as zf:
    names = set(zf.namelist())
required = {
    "org/osgi/service/dmt/Acl.class",
    "org/osgi/service/dmt/DmtAdmin.class",
    "org/osgi/service/dmt/DmtConstants.class",
    "org/osgi/service/dmt/DmtData.class",
    "org/osgi/service/dmt/DmtEvent.class",
    "org/osgi/service/dmt/DmtEventListener.class",
    "org/osgi/service/dmt/DmtException.class",
    "org/osgi/service/dmt/DmtIllegalStateException.class",
    "org/osgi/service/dmt/DmtSession.class",
    "org/osgi/service/dmt/MetaNode.class",
    "org/osgi/service/dmt/Uri.class",
    "org/osgi/service/dmt/package-info.class",
    "org/osgi/service/dmt/notification/AlertItem.class",
    "org/osgi/service/dmt/notification/NotificationService.class",
    "org/osgi/service/dmt/notification/package-info.class",
    "org/osgi/service/dmt/notification/spi/RemoteAlertSender.class",
    "org/osgi/service/dmt/notification/spi/package-info.class",
    "org/osgi/service/dmt/security/AlertPermission.class",
    "org/osgi/service/dmt/security/DmtAlertPermissionCollection.class",
    "org/osgi/service/dmt/security/DmtPermission.class",
    "org/osgi/service/dmt/security/DmtPermissionCollection.class",
    "org/osgi/service/dmt/security/DmtPrincipalPermission.class",
    "org/osgi/service/dmt/security/DmtPrincipalPermissionCollection.class",
    "org/osgi/service/dmt/security/package-info.class",
    "org/osgi/service/dmt/spi/DataPlugin.class",
    "org/osgi/service/dmt/spi/ExecPlugin.class",
    "org/osgi/service/dmt/spi/MountPlugin.class",
    "org/osgi/service/dmt/spi/MountPoint.class",
    "org/osgi/service/dmt/spi/ReadWriteDataSession.class",
    "org/osgi/service/dmt/spi/ReadableDataSession.class",
    "org/osgi/service/dmt/spi/TransactionalDataSession.class",
    "org/osgi/service/dmt/spi/package-info.class",
}
missing = sorted(required - names)
if missing:
    raise SystemExit("missing " + " ".join(missing))
extra = sorted(name for name in names if name.endswith(".class") and name not in required)
if extra:
    raise SystemExit("extra " + " ".join(extra))
if any("$" in name for name in names):
    raise SystemExit("unexpected inner class")
if any(name.endswith("packageinfo") for name in names):
    raise SystemExit("unexpected packageinfo")
PY

%files -f .mfiles
%doc LICENSE
