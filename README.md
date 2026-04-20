# 🛠 機械零件自動辨識系統 (Mechanical Part Identifier)

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)

這是一個專為**大學程式設計課程專題**開發的「機械零件自動辨識系統」。本系統結合了電腦視覺 (Computer Vision) 與幾何特徵分析技術，旨在自動辨識、測量並分類常見的工業零件（如墊片、螺栓、螺帽等）。

---

## 🌟 核心特色

- **零摩擦輸入**：支援從系統剪貼簿直接抓取圖片（Win+Shift+S 截圖後即可辨識），無需手動存檔與輸入路徑。
- **工業級預處理**：導入大津二值化 (Otsu's Thresholding) 與雙邊濾波 (Bilateral Filter)，有效應對金屬反光問題。
- **物理特徵驗證**：不依賴黑盒 AI，而是透過幾何算式（圓形度、實心度）進行精準分類。
- **視覺化數據輸出**：自動標註零件編號，並即時生成對齊的量測數據清單。

---

## 🔬 技術原理

本系統的辨識邏輯基於以下幾何物理特徵：

### 1. 圓形度 (Circularity)
用於判斷零件是否為標準圓形（如墊片或螺絲頭）：
$$C = \frac{4\pi A}{P^2}$$
*其中 $A$ 為面積，$P$ 為周長。當 $C$ 越接近 1，表示形狀越圓。*

### 2. 實心度 (Solidity)
用於區分實心零件與具有凹槽或孔洞的異形零件：
$$S = \frac{\text{Area}}{\text{Convex Hull Area}}$$

---

## 🛠 安裝指引

請確保您的電腦已安裝 Python 3.10+，並執行以下指令安裝必要函式庫：

```bash
pip install opencv-python numpy pillow pandas
