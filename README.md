# YouTube 播放清單下載器

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

一個簡單但功能強大的 YouTube 播放清單下載工具，可以將播放清單中的影片轉換為 MP3 格式。


## 功能特點

- 圖形化使用者介面
- 支援大量歌曲下載（5000+ 首）
- 多線程並行下載（最多 10 個同時下載）
- 使用 aria2c 加速下載
- 高品質 MP3 輸出（192kbps）
- 即時下載進度和速度顯示
- 支援選擇下載目錄
- 錯誤自動處理和重試機制

## 快速開始

### 下載和安裝

#### 方法一：直接使用執行檔（推薦）

1. 從 [Releases](../../releases) 頁面下載最新的 `YouTube播放清單下載器.exe`
2. 下載並安裝 [FFmpeg](https://ffmpeg.org/download.html)
3. 下載並安裝 [aria2](https://github.com/aria2/aria2/releases)
4. 雙擊執行 `YouTube播放清單下載器.exe`

#### 方法二：從原始碼運行

### 安裝

1. 克隆專案：
```bash
git clone https://github.com/roy4222/youtube-playlist-downloader.git
cd youtube-playlist-downloader
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

### 必要工具安裝

#### FFmpeg 安裝：
- Windows：
  1. 下載 [FFmpeg](https://ffmpeg.org/download.html)
  2. 解壓並添加到系統環境變數

- Linux：
```bash
sudo apt-get install ffmpeg
```

- macOS：
```bash
brew install ffmpeg
```

#### aria2 安裝：
- Windows：
  1. 下載 [aria2](https://github.com/aria2/aria2/releases)
  2. 解壓並添加到系統環境變數

- Linux：
```bash
sudo apt-get install aria2
```

- macOS：
```bash
brew install aria2
```

### 使用方法

1. 運行程式：
```bash
python youtube_playlist_downloader.py
```

2. 在程式界面中：
   - 輸入 YouTube 播放清單 URL
   - 選擇下載目錄
   - 調整同時下載數量（建議：3-7）
   - 點擊「開始下載」

## 進階設置

### 下載設置建議

| 網路狀況 | 建議同時下載數 |
|---------|--------------|
| 極佳     | 7-10        |
| 良好     | 5-7         |
| 一般     | 3-5         |
| 不穩定   | 1-3         |

## 貢獻指南

1. Fork 本專案
2. 創建新分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request

## 常見問題

詳見 [Wiki](../../wiki) 頁面

## 授權協議

本專案使用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件

## 致謝

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [aria2](https://github.com/aria2/aria2)
- [FFmpeg](https://ffmpeg.org)

## 聯繫方式

- 問題回報：[Issues](../../issues)
- 討論：[Discussions](../../discussions)

---
⭐ 如果這個專案對你有幫助，歡迎給個星星！

## 系統需求

- Python 3.6 或更高版本
- FFmpeg（用於音訊轉換）
- aria2c（用於下載加速）

## 更新歷史

### 版本 1.0.0 (2025-01-13)
- 初始版本發布
- 支援多線程下載
- 圖形化介面
- 高品質 MP3 輸出

## 技術細節

- 使用 yt-dlp 作為下載核心
- FFmpeg 用於音訊轉換
- aria2c 用於多線程下載加速
- tkinter 和 ttk 用於圖形介面
- 使用 ThreadPoolExecutor 進行並行下載
