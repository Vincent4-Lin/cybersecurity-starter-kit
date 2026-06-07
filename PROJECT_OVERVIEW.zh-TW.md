# 專案說明：Cybersecurity Starter Kit

這個專案是一個可以放上 GitHub 的資安入門作品。

它主要做兩件事：

1. 整理資安學習資料。
2. 提供一個 GitHub 專案安全檢查工具。

簡單說：

```text
這是一個「資安學習筆記 + GitHub repo 安全健康檢查器」。
```

## 為什麼做這個專案

GitHub 雖然有一些安全功能，例如 secret scanning、Dependabot、CodeQL，但很多檢查是：

- push 到 GitHub 的時候才做。
- push 到 GitHub 之後才提醒。
- 需要先設定才會跑。

所以這個專案想解決的是：

```text
在程式碼推上 GitHub 之前，先自己做一次基本檢查。
```

這樣可以提早發現：

- 不該上傳的 `.env`
- 疑似 API key / token / private key
- 缺少 `SECURITY.md`
- 缺少 `.gitignore`
- GitHub Actions 權限沒有明確設定
- 有套件檔案但沒有 Dependabot

## 這個專案可以怎麼用

### 1. 檢查自己的專案

在你要 push 到 GitHub 前，先進到你的專案資料夾，執行：

```bash
python3 repo-security-checker/check_repo_security.py .
```

它會掃描目前資料夾，然後輸出分數和問題清單。

例如：

```text
Score: 100/100
Findings: 0
```

代表目前沒有發現基本安全問題。

也可以安裝 pre-push hook：

```bash
sh scripts/install-pre-push-hook.sh
```

如果是在 Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-pre-push-hook.ps1
```

安裝後，每次你執行：

```bash
git push
```

Git 都會先自動跑安全檢查。

如果檢查發現 high 風險問題，就會取消 push。

### 2. 檢查 GitHub 上的公開 repo

也可以直接輸入 GitHub URL：

```bash
python3 repo-security-checker/check_repo_security.py https://github.com/owner/repo
```

工具會自動：

```text
clone repo 到暫存資料夾
掃描檔案
輸出報告
掃完刪掉暫存資料夾
```

這可以用來研究別人的公開 repo 有沒有基本安全設定。

## 它檢查什麼

| 檢查項目 | 意思 | 為什麼重要 |
|---|---|---|
| `README.md` | 專案說明 | 讓別人知道專案是什麼、怎麼使用。 |
| `LICENSE` | 授權條款 | 公開 repo 需要說清楚別人能不能使用或修改。 |
| `SECURITY.md` | 安全問題回報方式 | 如果有人發現漏洞，知道要怎麼安全回報。 |
| `.gitignore` | Git 忽略規則 | 避免 `.env`、暫存檔、private key 被加進 Git。 |
| `.env` / private key | 敏感檔案 | 可能包含密碼、API key、token，不該推上 GitHub。 |
| hardcoded secret | 寫在程式碼裡的 secret | 例如 `API_KEY=...`，可能造成帳號或服務被濫用。 |
| GitHub Actions | GitHub 自動化流程 | 可以自動跑測試、安全檢查、部署。 |
| Actions permissions | workflow 權限 | 權限太大會增加風險。 |
| Dependabot | 套件更新提醒 | 可以提醒有漏洞的依賴套件，並幫忙開 PR 更新。 |
| `pull_request_target` | 特殊 Actions 觸發方式 | 用錯可能讓外部 PR 接觸高權限環境，需要特別注意。 |

## GitHub 自己會不會檢查

會，但不是全部。

GitHub 會提供一些安全功能：

- Secret scanning push protection：push 時擋一些支援的 secret。
- Dependabot alerts：repo 上 GitHub 後，檢查依賴套件漏洞。
- Code scanning / CodeQL：設定後掃描程式碼漏洞。
- GitHub Actions：push 或 PR 後自動跑流程。

但是這些不代表你可以完全不用自己檢查。

原因是：

- 有些功能要設定才會跑。
- 有些檢查是 push 後才提醒。
- 有些 secret 格式不一定會被 GitHub 抓到。
- GitHub 不一定會提醒你缺 `README.md`、`SECURITY.md`、`.gitignore`。

所以這個工具的定位是：

```text
GitHub 檢查之前的第一層本機檢查。
```

## 這個工具不是什麼

這個工具不是：

- 不是完整漏洞掃描器。
- 不是 AI 安全審查工具。
- 不是可以保證 repo 100% 安全的工具。
- 不是拿來攻擊別人的工具。

它只是幫你做基本檢查。

如果要更完整，可以再搭配：

- Gitleaks
- TruffleHog
- Trivy
- OSV-Scanner
- CodeQL

## 專案資料夾內容

```text
docs/
  learning-roadmap.md          資安學習路線
  tools.md                     常見資安工具整理
  labs.md                      練習平台整理
  pre-push-security-checks.md  push 前可以做的安全檢查

checklists/
  github-repo-security.md      GitHub repo 安全 checklist
  web-app-security.md          Web App 安全 checklist

repo-security-checker/
  check_repo_security.py       主要檢查工具
  README.md                    工具使用說明

scripts/
  install-pre-push-hook.sh     macOS / Linux / Git Bash 用的 hook 安裝器
  install-pre-push-hook.ps1    Windows PowerShell 用的 hook 安裝器

tests/
  test_check_repo_security.py  單元測試
```

## 可以繼續加的功能

之後可以把這個專案升級成：

- 支援輸出 HTML 報告。
- 加更多 secret 掃描規則。
- 加更清楚的修復教學。
- 支援掃描 GitHub organization 多個 repo。
- 加一個簡單網頁版介面。
- 加 Gitleaks / Trivy / OSV-Scanner 整合。

## 一句話總結

這個專案是在做：

```text
幫使用者在 push GitHub 前，先檢查 repo 有沒有基本安全問題，
同時整理資安學習路線和工具資料。
```
