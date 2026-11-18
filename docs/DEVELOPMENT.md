# 开发维护流程

## 环境准备
当前版本 2.3.3（21）。使用 Android Studio 打开 Deque 根目录，Gradle JDK 选择 17。Gradle Wrapper 固定 8.0.2，AGP 8.0.2，compileSdk/targetSdk 33，minSdk 23。依赖 Material 1.9.0、RecyclerView 1.3.0。
本机 SDK=F:\SDK，JDK=F:\Java\jdk-17.0.5。local.properties 配置 sdk.dir，不提交其他开发者的本机路径。首次构建需要网络下载 Wrapper/依赖；禁止直接把 IDE 选择的最新 Gradle 替换进项目。

在 PowerShell 的项目根目录：

```powershell
$env:JAVA_HOME='F:\Java\jdk-17.0.5'
$env:ANDROID_HOME='F:\SDK'
.\gradlew.bat :app:assembleDebug :app:lintDebug
```

SDK 至少安装 Platform 33、Platform Tools 和 AGP 所需 Build Tools，出现缺组件提示时用 SDK Manager 安装。普通开发无需签名密码；发布需要本机签名配置，见 RELEASE.md。

## 日常迭代
1. 阅读 FEATURES.md 确认规则及 QA.md 的关联回归项。
2. 修改源文件，而非执行 docs/history-scripts 中的一次性改写脚本。
3. 涉及字段或状态时同步更新迁移、查询数组、Backup、文档和测试。
4. 构建 debug，运行 Lint；备份相关变更运行 BackupCheck。
5. 在设备验证本次影响的场景，数据破坏性测试使用测试队列/隔离数据库。
6. 修改 docs/HISTORY.md；发布前递增 app/build.gradle 的版本，按 RELEASE.md 交付。

## 常见修改入口

|需求|需要检查|
|---|---|
|新增事项字段|建表/迁移、show 查询及下标、taskForm、卡片/details、Backup 与测试|
|修改排序|edge、persist、TaskAdapter.sort、urgent、队列 position 及导入|
|改主题|values/styles.xml、values-night/styles.xml、tone() 硬编码颜色、Canvas 图标 tint|
|改标题编辑|InlineTitle、dispatchTouchEvent、tick 暂停条件、键盘/返回/焦点行为|
|新增全局设置|preferences 表、globalSettings、Backup、默认值回退|
|接入音效|res/raw/completion.mp3 或 wav/ogg，只保留一种；见 AUDIO.md|
|改启动图标|SVG、前景、monochrome、legacy、mipmap 旧版及 API 26/33 资源|

## 测试与调试

```powershell
.\gradlew.bat :app:assembleDebugAndroidTest
adb devices
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb install -r app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
adb shell am instrument -w cn.deque.test/cn.deque.BackupCheck
adb logcat -s AndroidRuntime:E
```

BackupCheck 使用内存数据库，不修改用户数据；验证往返数量、字段与引用重映射、错误引用拒绝。测试 APK 不是正式交付物。设备若已安装 release，不要为运行 debug 测试卸载用户数据；使用独立模拟器或先备份。
Lint HTML 报告在 app/build/reports/；其通过不代表手势、动画和系统输入法全部可用。UI 回归见 QA.md。

## 故障排查
- 签名冲突：debug 与 release 不能互相覆盖；先备份再迁移，不要为消除报错重建正式密钥。
- 版本降级：检查 versionCode，后续正式发布始终递增。
- SDK 路径错误：检查 local.properties 和 SDK Manager，环境变量并非唯一依据。
- Gradle native-platform.dll：确认 JDK/Gradle 安装与执行权限；本会话曾因沙箱限制失败，不应据此改业务代码。
- 图标旧缓存：先重启启动器/设备，不要为了刷新图标直接卸载有数据的应用。
- DDL 不在后台通知：当前设计仅前台视觉提醒。

## 二次开发建议
先建立 Task/Queue 类型模型与 Repository，逐步拆分 Activity，再引入 ViewModel/生命周期安全文件任务。数据库转版本化迁移并补外键、索引和升级测试；自动测试补状态排序、撤销、原位编辑、滚轮与手势。新增同步前阅读 DATA.md，不把备份副本导入当成同步合并。
