import cv2
import numpy as np
from PIL import ImageGrab, Image

def advanced_part_identifier():
    print("正在獲取圖片並進行零件辨識...")
    
    # 1. 獲取圖片
    img_pil = ImageGrab.grabclipboard()
    if not isinstance(img_pil, Image.Image):
        print("錯誤：請先複製圖片！")
        return
    
    # 轉換格式
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 強化預處理 (針對反光金屬零件)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    # 使用大津二值化 (Otsu's Binarization) 自動尋找最佳切割閾值
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 形態學優化：去除細小雜訊
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # 3. 尋找輪廓並進行邏輯辨識
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 800: continue # 過濾太小的雜訊

        # 計算周長與凸包 (Convex Hull)
        perimeter = cv2.arcLength(cnt, True)
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        
        # --- 核心辨識邏輯 ---
        # A. 圓形度 (判斷是不是圓的)
        circularity = (4 * np.pi * area) / (perimeter * perimeter) if perimeter > 0 else 0
        # B. 實心度 (判斷外型是否完整，用來區分螺絲頭與複雜零件)
        solidity = float(area) / hull_area if hull_area > 0 else 0

        # 定義零件類別
        label = "Unknown Part"
        color = (255, 255, 0) 

        if circularity > 0.85:
            label = "Washer (Gasket)" # 墊片通常非常圓
            color = (0, 255, 0) # 綠色
        elif 0.7 <= circularity <= 0.85:
            label = "Hex Nut / Bolt" # 六角螺帽圓形度稍低
            color = (255, 0, 0) # 藍色
        elif solidity < 0.6:
            label = "Special Component" # 實心度低可能是異形零件
            color = (0, 165, 255) # 橘色

        # 4. 繪製精美標籤
        x, y, w, h = cv2.boundingRect(cnt)
        # 畫框
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        # 畫背景標籤底色
        cv2.rectangle(img, (x, y - 30), (x + 180, y), color, -1)
        # 寫上零件名稱
        cv2.putText(img, label, (x + 5, y - 8), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Mechanical Part AI Identifier', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    advanced_part_identifier()