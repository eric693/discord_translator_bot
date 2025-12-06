# Discord 翻譯機器人

一個支援中英雙向自動翻譯的 Discord 機器人。

## 功能特色

- 🔄 **雙向自動翻譯**：中文自動翻成英文，英文自動翻成中文
- 🌐 **無限次數翻譯**：沒有使用限制
- 🎯 **智能語言檢測**：自動識別輸入語言
- 🎨 **精美訊息格式**：使用 Discord Embed 顯示翻譯結果
- 📱 **多種指令別名**：支援中英文指令

## 可用指令

- `!translate [文字]` / `!翻譯 [文字]` / `!t [文字]` - 自動檢測並翻譯
- `!to_english [文字]` / `!英文 [文字]` / `!en [文字]` - 強制翻譯成英文
- `!to_chinese [文字]` / `!中文 [文字]` / `!zh [文字]` - 強制翻譯成繁體中文
- `!help_translate` / `!翻譯幫助` - 顯示幫助訊息
- `!auto_toggle` / `!自動翻譯` - 查看自動翻譯設置

## 本地運行

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 創建 `.env` 檔案並添加你的 Discord Bot Token：
```
DISCORD_BOT_TOKEN=你的_Discord_Token
```

3. 運行機器人：
```bash
python main.py
```

## Railway 部署步驟

### 1. 推送到 GitHub

```bash
# 初始化 git
git init

# 添加所有檔案
git add .

# 提交
git commit -m "Initial commit"

# 連接到你的 GitHub repository
git remote add origin https://github.com/你的用戶名/discord-translator.git
git branch -M main
git push -u origin main
```

### 2. 在 Railway 部署

1. 前往 [railway.app](https://railway.app) 並登入
2. 點擊 "New Project"
3. 選擇 "Deploy from GitHub repo"
4. 選擇你的 `discord-translator` repository
5. Railway 會自動偵測為 Python 專案並開始部署

### 3. 設定環境變數

1. 在 Railway 專案中，點擊你的服務
2. 進入 "Variables" 標籤
3. 添加環境變數：
   - Key: `DISCORD_BOT_TOKEN`
   - Value: 你的 Discord Bot Token

### 4. 完成！

機器人會自動啟動並保持運行。

## 獲取 Discord Bot Token

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 創建新應用程式或選擇現有應用程式
3. 進入 "Bot" 頁面
4. 點擊 "Reset Token" 並複製 Token
5. 在 Bot 設置中啟用以下權限：
   - MESSAGE CONTENT INTENT（訊息內容意圖）
   - Send Messages（發送訊息）
   - Read Message History（讀取訊息歷史）

## 注意事項

- 確保 Discord Bot 有適當的權限
- Token 必須保密，不要上傳到 GitHub
- Railway 免費方案有使用限制，可升級至付費方案

## 技術棧

- Python 3.11
- discord.py
- googletrans
- python-dotenv