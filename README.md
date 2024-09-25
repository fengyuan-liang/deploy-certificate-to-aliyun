# deploy-certificate-to-aliyun
自动部署泛解析证书到阿里云CDN上



## 如何使用

fork该项目，并填写对应参数，再push一次代码即可（随便改点啥，workflow需要push才能触发）

 GitHub 仓库的 "Settings" -> "Secrets and variables" -> "Actions" 中添加以下 secrets：

- `ALIYUN_ACCESS_KEY_ID`：阿里云账户AK
- `ALIYUN_ACCESS_KEY_SECRET`：阿里云账户SK
- `DOMAINS`: 要设置域名的二级域名，例如要设置*.example.com，这里填写的就是example.com, 多个域名用英文逗号隔开
- `ALIYUN_CDN_DOMAINS`：设置阿里云cdn域名，一般是三级域名，例如cdn.example.com，需要跟上面的DOMAINS对应，否则会设置错误
- `EMAIL`:  证书过期时提醒的邮件





## 相关文档

> 这里使用的是阿里云提供的api进行的调用
>
> - 设置CDN证书：https://next.api.aliyun.com/document/Cdn/2018-05-10/SetCdnDomainSSLCertificate
