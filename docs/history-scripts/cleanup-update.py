from pathlib import Path
p=Path('app/src/main/java/cn/deque/MainActivity.java');s=p.read_text('utf-8')
s=s.replace('SELECT id,title,position,notes,deadline FROM tasks','SELECT id,title,position,notes,deadline,completed FROM tasks').replace('c.getString(3),c.getString(4)}','c.getString(3),c.getString(4),c.isNull(5)?"0":c.getString(5)}')
pos=s.index(' void details(')
s=s[:pos]+''' boolean overdue(String[] t){long ddl=Long.parseLong(t[4]);return ddl>0&&now()>=ddl;}
 void deleteTask(String[] t){new com.google.android.material.dialog.MaterialAlertDialogBuilder(this).setTitle("删除事项？").setMessage("将直接删除「"+t[1]+"」，此操作无法撤销。").setNegativeButton("取消",null).setPositiveButton("删除",(d,k)->{db.execSQL("DELETE FROM tasks WHERE id=?",new Object[]{t[0]});show();}).show();}
 void clearTrash(){new com.google.android.material.dialog.MaterialAlertDialogBuilder(this).setTitle("清除全部已完成事项？").setMessage("仅清除当前队列的回收站，此操作无法撤销。").setNegativeButton("取消",null).setPositiveButton("清除",(d,k)->{db.execSQL("DELETE FROM tasks WHERE queueId=? AND state=1",new Object[]{queue});show();}).show();}
''' +s[pos:]
# Timer refresh also catches transition from upcoming to overdue.
s=s.replace('(urgent(t)?1:0)','(urgent(t)?(overdue(t)?2:1):0)')
s=s.replace('TaskAdapter adapter=new TaskAdapter(rows);','if(trash){button(root,"清空当前回收站",()->clearTrash());}\n TaskAdapter adapter=new TaskAdapter(rows);')
s=s.replace('if(Long.parseLong(t[4])>0)sub.setText((urgent(t)?"即将截止 / 已逾期 · ":"DDL · ")+date(Long.parseLong(t[4])));if(urgent(t))sub.setTextColor(0xff9b3029);','if(trash){sub.setText("完成于 "+(Long.parseLong(t[5])>0?date(Long.parseLong(t[5])):"时间未记录"));}else if(Long.parseLong(t[4])>0){sub.setText((overdue(t)?"⚠ 已逾期 · ":urgent(t)?"◷ 即将截止 · ":"DDL · ")+date(Long.parseLong(t[4])));}if(urgent(t))sub.setTextColor(overdue(t)?0xff8e211c:0xff9b3029);')
s=s.replace('h.card.setStrokeColor(urgent(t)?0xffd89690:0xffb9cfbe)','h.card.setStrokeColor(urgent(t)?(overdue(t)?0xffb84b42:0xffd89690):0xffb9cfbe)')
s=s.replace('menu.getMenu().add("编辑事项");menu.setOnMenuItemClickListener(item->{taskForm(t);return true;});','menu.getMenu().add("编辑事项");menu.getMenu().add("删除事项");menu.setOnMenuItemClickListener(item->{if("删除事项".contentEquals(item.getTitle()))deleteTask(t);else taskForm(t);return true;});')
s=s.replace('menu.show();});','menu.show();});if(trash){LinearLayout clearRow=new LinearLayout(MainActivity.this);clearRow.setGravity(Gravity.END);button(clearRow,"清除该事项",()->{db.execSQL("DELETE FROM tasks WHERE id=? AND state=1",new Object[]{t[0]});show();});h.body.addView(clearRow);}')
p.write_text(s,'utf-8')
p=Path('app/build.gradle');p.write_text(p.read_text().replace("versionCode 7; versionName '1.6'","versionCode 8; versionName '1.7'"))
