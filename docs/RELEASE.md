# 打包、签名与发布

当前交付：2.3.3 / versionCode 21，包名 cn.deque；Android 6 及以上。本项目当前正式 APK 面向侧载实机测试，不等同于完成应用商店上架审核。平台/商店要求需在上架时重新核对。

## 正式签名准备
签名材料只保存在本机，不得提交或复制进 releases：
- signing/release.jks：正式密钥，必须独立安全备份。
- signing.properties：密码和别名配置，同样需安全备份。

配置键如下，示例不包含真实密码：

```properties
storeFile=signing/release.jks
keyAlias=deque
storePassword=<本机密钥密码>
keyPassword=<本机密钥密码>
```

app/build.gradle 从此文件读取配置。不要打印真实配置到日志，不要重新生成密钥覆盖现有文件。正式签名证书 SHA-256（公开指纹，可比对身份）：

```text
4830f0d855c90f279240d22850373c2e7c0a83f71c1173af5e089e36ed639b5e
```

## 发布步骤
1. 确认本次代码、DATA/FEATURES 文档及相关测试一致。
2. 在 app/build.gradle 递增 versionCode，设置 versionName；不要仅改 APK 文件名。
3. 运行正式构建与 Lint：

```powershell
$env:JAVA_HOME='F:\Java\jdk-17.0.5'
.\gradlew.bat :app:assembleRelease :app:lintRelease
```

release 当前 debuggable=false、minifyEnabled=false。正式包路径 app/build/outputs/apk/release/app-release.apk；调试包位于 app/build/outputs/apk/debug/app-debug.apk。R8 尚未开启，不要把“未混淆”误认为 debug 构建。

4. 用实际已安装的 Build Tools 验证签名、版本与调试标志：

```powershell
& F:\SDK\build-tools\30.0.3\apksigner.bat verify --verbose --print-certs app/build/outputs/apk/release/app-release.apk
& F:\SDK\build-tools\30.0.3\aapt.exe dump badging app/build/outputs/apk/release/app-release.apk
```

确认命令退出成功、证书指纹正确、包名及版本正确，badging 没有 application-debuggable。以上工具路径为本机示例，其他机器替换为所装版本。构建签名验证警告应结合具体签名方案判断，不能只忽略所有警告。

5. 按 QA.md 执行实机验收并记录未覆盖项目。测试前导出备份，避免在真实事项上验证清除。
6. 将 APK 命名 Deque-<版本>-release.apk 放入 releases，并生成 SHA-256；不要混入 debug APK 或私钥。

```powershell
Copy-Item app/build/outputs/apk/release/app-release.apk releases/Deque-2.3.3-release.apk
$hash=(Get-FileHash releases/Deque-2.3.3-release.apk -Algorithm SHA256).Hash
"$hash  Deque-2.3.3-release.apk" | Set-Content releases/SHA256SUMS.txt
Copy-Item docs/RELEASE.md releases/INSTALL.md
```

下次发布需替换上例版本。交付目录只保留当前 APK、INSTALL.md、SHA256SUMS.txt；清理旧文件前确认路径与当前产物，源码、签名和用户备份不属于清理对象。
7. 更新 README 当前版本和 docs/HISTORY.md，写清实际验证结果，不将 QA 清单视为已通过证明。

## 实机安装与升级
当前文件：releases/Deque-2.3.3-release.apk。允许相应文件管理器安装未知来源应用后安装，或使用：

```powershell
adb install -r releases/Deque-2.3.3-release.apk
```

相同包名、相同正式密钥、递增 versionCode 才能正常覆盖升级。debug 签名不同：先在旧应用导出并确认 JSON 可读取，再卸载旧版，安装正式版，导入备份。卸载删除私有数据库；导入生成副本，不覆盖其他已有队列。
出现签名冲突不要直接卸载；先确认是否有未备份数据。发布回退不要使用 adb 强制降级或清库作为常规方案，应修复问题后以更高 versionCode 发布补丁。

## 发布记录的范围
2.3.3 已有 assembleRelease、lintRelease 通过记录；前序版本有备份往返和模拟器检查记录。没有完整覆盖所有 Android 版本、机型、输入法和大字体组合；完整体验以实际验收为准。
