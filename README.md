# BlueOSDoc

BlueOSDoc 抓取 [vivo BlueOS 应用开发文档](https://developers-watch.vivo.com.cn/) 并将其转换为 Markdown，方便离线查阅、二次整理和托管到 GitHub。

当前仓库已经包含一份抓取结果，输出目录为 `docs/`。

## 使用方法

运行成功后，会在当前目录生成或刷新 `docs` 文件夹，里面存放全部 Markdown 文档和资源文件。

如果你不想手动克隆仓库，也可以直接下载启动脚本一键运行。

Linux / macOS：

```bash
curl -L 'https://cdn.jsdelivr.net/gh/hanyu12138/blueosdoc@main/run_scraper-linux%26mac.sh' -o run_scraper-linux\&mac.sh || curl -L 'https://raw.githubusercontent.com/hanyu12138/blueosdoc/main/run_scraper-linux%26mac.sh' -o run_scraper-linux\&mac.sh || curl -L 'https://ghproxy.net/https://raw.githubusercontent.com/hanyu12138/blueosdoc/main/run_scraper-linux%26mac.sh' -o run_scraper-linux\&mac.sh && chmod +x './run_scraper-linux&mac.sh' && ./run_scraper-linux\&mac.sh
```

Windows PowerShell：

```powershell
Write-Host 'Downloading launcher...'; $content = $null; foreach ($url in @('https://cdn.jsdelivr.net/gh/hanyu12138/blueosdoc@main/run_scraper-win.cmd','https://raw.githubusercontent.com/hanyu12138/blueosdoc/main/run_scraper-win.cmd','https://ghproxy.net/https://raw.githubusercontent.com/hanyu12138/blueosdoc/main/run_scraper-win.cmd')) { try { Write-Host "Trying $url"; $content = (Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 15).Content; if ($content) { break } } catch {} }
if (-not $content) { throw 'Failed to download launcher from all sources.' }
Write-Host 'Writing launcher to local file...'
[System.IO.File]::WriteAllText((Join-Path (Get-Location) 'run_scraper-win.cmd'), ($content -replace "`r?`n", "`r`n"), [System.Text.UTF8Encoding]::new($false))
Write-Host 'Starting launcher...'
.\run_scraper-win.cmd
```

## 本地运行

```bash
python -m venv scraper_env
source scraper_env/bin/activate
pip install -r requirements.txt
python docs.py
```

Windows：

```powershell
python -m venv scraper_env
.\scraper_env\Scripts\Activate.ps1
pip install -r requirements.txt
python docs.py
```

## 自动更新

仓库自带 GitHub Actions 工作流：

- 支持手动触发
- 默认每月 1 日自动重新抓取一次
- 文档有变化时自动提交并推送到仓库

## 说明

- 抓取源站：`https://developers-watch.vivo.com.cn/`
- 当前默认抓取范围：`/reference/`、`/component/`、`/api/`、`/native/`
- 部分失效链接会在 `docs/manifest.json` 中记录为错误项

## 许可证

仓库中的脚本用于学习交流。`docs/` 内容来自 vivo BlueOS 官方开发文档，请勿用于侵犯原站权益的用途。
