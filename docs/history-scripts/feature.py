from pathlib import Path
p=Path('app/src/main/java/cn/deque/MainActivity.java');s=p.read_text('utf-8')
s=s.replace('if(queues().isEmpty()) createQueue','migrate(); if(queues().isEmpty()) createQueue',1)
pos=s.index(' ArrayList<String[]> queues()')
s=s[:pos]+''' void migrate(){addColumn("tasks","notes","TEXT DEFAULT ''");addColumn("tasks","deadline","INTEGER DEFAULT 0");addColumn("queues","reminderMinutes","INTEGER DEFAULT 60");}
 void addColumn(String table,String column,String type){boolean found=false;try(Cursor c=db.rawQuery("PRAGMA table_info("+table+")",null)){while(c.moveToNext())if(column.equals(c.getString(1)))found=true;}if(!found)db.execSQL("ALTER TABLE "+table+" ADD COLUMN "+column+" "+type);}
 final Handler timer=new Handler(Looper.getMainLooper());TaskAdapter active;boolean dragging=false;long signature=0;
 final Runnable tick=new Runnable(){public void run(){if(active!=null&&!trash&&!dragging){long next=0;for(String[] t:active.rows)next=next*31+(urgent(t)?1:0);if(next!=signature){signature=next;active.refresh();}}timer.postDelayed(this,1000);}};
 protected void onResume(){super.onResume();timer.removeCallbacks(tick);timer.post(tick);}
 protected void onPause(){timer.removeCallbacks(tick);super.onPause();}
 long reminder(){try(Cursor c=db.rawQuery("SELECT reminderMinutes FROM queues WHERE id=?",new String[]{queue})){return c.moveToFirst()?c.getLong(0)*60000L:3600000L;}}
 boolean urgent(String[] t){return !trash&&Long.parseLong(t[4])>0&&now()>=Long.parseLong(t[4])-reminder();}
 String date(long value){return new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm",Locale.getDefault()).format(new Date(value));}
 void restore(String[] t){new com.google.android.material.dialog.MaterialAlertDialogBuilder(this).setTitle("恢复到原队列").setItems(new String[]{"恢复到队头","恢复到队尾"},(d,k)->{db.execSQL("UPDATE tasks SET state=0,position=?,updated=?,completed=NULL WHERE id=?",new Object[]{edge(k==1),now(),t[0]});show();}).show();}
 void details(String[] t){new com.google.android.material.dialog.MaterialAlertDialogBuilder(this).setTitle(t[1]).setMessage((t[3].isEmpty()?"暂无备注":t[3])+"\\n\\nDDL："+(Long.parseLong(t[4])==0?"未设置":date(Long.parseLong(t[4])))).setPositiveButton("关闭",null).show();}
''' +s[pos:]
s=s.replace('SELECT id,title,position FROM tasks','SELECT id,title,position,notes,deadline FROM tasks').replace('c.getString(2)}','c.getString(2),c.getString(3),c.getString(4)}')
s=s.replace('TaskAdapter adapter=new TaskAdapter(rows);recycler.setAdapter(adapter);','TaskAdapter adapter=new TaskAdapter(rows);active=adapter;adapter.sort();recycler.setAdapter(adapter);')
s=s.replace('if(from<0||to<0)return false;','if(from<0||to<0||urgent(rows.get(from))||urgent(rows.get(to)))return false;dragging=true;')
s=s.replace('super.clearView(r,h);adapter.notifyDataSetChanged();','super.clearView(r,h);dragging=false;adapter.refresh();')
s=s.replace('public int getItemCount(){return rows.size();}','''void sort(){rows.sort((a,b)->{boolean ua=urgent(a),ub=urgent(b);if(ua!=ub)return ua?-1:1;if(ua)return Long.compare(Long.parseLong(a[4]),Long.parseLong(b[4]));return Long.compare(Long.parseLong(a[2]),Long.parseLong(b[2]));});}
 void refresh(){sort();notifyDataSetChanged();}
 public int getItemCount(){return rows.size();}''')
s=s.replace('new Object[]{k*1024L,now(),rows.get(k)[0]});db.setTransactionSuccessful();','new Object[]{k*1024L,now(),rows.get(k)[0]});db.setTransactionSuccessful();')
s=s.replace('persist(rows);adapter.notifyItemMoved','persist(rows);for(int k=0;k<rows.size();k++)rows.get(k)[2]=String.valueOf(k*1024L);adapter.notifyItemMoved')
s=s.replace('float fade=Math.min(i,6)/6f;','int normalIndex=0;for(int k=0;k<i;k++)if(!urgent(rows.get(k)))normalIndex++;float fade=Math.min(normalIndex,6)/6f;')
s=s.replace('int fill=trash?Color.WHITE:','int fill=urgent(t)?0xffffd9d5:trash?Color.WHITE:')
s=s.replace('h.card.setStrokeColor(0xffb9cfbe)','h.card.setStrokeColor(urgent(t)?0xffd89690:0xffb9cfbe)')
s=s.replace('if(trash)db.execSQL("UPDATE tasks SET state=0,position=?,updated=?,completed=NULL WHERE id=?",new Object[]{edge(true),now(),t[0]});else','if(trash){restore(t);return;}else')
s=s.replace('恢复到原队列队尾','选择恢复位置')
s=s.replace('title.setTypeface(null','if(!t[3].isEmpty())title.setText("▤  "+t[1]);title.setTypeface(null')
s=s.replace('text.addView(sub);','''if(Long.parseLong(t[4])>0)sub.setText((urgent(t)?"即将截止 / 已逾期 · ":"DDL · ")+date(Long.parseLong(t[4])));if(urgent(t))sub.setTextColor(0xff9b3029);text.addView(sub);h.body.setOnClickListener(v->details(t));text.setOnClickListener(v->details(t));''')
# Replace creation sheet with scrollable optional metadata controls.
s=s.replace('form.addView(field);LinearLayout actions','''form.addView(field);EditText notes=new EditText(this);notes.setHint("备注（选填）");notes.setMinLines(2);form.addView(notes);final long[] deadline={0};TextView ddl=label("DDL · 未设置",14);form.addView(ddl);button(form,"选择日期和时间",()->{Calendar c=Calendar.getInstance();new DatePickerDialog(this,(picker,y,m,day)->{Calendar selected=Calendar.getInstance();selected.set(y,m,day);new TimePickerDialog(this,(clock,hour,minute)->{selected.set(Calendar.HOUR_OF_DAY,hour);selected.set(Calendar.MINUTE,minute);selected.set(Calendar.SECOND,0);selected.set(Calendar.MILLISECOND,0);deadline[0]=selected.getTimeInMillis();ddl.setText("DDL · "+date(deadline[0]));},c.get(Calendar.HOUR_OF_DAY),c.get(Calendar.MINUTE),true).show();},c.get(Calendar.YEAR),c.get(Calendar.MONTH),c.get(Calendar.DAY_OF_MONTH)).show();});button(form,"清除 DDL",()->{deadline[0]=0;ddl.setText("DDL · 未设置");});LinearLayout actions''')
s=s.replace('INSERT INTO tasks VALUES(?,?,?,?,0,?,NULL)",new Object[]{id(),queue,value,edge(atTail),now()}','INSERT INTO tasks(id,queueId,title,position,state,updated,completed,notes,deadline) VALUES(?,?,?,?,0,?,NULL,?,?)",new Object[]{id(),queue,value,edge(atTail),now(),notes.getText().toString().trim(),deadline[0]}')
s=s.replace('dialog.setContentView(form);dialog.show();','ScrollView content=new ScrollView(this);content.addView(form);dialog.setContentView(content);dialog.show();')
s=s.replace('"新队列默认设置","删除队列"','"新队列默认设置","删除队列","DDL 提醒时限"')
s=s.replace('(d,n)->{if(n==0)','''(d,n)->{if(n==4)input("DDL 提醒时限（分钟）",String.valueOf(reminder()/60000),value->{try{long minutes=Long.parseLong(value);if(minutes<0||minutes>5256000)throw new NumberFormatException();db.execSQL("UPDATE queues SET reminderMinutes=?,updated=? WHERE id=?",new Object[]{minutes,now(),queue});show();}catch(NumberFormatException e){Toast.makeText(this,"请输入 0–5256000 的整数分钟",Toast.LENGTH_LONG).show();}});if(n==0)''')
p.write_text(s,'utf-8')
p=Path('app/build.gradle');p.write_text(p.read_text().replace("versionCode 5; versionName '1.4'","versionCode 6; versionName '1.5'"))
