# 序 · DEQUE

离线 Android 待办队列应用，当前版本 **2.3.3（versionCode 21）**。Java 17 / Android Views / Material 3 / SQLite，最低 Android 6。

## 文档

从 [开发文档索引](docs/README.md) 开始：

- [项目结构与架构](docs/ARCHITECTURE.md)
- [功能设计](docs/FEATURES.md)
- [开发维护流程](docs/DEVELOPMENT.md)
- [数据模型与备份协议](docs/DATA.md)
- [构建打包发布](docs/RELEASE.md)
- [验收清单](docs/QA.md)
- [历史迭代记录](docs/HISTORY.md)

## 使用与开发

支持多队列、长按排序、独立回收站、备注、DDL 自动置顶、原位重命名、深浅色主题及 JSON 导入导出。DDL 是前台视觉提醒，尚无后台通知或多端同步。

Android Studio 打开项目根目录，配置 JDK 17 和 SDK 33 后运行：

```powershell
.\gradlew.bat :app:assembleDebug :app:lintDebug
```

正式包及安装说明在 releases/，签名步骤见发布文档。debug 与 release 不能直接相互覆盖，卸载前必须先备份数据。

图标设计稿在 [design/app-icon.svg](design/app-icon.svg)，音效说明见 [AUDIO.md](AUDIO.md)。历史 Python 改写脚本在 docs/history-scripts/，不可重复执行。私钥 signing/、signing.properties 与 local.properties 不可提交或随 APK 分发。
