# 项目结构与架构

## 技术基线
Java 17、Android Views、AppCompat、Material Components 1.9.0、RecyclerView 1.3.0、SQLite。单 app 模块，applicationId/namespace 均为 cn.deque。无登录、无服务器、无网络同步；数据保存在应用私有数据库。

## 目录

```text
Deque/
├─ app/
│  ├─ build.gradle                 应用版本、依赖、构建类型和签名配置
│  └─ src/
│     ├─ main/
│     │  ├─ AndroidManifest.xml    应用入口、主题、图标
│     │  ├─ java/cn/deque/
│     │  │  ├─ MainActivity.java   当前界面与业务实现
│     │  │  └─ Backup.java         JSON 备份协议与数据库导入导出
│     │  └─ res/
│     │     ├─ values/             浅色主题、颜色、动画样式
│     │     ├─ values-night/       深色主题
│     │     ├─ anim/               侧栏进入/退出动画
│     │     ├─ drawable/           矢量图标
│     │     ├─ mipmap-anydpi*/     旧版、自适应、单色启动图标
│     │     └─ raw/                可选 completion 音效素材
│     └─ androidTest/             BackupCheck 测试及 instrumentation 声明
├─ design/app-icon.svg            可编辑图标设计稿
├─ docs/                          维护文档、历史脚本和检查素材
├─ releases/                      当前正式 APK、INSTALL.md、SHA256SUMS.txt
├─ gradle/wrapper/、gradlew*       固定版本构建入口
├─ build.gradle、settings.gradle  插件与仓库配置
├─ signing/release.jks            本地正式私钥，不入库
├─ signing.properties             本地签名密码，不入库
├─ local.properties               本机 SDK 路径，不入库
└─ AUDIO.md                       完成音效接入方法
```

`.gradle/`、`build/`、`app/build/`、`build-check/` 是可再生输出，`.idea/` 是 IDE 配置，`.screenshots/` 可能含早期本机检查素材。它们不是业务代码，不应将私有缓存或本机路径加入交付源代码。

## 当前实现边界
MainActivity 同时承担数据访问、布局创建、手势、动画与生命周期处理，尚未采用 MVVM、Repository 或 Room。不要把规划中的分层当作已经存在。

|入口/组件|职责|
|---|---|
|onCreate、migrate、addColumn|建表、兼容旧数据库、增加缺失字段|
|show、switchPage|创建主页、保持标题/标签稳定、切换内容区|
|TaskAdapter、TaskHolder|绑定卡片、备注/DDL/完成时间、完成恢复清除入口|
|drawer、QueueHolder|侧栏导航、队列拖动排序与底部操作|
|taskForm、pickDeadline|创建/编辑共用底部面板，年月日时分滚轮|
|InlineTitle|双击原位编辑、保存取消、编辑态文字宽度描边|
|tick、urgent、overdue|前台提醒状态检查和逾期判定|
|persist、edge|手动顺序重排、端点插入|
|globalSettings、onActivityResult|系统文件选择与后台文件读写|
|Backup|快照导出、文件校验、新 UUID 副本导入|

数据流：用户操作 → Activity 校验 → SQLite 写入 → show()/Adapter 刷新。DDL 每秒重算，提醒状态主要是显示排序，不将自动置顶写成永久手动位置。数据库未使用外键，导入引用校验在 Backup 中完成。

## 资源与图标
主题资源与 MainActivity.tone() 共同决定颜色，修改主题不能只改 XML。部分操作图标通过 icon() 的 Canvas 绘制，需保持线宽和触摸区域一致。启动图标书页中心为画布 (54,54)，叶子为右上装饰；修改时同步 SVG、自适应前景、单色和旧版资源。音效使用资源名 completion，缺少素材时静音。

## 已知限制
Activity 体积较大，任务使用 String[]，文件线程回调未完全生命周期隔离；横滑为自定义阈值识别而非 ViewPager；原位编辑、拖动、计时刷新存在交互耦合。大规模数据性能、旋转与输入法组合需要持续回归。当前只有备份核心自动测试，不能视作完整 UI 测试覆盖。
