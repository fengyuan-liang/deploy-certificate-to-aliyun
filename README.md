# deploy-certificate-to-aliyun
自动部署泛解析证书到阿里云上





## 如何使用

fork该项目，并填写对应参数即可

 GitHub 仓库的 "Settings" -> "Secrets and variables" -> "Actions" 中添加以下 secrets：

- `ALIYUN_ACCESS_KEY_ID`：阿里云账户AK
- `ALIYUN_ACCESS_KEY_SECRET`：阿里云账户SK
- `DOMAIN`: 要设置域名的二级域名，例如要设置*.example.com，这里填写的就是example.com, 多个域名用英文逗号隔开
- `ALIYUN_CDN_DOMAIN`：设置阿里云cdn域名，一般是三级域名，例如cdn.example.com，需要跟上面的DOMAINS对应，否则会设置错误





## 相关文档

> 这里使用的是阿里云提供的api进行的调用
>
> - 上传证书：https://next.api.aliyun.com/document/cas/2020-04-07/UploadUserCertificate
> - 设置CDN证书：https://next.api.aliyun.com/document/Cdn/2018-05-10/SetCdnDomainSSLCertificate
