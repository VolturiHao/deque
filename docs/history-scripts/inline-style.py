from pathlib import Path
p=Path('app/src/main/java/cn/deque/MainActivity.java');s=p.read_text('utf-8')
s=s.replace('View renameHint;','')
a=s.index('setBackgroundTintList(null);android.graphics.drawable.GradientDrawable editBackground=');b=s.index('announceForAccessibility(',a)
s=s[:a]+'setBackground(null);invalidate();'+s[b:]
a=s.index('if(renameHint!=null)');b=s.index('if(inlineEditor==this)',a);s=s[:a]+s[b:]
pos=s.index(' void begin(){',s.index(' class InlineTitle'))
s=s[:pos]+''' @Override protected void onDraw(android.graphics.Canvas canvas){if(editing){float textWidth=getPaint().measureText(getText().toString());float width=Math.min(getWidth(),Math.max(dp(28),textWidth+getPaddingLeft()+getPaddingRight()+dp(8)));float inset=dp(1);android.graphics.RectF bounds=new android.graphics.RectF(getScrollX()+inset,getScrollY()+inset,getScrollX()+width-inset,getScrollY()+getHeight()-inset);android.graphics.Paint paint=new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);paint.setColor(tone(0xffe0efda,0xff284632));canvas.drawRoundRect(bounds,dp(8),dp(8),paint);paint.setStyle(android.graphics.Paint.Style.STROKE);paint.setStrokeWidth(dp(1));paint.setColor(accent);canvas.drawRoundRect(bounds,dp(8),dp(8),paint);}super.onDraw(canvas);}
''' +s[pos:]
s=s.replace('editing=false;setBackground(null);','editing=false;setBackground(null);invalidate();')
p.write_text(s,'utf-8')
p=Path('app/build.gradle');p.write_text(p.read_text().replace("versionCode 19; versionName '2.3.1'","versionCode 20; versionName '2.3.2'"))
