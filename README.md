# Deploy Certificate to Aliyun

每两个月自动部署泛解析证书到阿里云CDN上

## ✨ 功能特点

- 🔄 自动续期 Let's Encrypt 泛域名证书
- ☁️ 自动部署到阿里云 CDN
- ⏰ 每两个月自动运行一次
- 📧 证书过期邮件提醒
- 🔒 使用 GitHub Secrets 保护敏感信息

## 🚀 如何使用

### 第一步：Fork 项目仓库

1. 打开本项目的 GitHub 仓库页面
2. 点击页面右上角的 **"Fork"** 按钮
3. 这会在您的 GitHub 账户下创建一个完整的副本

### 第二步：配置阿里云访问密钥（AK/SK）

为了能让 GitHub 的脚本有权限操作您的阿里云账户，您需要提供一个具有相应权限的 AccessKey。

1. 登录[阿里云控制台](https://homenew.console.aliyun.com/)，进入 **访问控制 (RAM)** 页面
2. 创建一个专用于此项目的用户（推荐，出于安全最佳实践）
3. 为该用户授权以下策略权限：
   - `AliyunDNSFullAccess`（管理DNS解析，用于自动验证域名所有权）
   - `AliyunCDNFullAccess`（管理CDN，用于上传和部署证书）
   - `AliyunYundunCertFullAccess`（管理SSL证书服务）
4. 为这个用户创建一个 **AccessKey (AK/SK)**，并妥善保存

### 第三步：在 GitHub 仓库中设置秘密变量

1. 进入您 **Fork 出来的仓库** 的页面
2. 点击顶部的 **"Settings"** 选项卡
3. 在左侧边栏中找到 **"Secrets and variables" → "Actions"**
4. 点击 **"New repository secret"** 按钮，逐个添加以下秘密变量：

| 变量名                     | 说明                                               | 示例值                         |
| :------------------------- | :------------------------------------------------- | :----------------------------- |
| `ALIYUN_ACCESS_KEY_ID`     | 阿里云 AccessKey ID                                | `LTAI5txxxxxxxxxxxxx`          |
| `ALIYUN_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret                            | `h6J9Zxxxxxxxxxxxxxxxxxxxx`    |
| `DOMAINS`                  | 主域名，多个用**英文逗号**隔开                     | `example.com,test.org`         |
| `ALIYUN_CDN_DOMAINS`       | CDN域名，与DOMAINS顺序对应，多个用**英文逗号**隔开 | `cdn.example.com,img.test.org` |
| `EMAIL`                    | 接收通知的邮箱地址                                 | `your-email@example.com`       |

### 第四步：手动触发工作流运行

1. 在仓库顶部的 **"Actions"** 选项卡中选中action, 执行右边的`Run workflow`

### 第五步：查看执行结果

1. 点击仓库顶部的 **"Actions"** 选项卡
2. 查看工作流运行状态和详细日志
3. 如果所有配置正确，工作流会显示绿色的对勾（✅），表示执行成功
4. 登录 [阿里云CDN控制台](https://cdn.console.aliyun.com/)，检查证书是否已更新

## ⚠️ 重要注意事项

- **安全性**：阿里云 AK/SK 是非常敏感的凭证，务必通过 **Secrets** 的方式配置，绝不要直接写在代码文件里
- **分隔符**：多个域名之间使用**英文逗号**分隔，不要使用空格或其他符号
- **首次运行**：建议手动触发一次以确保配置无误
- **费用**：Let's Encrypt 证书本身是免费的，但关联的阿里云CDN、DNS等服务可能会产生正常费用 

## 🔧 技术支持

如果您遇到问题，请：

1. 检查 GitHub Actions 日志中的错误信息
2. 确保所有秘密变量已正确设置
3. 确认阿里云 RAM 用户具有所需权限

------

至此，您就完成了所有设置，之后每隔约60天，GitHub 就会自动帮你免费续期并部署证书，一劳永逸。
