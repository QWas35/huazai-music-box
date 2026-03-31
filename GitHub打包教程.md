# 华仔音乐盒 Android APK 打包教程
## 方案一：GitHub Actions 自动打包（免费、全自动）

---

## 第一步：注册 GitHub 账号

1. 打开浏览器，访问 **https://github.com/signup**
2. 填写信息：
   - **Username**（用户名）：自己起一个英文名，比如 `huazai2024`
   - **Email**（邮箱）：填你的常用邮箱
   - **Password**（密码）：设置一个强密码
3. 点击 **Create account**
4. 验证邮箱（去邮箱收验证邮件，点击确认）

> ⚠️ 如果已有 GitHub 账号，跳过此步，直接登录 https://github.com/login

---

## 第二步：创建 GitHub 仓库

1. 登录 GitHub 后，点击右上角 **"+"** 号，选择 **"New repository"**
2. 填写信息：
   - **Repository name**（仓库名）：`huazai-music-box`
   - **Description**（描述）：`🎵 华仔音乐盒 Android多源音乐搜索播放器`
   - **Public** 或 **Private** 都可以（选 Public 更简单）
3. ⚠️ **不要勾选** "Add a README file"
4. 点击 **"Create repository"**

---

## 第三步：生成 GitHub Token（令牌）

1. 点击右上角头像 → 选择 **"Settings"**（设置）
2. 左侧菜单最下方找到 **"Developer settings"**（开发者设置）
3. 左侧菜单点击 **"Personal access tokens"** → **"Tokens (classic)"**
4. 点击 **"Generate new token"** → 选择 **"Generate new token (classic)"**
5. 填写：
   - **Note**：写 `华仔音乐盒打包`
   - **Expiration**：选 `30 days`（30天有效）
   - **勾选权限**：只勾选 **`repo`**（完整的仓库控制权限）
6. 点击页面最下方绿色按钮 **"Generate token"**
7. **复制显示的 Token**（只显示一次！类似 `ghp_xxxxxxxxxxxxxxxx`）

> 💡 把 Token 复制到记事本保存，后面要用

---

## 第四步：获取 GitHub 用户名

- 看右上角头像下方显示的名字
- 或者打开 https://github.com/settings 页面，顶部显示的就是你的用户名

> 例如用户名是 `huazai2024`，后面要用

---

## 第五步：运行一键打包脚本

1. 打开文件夹：`C:\Users\lenovo\.qclaw\workspace\华仔音乐盒_android`
2. **双击运行** `trigger_build.py`
3. 按提示输入：
   - 第一个提示：粘贴刚才复制的 **GitHub Token**，按回车
   - 第二个提示：输入你的 **GitHub 用户名**，按回车
4. 等待脚本执行完成

**脚本会自动完成：**
- ✅ 创建 GitHub 仓库
- ✅ 上传代码
- ✅ 触发自动构建

---

## 第六步：等待构建（约 15-20 分钟）

1. 脚本会输出一个链接，格式类似：
   ```
   https://github.com/你的用户名/huazai-music-box/actions
   ```
2. 打开这个链接，可以看到构建进度
3. 看到 **绿色 ✅** 表示构建成功

**如果 Actions 页面是空的：**
1. 打开 https://github.com/你的用户名/huazai-music-box
2. 点击 **"Actions"** 标签
3. 左侧选择 **"Build Android APK"** 工作流
4. 点击 **"Enable workflow"**（启用工作流）
5. 然后点击 **"Run workflow"** → **"Run workflow"**

---

## 第七步：下载 APK

构建完成后（绿色 ✅）：

1. 点击构建记录（最新的一条）
2. 滚动到页面底部，找到 **"Artifacts"** 区域
3. 点击 **"huazaimusicbox-apk"** 下载
4. 下载后是一个 **.zip** 压缩包
5. 解压后得到 **.apk** 文件

---

## 第八步：安装到手机

1. 把 APK 文件传到手机（微信/QQ发送、数据线连接、网盘都行）
2. 在手机上打开 APK 文件
3. 如果提示"未知来源"，去 **设置 → 安全 → 允许安装未知来源应用**
4. 点击 **安装**
5. 安装完成后打开就能用！

---

## 📱 支持的 Android 版本

- Android 5.0 及以上
- 绝大多数 2015 年以后的手机都支持

---

## ❓ 常见问题

### Q1: 脚本运行报错 "git push 失败"
- 检查 Token 是否正确复制
- 检查用户名是否正确
- 确认 GitHub 仓库已创建

### Q2: Actions 构建失败
- 打开 Actions 页面，点击失败的构建查看错误日志
- 通常是代码格式问题，把错误截图给我帮你解决

### Q3: 找不到 Artifacts 下载
- 确认构建状态是绿色 ✅（不是红色 ❌）
- 只有成功的构建才会有下载

### Q4: APK 安装失败
- 检查手机系统版本（需 >= Android 5.0）
- 检查手机存储空间（需要约 50MB）
- 开启"允许安装未知来源应用"

### Q5: 想重新打包（改了代码后）
- 直接运行 `trigger_build.py`，会自动更新代码并触发构建
- 或者去 GitHub 仓库页面，Actions → Run workflow

---

## 📞 需要帮助？

遇到任何问题，提供以下信息：
1. 哪一步出错了
2. 错误信息的截图
3. 你的 GitHub 用户名

我帮你远程排查解决！
