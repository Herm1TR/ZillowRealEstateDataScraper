# Zillow Real Estate Data Scraper

## 項目概述

這個Python應用程序可以從Zillow克隆網站抓取房地產數據，並自動將收集到的資訊提交到Google表單。該項目演示了使用`requests`、`BeautifulSoup`和`Selenium`進行網頁抓取和自動化表單提交的技術。

## 功能特點

- 從Zillow克隆網站抓取房產價格、地址和連結
- 使用面向對象方法實現爬蟲和表單提交邏輯
- 詳細的錯誤處理和日誌記錄
- 將抓取的數據保存為CSV文件
- 自動將數據提交到Google表單
- 可選下載表單回應

## 技術棧

- **Python 3.7+**
- **Requests**: 用於發送HTTP請求
- **BeautifulSoup4**: 用於HTML解析
- **Selenium**: 用於瀏覽器自動化和表單提交
- **Pandas**: 用於數據處理和CSV導出
- **Logging**: 用於詳細的日誌記錄

## 安裝指南

1. 克隆代碼庫
   ```bash
   git clone https://github.com/yourusername/zillow-scraper.git
   cd zillow-scraper
   ```

2. 創建並激活虛擬環境
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. 安裝依賴
   ```bash
   pip install -r requirements.txt
   ```

4. 安裝Chrome瀏覽器和ChromeDriver
   
   確保安裝了Chrome瀏覽器，並下載與Chrome版本匹配的[ChromeDriver](https://sites.google.com/chromium.org/driver/)。

## 使用方法

### 基本用法

運行主腳本開始抓取數據和提交表單：

```bash
python zillow_scraper.py
```

### 配置

要更改目標URL或表單URL，請在`zillow_scraper.py`文件中修改以下常量：

```python
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_URL = "https://forms.gle/z4JvQZx8jTBDzMpw8"
RESPONSES_URL = "https://docs.google.com/forms/d/1tSK6EafVovJYyUxPo4tGAGosrzZtcElg7V6d5-Z0Z0g/edit?pli=1#responses"
```

### 以無頭模式運行

如果您希望在沒有可見瀏覽器窗口的情況下運行程序，可以修改`GoogleFormSubmitter`類的初始化：

```python
submitter = GoogleFormSubmitter(GOOGLE_FORM_URL, headless=True)
```

## 代碼結構

### 主要類

1. **PropertyScraper**: 負責從網站抓取和解析房產數據
   - `fetch_page()`: 獲取目標網頁的HTML內容
   - `parse_properties()`: 從HTML中解析房產數據
   - `save_to_csv()`: 將抓取的數據保存為CSV
   - `scrape()`: 執行完整的抓取過程

2. **GoogleFormSubmitter**: 負責將數據提交到Google表單
   - `setup_driver()`: 設置Selenium WebDriver
   - `submit_property()`: 提交單個房產數據
   - `submit_all_properties()`: 提交所有房產數據
   - 實現了上下文管理器接口（`__enter__`和`__exit__`）

### 輔助功能

- `download_responses()`: 從Google表單下載回應數據
- `main()`: 協調整個程序的執行流程

## 錯誤處理

本程序實現了全面的錯誤處理機制：

1. **網絡請求錯誤**：處理連接超時、404和5XX等HTTP錯誤
2. **解析錯誤**：當HTML結構變化時優雅地處理
3. **Selenium錯誤**：處理元素未找到、等待超時等問題
4. **重試機制**：表單提交失敗時自動重試
5. **詳細日誌**：記錄執行過程中的所有關鍵事件

## 日誌記錄

所有操作都記錄在`zillow_scraper.log`文件中，同時顯示在控制台。日誌包括：

- 信息級別：常規操作和進度報告
- 警告級別：非致命問題和潛在問題
- 錯誤級別：需要注意的操作失敗

## 改進計劃

1. 添加命令行參數以自定義爬蟲行為
2. 實現代理IP輪換以避免被阻止
3. 添加更多數據驗證和清理步驟
4. 創建Web界面以便更容易使用
5. 添加單元測試和集成測試
6. 實現更強大的反反爬蟲措施

## 依賴清單

```
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
pandas==2.1.1
```

## 許可

MIT許可證

## 作者

Your Name
