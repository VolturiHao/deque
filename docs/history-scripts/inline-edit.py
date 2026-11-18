from pathlib import Path
p=Path('app/src/main/java/cn/deque/MainActivity.java');s=p.read_text('utf-8')
s=s.replace('active!=null&&!trash&&!dragging','active!=null&&!trash&&!dragging&&inlineEditor==null')
a=s.index('toolbar.setTitle(name());');b=s.index(' tabFrame=',a)
s=s[:a]+'''toolbar.setNavigationIcon(icon("menu"));toolbar.setNavigationContentDescription("打开队列");toolbar.setNavigationOnClickListener(v->drawer());toolbar.getMenu().add("队列设置").setIcon(icon("settings")).setShowAsAction(2);toolbar.setOnMenuItemClickListener(item->{settings();return true;});root.addView(toolbar);final String queueId=queue;InlineTitle queueTitle=new InlineTitle(name(),value->{db.execSQL("UPDATE queues SET name=?,updated=? WHERE id=?",new Object[]{value,now(),queueId});},null);queueTitle.setTextSize(20);queueTitle.setTypeface(null,android.graphics.Typeface.BOLD);queueTitle.setContentDescription("队列标题，双击原位编辑");toolbar.addView(queueTitle,new com.google.android.material.appbar.MaterialToolbar.LayoutParams(-1,-2));
''' +s[b:]
s=s.replace('TextView title=label(t[1],17);','TextView title=trash?label(t[1],17):new InlineTitle(t[1],value->{db.execSQL("UPDATE tasks SET title=?,updated=? WHERE id=?",new Object[]{value,now(),t[0]});t[1]=value;},()->details(t));')
s=s.replace('if(event.getActionMasked()==2&&!dragging','if(event.getActionMasked()==2&&inlineEditor==null&&!dragging')
pos=s.index(' void renameQueue()')
s=s[:pos]+''' InlineTitle inlineEditor;
 class InlineTitle extends androidx.appcompat.widget.AppCompatEditText{
 final Submit save;final Runnable singleTap;String original;boolean editing,finishing;final GestureDetector gestures;
 InlineTitle(String value,Submit saveAction,Runnable tap){super(MainActivity.this);save=saveAction;singleTap=tap;setText(value);setTextSize(17);setTextColor(ink);setBackground(null);setSingleLine(true);setEllipsize(android.text.TextUtils.TruncateAt.END);setPadding(dp(4),dp(12),dp(4),dp(12));setFocusable(false);setFocusableInTouchMode(false);setCursorVisible(false);setInputType(android.text.InputType.TYPE_CLASS_TEXT|android.text.InputType.TYPE_TEXT_FLAG_CAP_SENTENCES);setImeOptions(android.view.inputmethod.EditorInfo.IME_ACTION_DONE);setContentDescription("标题，双击原位编辑");
 gestures=new GestureDetector(MainActivity.this,new GestureDetector.SimpleOnGestureListener(){public boolean onDown(android.view.MotionEvent e){return true;}public boolean onSingleTapConfirmed(android.view.MotionEvent e){if(singleTap!=null&&!editing)singleTap.run();return true;}public boolean onDoubleTap(android.view.MotionEvent e){begin();return true;}});gestures.setIsLongpressEnabled(false);
 setOnFocusChangeListener((v,focus)->{if(!focus&&editing)finish(true);});setOnEditorActionListener((v,action,event)->{if(action==android.view.inputmethod.EditorInfo.IME_ACTION_DONE||(event!=null&&event.getKeyCode()==KeyEvent.KEYCODE_ENTER)){if(event==null||event.getAction()==KeyEvent.ACTION_UP)finish(true);return true;}return false;});}
 public boolean onTouchEvent(android.view.MotionEvent event){if(editing)return super.onTouchEvent(event);return gestures.onTouchEvent(event);}
 void begin(){if(editing)return;if(inlineEditor!=null)inlineEditor.finish(true);original=getText().toString();editing=true;inlineEditor=this;setFocusableInTouchMode(true);setFocusable(true);setCursorVisible(true);setEllipsize(null);setBackgroundTintList(android.content.res.ColorStateList.valueOf(accent));requestFocus();selectAll();post(()->((android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE)).showSoftInput(this,android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT));}
 void finish(boolean commit){if(!editing||finishing)return;finishing=true;String value=getText().toString().trim();boolean changed=commit&&!value.isEmpty()&&!value.equals(original);editing=false;if(inlineEditor==this)inlineEditor=null;if(changed){save.run(value);setText(value);}else setText(original);setCursorVisible(false);clearFocus();setFocusable(false);setFocusableInTouchMode(false);setEllipsize(android.text.TextUtils.TruncateAt.END);((android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE)).hideSoftInputFromWindow(getWindowToken(),0);finishing=false;}
 public boolean onKeyPreIme(int key,KeyEvent event){if(key==KeyEvent.KEYCODE_BACK&&editing){if(event.getAction()==KeyEvent.ACTION_UP)finish(false);return true;}return super.onKeyPreIme(key,event);}
 }
 @Override public void onBackPressed(){if(inlineEditor!=null){inlineEditor.finish(false);return;}super.onBackPressed();}
''' +s[pos:]
# Avoid replacing the title while typing when another action rebuilds the page.
s=s.replace(' void show(){',' void show(){\n if(inlineEditor!=null)inlineEditor.finish(true);')
p.write_text(s,'utf-8')
p=Path('app/build.gradle');p.write_text(p.read_text().replace("versionCode 17; versionName '2.2.2'","versionCode 18; versionName '2.3'"))
