# lapo 官网

轻量静态网站，无前端依赖、无运行时 JavaScript。直接打开 `index.html` 即可浏览；部署时上传四个 HTML 文件、`style.css` 和 `assets/` 到静态托管服务，同样支持部署到子目录。

- `index.html`：产品介绍与协议入口。
- `privacy.html`：隐私政策。
- `terms.html`：用户协议。
- `minors.html`：未成年人个人信息保护规则。

## 同步协议

协议内容源自 `../ecce-app/assets/legal/`，不另行改写条款。修改 App 中的源文件后，在本目录运行：

```sh
python3 sync_legal.py
```

脚本使用与 App 相同的四个环境变量填写运营信息：`LAPO_LEGAL_OPERATOR`、`LAPO_PRIVACY_CONTACT`、`LAPO_DATA_REGION`、`LAPO_CLOUD_PROVIDER`。官网运营主体默认使用已确认的 `小海懒科技(深圳)有限公司`，其他未设置的信息显示“尚未公布”。环境变量可覆盖默认值；补齐信息后，再运行同步命令生成页面。重新生成会覆盖三个协议 HTML 文件，请勿直接修改生成文件。

当前未配置应用商店下载地址，首页不显示下载按钮。发布前请补全真实运营信息及下载地址；协议版本与日期沿用源文件。本次未添加测试用例或运行功能测试。
