from pathlib import Path
p=Path('app/build.gradle');s=p.read_text();s=s.replace("android { namespace", "def signingFile = rootProject.file('signing.properties')\ndef signing = new Properties()\nif (signingFile.exists()) signingFile.withInputStream { signing.load(it) }\nandroid { namespace")
s=s.replace("versionCode 12; versionName '2.1'","versionCode 13; versionName '2.1.1'")
s=s.replace(' compileOptions', ''' signingConfigs { release { if (signingFile.exists()) { storeFile rootProject.file(signing['storeFile']); storePassword signing['storePassword']; keyAlias signing['keyAlias']; keyPassword signing['keyPassword'] } } }
 buildTypes { release { signingConfig signingConfigs.release; minifyEnabled false; debuggable false } }
 compileOptions''');p.write_text(s)
p=Path('.gitignore');p.write_text(p.read_text()+'\nsigning.properties\nsigning/\n*.jks\n*.keystore\n')
