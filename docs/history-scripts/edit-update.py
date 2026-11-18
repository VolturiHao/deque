from pathlib import Path
p=Path('app/src/main/java/cn/deque/MainActivity.java');s=p.read_text('utf-8')
a=s.index('menu.setOnMenuItemClickListener(item->{input(');b=s.index('menu.show();',a)
s=s[:a]+'menu.setOnMenuItemClickListener(item->{taskForm(t);return true;});'+s[b:]
s=s.replace('void addTask(){','void addTask(){taskForm(null);}\n void taskForm(String[] task){')
s=s.replace('sheet("添加事项","给想做的事，留一个位置。")','sheet(task==null?"添加事项":"编辑事项",task==null?"给想做的事，留一个位置。":"更新内容、备注与截止时间。")')
s=s.replace('form.addView(field);EditText notes','if(task!=null)edit.setText(task[1]);form.addView(field);EditText notes')
s=s.replace('final long[] deadline={0};TextView ddl=label("DDL · 未设置",14);','if(task!=null)notes.setText(task[3]);final long[] deadline={task==null?0:Long.parseLong(task[4])};TextView ddl=label(deadline[0]==0?"DDL · 未设置":"DDL · "+date(deadline[0]),14);')
a=s.index('button(form,"选择日期和时间",');b=s.index('button(form,"清除 DDL"',a)
s=s[:a]+'button(form,"选择日期和时间",()->pickDeadline(deadline[0],value->{deadline[0]=value;ddl.setText("DDL · "+date(value));}));'+s[b:]
s=s.replace('position<2;position++','position<(task==null?2:1);position++')
s=s.replace('add.setText(atTail?"添加到队尾":"添加到队头");','add.setText(task!=null?"保存修改":atTail?"添加到队尾":"添加到队头");')
s=s.replace('db.execSQL("INSERT INTO tasks(id,queueId,title,position,state,updated,completed,notes,deadline)', 'if(task!=null){db.execSQL("UPDATE tasks SET title=?,notes=?,deadline=?,updated=? WHERE id=?",new Object[]{value,notes.getText().toString().trim(),deadline[0],now(),task[0]});}else db.execSQL("INSERT INTO tasks(id,queueId,title,position,state,updated,completed,notes,deadline)')
pos=s.index(' LinearLayout sheet(')
s=s[:pos]+''' interface DeadlineSelected{void accept(long value);}
 void pickDeadline(long existing,DeadlineSelected selected){Calendar initial=Calendar.getInstance();if(existing>0)initial.setTimeInMillis(existing);LinearLayout panel=column();panel.setPadding(dp(12),dp(8),dp(12),dp(8));LinearLayout wheels=new LinearLayout(this);panel.addView(wheels);String[] units={"年","月","日","时","分"};NumberPicker[] pickers=new NumberPicker[5];int year=initial.get(Calendar.YEAR);int[] min={Math.min(1900,year),1,1,0,0},max={Math.max(2100,year),12,31,23,59},values={year,initial.get(Calendar.MONTH)+1,initial.get(Calendar.DAY_OF_MONTH),initial.get(Calendar.HOUR_OF_DAY),initial.get(Calendar.MINUTE)};for(int i=0;i<5;i++){LinearLayout col=column();TextView unit=label(units[i],12);unit.setGravity(Gravity.CENTER);col.addView(unit);NumberPicker picker=new NumberPicker(this);picker.setMinValue(min[i]);picker.setMaxValue(max[i]);picker.setValue(values[i]);picker.setWrapSelectorWheel(false);picker.setDescendantFocusability(NumberPicker.FOCUS_BLOCK_DESCENDANTS);picker.setContentDescription(units[i]);pickers[i]=picker;col.addView(picker,new LinearLayout.LayoutParams(-1,dp(150)));wheels.addView(col,new LinearLayout.LayoutParams(0,-2,i==0?1.4f:1));}
 Runnable updateDays=()->{Calendar c=Calendar.getInstance();c.set(Calendar.DAY_OF_MONTH,1);c.set(Calendar.YEAR,pickers[0].getValue());c.set(Calendar.MONTH,pickers[1].getValue()-1);int days=c.getActualMaximum(Calendar.DAY_OF_MONTH);if(pickers[2].getValue()>days)pickers[2].setValue(days);pickers[2].setMaxValue(days);};pickers[0].setOnValueChangedListener((p,oldValue,newValue)->updateDays.run());pickers[1].setOnValueChangedListener((p,oldValue,newValue)->updateDays.run());updateDays.run();new com.google.android.material.dialog.MaterialAlertDialogBuilder(this).setTitle("截止时间").setView(panel).setNegativeButton("取消",null).setPositiveButton("确定",(d,which)->{Calendar c=Calendar.getInstance();c.clear();c.set(pickers[0].getValue(),pickers[1].getValue()-1,pickers[2].getValue(),pickers[3].getValue(),pickers[4].getValue());selected.accept(c.getTimeInMillis());}).show();}
''' +s[pos:]
p.write_text(s,'utf-8')
p=Path('app/build.gradle');p.write_text(p.read_text().replace("versionCode 6; versionName '1.5'","versionCode 7; versionName '1.6'"))
