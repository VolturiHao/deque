from pathlib import Path
import re
base=Path('app/src/main/res')
for filename in ['ic_launcher_foreground.xml','ic_launcher_mono.xml']:
 p=base/'drawable'/filename;s=p.read_text('utf-8-sig');s=s.replace('><path','><group android:translateX="3" android:translateY="-1"><path',1).replace('</vector>','</group></vector>');p.write_text(s,'utf-8')
fg=(base/'drawable/ic_launcher_foreground.xml').read_text()
background='<path android:fillColor="#174E36" android:pathData="M18,0 L90,0 Q108,0 108,18 L108,90 Q108,108 90,108 L18,108 Q0,108 0,90 L0,18 Q0,0 18,0Z"/>'
legacy=fg.replace('<group ',background+'<group ',1)
(base/'drawable/ic_launcher_legacy.xml').write_text(legacy,'utf-8');(base/'mipmap-anydpi/ic_launcher.xml').write_text(legacy,'utf-8')
p=Path('design/app-icon.svg');s=p.read_text('utf-8-sig');s=s.replace('/><path','/><g transform="translate(3 -1)"><path',1).replace('</svg>','</g></svg>');p.write_text(s,'utf-8')
p=Path('app/build.gradle');p.write_text(p.read_text().replace("versionCode 20; versionName '2.3.2'","versionCode 21; versionName '2.3.3'"))
