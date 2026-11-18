from pathlib import Path
p=Path('app/src/main/java/cn/deque/MainActivity.java');s=p.read_text('utf-8')
s=s.replace('if(trash!=completed){trash=completed;show();}','switchPage(completed);').replace('swipeConsumed=true;trash=!trash;show();','swipeConsumed=true;switchPage(!trash);')
a=s.index(' void lift(');b=s.index(' void drawer()',a)
s=s[:a]+''' boolean pageTransition;
 void switchPage(boolean completed){if(pageTransition||trash==completed)return;pageTransition=true;float direction=completed?-1:1;root.animate().translationX(direction*dp(24)).alpha(0).setDuration(100).withEndAction(()->{trash=completed;show();root.setTranslationX(-direction*dp(24));root.setAlpha(0);root.animate().translationX(0).alpha(1).setDuration(180).withEndAction(()->pageTransition=false).start();}).start();}
 void lift(View view,boolean selected){view.animate().scaleX(selected?.985f:1).scaleY(selected?.985f:1).translationZ(selected?dp(2):0).alpha(selected?.9f:1).setDuration(140).start();if(selected)view.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS);}
 class QueueHolder extends androidx.recyclerview.widget.RecyclerView.ViewHolder{TextView button;QueueHolder(TextView b){super(b);button=b;}}
''' +s[b:]
s=s.replace('list.setLayoutManager(new androidx.recyclerview.widget.LinearLayoutManager(this));panel.addView','list.setClipToPadding(false);list.setPadding(dp(4),dp(6),dp(4),dp(6));list.setLayoutManager(new androidx.recyclerview.widget.LinearLayoutManager(this));panel.addView')
a=s.index('com.google.android.material.button.MaterialButton button=new',s.index('void drawer()'));b=s.index('androidx.recyclerview.widget.RecyclerView.LayoutParams lp=',a)
s=s[:a]+'''TextView button=new TextView(MainActivity.this);button.setMinHeight(dp(52));button.setTextSize(16);button.setPadding(dp(16),dp(12),dp(12),dp(12));button.setGravity(Gravity.START|Gravity.CENTER_VERTICAL);''' +s[b:]
s=s.replace('lp.setMargins(0,0,0,dp(8))','lp.setMargins(0,0,0,dp(3))')
a=s.index('holder.button.setStrokeWidth(');b=s.index('holder.button.setOnClickListener',a)
s=s[:a]+'''holder.button.setTypeface(null,selected?android.graphics.Typeface.BOLD:android.graphics.Typeface.NORMAL);android.graphics.drawable.GradientDrawable background=new android.graphics.drawable.GradientDrawable();background.setCornerRadius(dp(12));background.setColor(selected?tone(0xffdcebd8,0xff2b4834):Color.TRANSPARENT);holder.button.setBackground(new android.graphics.drawable.RippleDrawable(android.content.res.ColorStateList.valueOf(tone(0x22246b49,0x33a4d6b0)),background,null));holder.button.setCompoundDrawablesRelativeWithIntrinsicBounds(icon("queue"),null,icon("drag"),null);holder.button.setCompoundDrawablePadding(dp(12));''' +s[b:]
s=s.replace('create.setMinHeight(dp(56));','create.setGravity(Gravity.CENTER);create.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);create.setIconPadding(dp(8));create.setPaddingRelative(dp(16),0,dp(16),0);create.setCornerRadius(dp(16));create.setMinHeight(dp(52));')
s=s.replace('settings.setMinHeight(dp(56));','settings.setMinHeight(dp(48));settings.setGravity(Gravity.CENTER);settings.setIconSize(dp(20));settings.setTextSize(14);settings.setPaddingRelative(dp(16),0,dp(16),0);')
s=s.replace('MaterialButton settings=new com.google.android.material.button.MaterialButton(this,null,com.google.android.material.R.attr.materialButtonOutlinedStyle)','MaterialButton settings=new com.google.android.material.button.MaterialButton(this,null,com.google.android.material.R.attr.borderlessButtonStyle)')
s=s.replace('panel.addView(settings,new LinearLayout.LayoutParams(-1,-2));','LinearLayout.LayoutParams settingsLp=new LinearLayout.LayoutParams(-2,-2);settingsLp.gravity=Gravity.START;panel.addView(settings,settingsLp);')
s=s.replace('dp(20),0,dp(12)','dp(12),0,dp(4)')
s=s.replace('case "menu":','case "queue":canvas.drawRoundRect(4,4,20,20,3,3,paint);canvas.drawLine(8,9,16,9,paint);canvas.drawLine(8,14,14,14,paint);break;case "drag":paint.setStyle(android.graphics.Paint.Style.FILL);for(int y=7;y<=17;y+=5){canvas.drawCircle(9,y,1,paint);canvas.drawCircle(15,y,1,paint);}break;case "menu":')
p.write_text(s,'utf-8')
p=Path('app/build.gradle');s=p.read_text().replace("versionCode 15; versionName '2.2'","versionCode 16; versionName '2.2.1'");p.write_text(s)
