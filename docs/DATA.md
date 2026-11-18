# 数据模型与备份协议

数据库：应用私有目录 databases/deque.db，无远程连接。

|表|字段|
|---|---|
|queues|id TEXT PRIMARY KEY；name TEXT；tail INTEGER DEFAULT 1；updated INTEGER；deleted INTEGER DEFAULT 0；reminderMinutes INTEGER DEFAULT 60；position INTEGER DEFAULT 0|
|tasks|id TEXT PRIMARY KEY；queueId TEXT；title TEXT；position INTEGER；state INTEGER DEFAULT 0；updated INTEGER；completed INTEGER 可空；notes TEXT DEFAULT ''；deadline INTEGER DEFAULT 0|
|preferences|key TEXT PRIMARY KEY；value INTEGER|

id 使用 UUID；tail=0 队头/1 队尾，state=0 待办/1 完成，deleted=1 为队列墓碑。时间统一毫秒，deadline=0 为未设置。preferences 当前 key=tail 表示新队列默认位置。tasks 数组下标：0 id、1 title、2 position、3 notes、4 deadline、5 completed；修改查询时必须同步绑定和编辑代码。
迁移通过 CREATE TABLE IF NOT EXISTS 和 PRAGMA table_info / ALTER TABLE，无正式 schema 版本号。旧 queues.position 默认 0，同值用 rowid 保持读取顺序。建议二次开发先建立版本化迁移和测试，不可通过删库解决升级问题。

## JSON v1

```json
{
  "format": "deque-backup",
  "version": 1,
  "exportedAt": 1763164800000,
  "queues": [{"id":"q1","name":"我的一天","tail":1,"updated":1763164800000,"deleted":0,"reminderMinutes":60,"position":0}],
  "tasks": [{"id":"t1","queueId":"q1","title":"示例","position":0,"state":0,"updated":1763164800000,"completed":null,"notes":"备注","deadline":0}],
  "preferences": [{"key":"tail","value":1}]
}
```

导出遍历三表全部字段，事务获取一致快照；NULL 转 JSON null。备份是明文，不含音效、APK、签名或系统设置。
导入读取上限 20MiB、10000 队列、100000 事项；检查 format/version、必要字段类型、范围、重复 ID 和 queueId 引用。position 对旧队列备份可省略，导入 optLong 默认 0；该可选字段目前没有与其他必需字段相同的严格类型校验，这是已知限制。
校验后事务写入；为所有队列和事项生成新 UUID，映射 queueId；保留墓碑、状态与元数据，preferences 按 key 替换。失败回滚全部写入。重复导入产生副本，不做去重或冲突合并。不要将 v1 悄悄改成覆盖恢复；未来变更需显式版本和迁移。
导出未限制文件大小，极大数据可能超过当前导入上限；失败导出可能留有不完整文件，需重新导出。文件通过系统 SAF 选择，后台线程读写，目前尚未完整处理 Activity 重建回调问题。

## 同步扩展
当前 UUID/updated/队列墓碑只提供基础，不代表已支持同步。任务物理删除需要改为可同步墓碑；引入事务 outbox、设备 ID、幂等 operationId、服务端递增版本和增量游标。队列顺序整体原子提交，冲突按版本处理，不仅比较客户端时间。PC 端复用协议，不能直接共享正在使用的 SQLite 文件。
