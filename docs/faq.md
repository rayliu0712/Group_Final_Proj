# FAQ

## 什麼是 Pygame ?

Pygame 是 Python 的一個模組，專為遊戲開發設計，提供繪圖、聲音處理、事件處理等功能，讓開發者能輕鬆創建 2D 遊戲

## 什麼是 Thorpy2 ?

Thorpy2 是基於 Pygame 的 GUI 庫，為 Pygame 提供擴展，讓開發者能夠輕鬆創建遊戲界面元素，如按鈕、菜單、對話框等；以及封裝事件和更新迴圈，讓開發者不用手動處理

## 為什麼不用其他的 Pygame 擴展庫，像是 Pygame GUI ?

因為 Thorpy2 是我目前找到 API 最簡潔，最適合快速開發的擴展庫。不信你就去比較兩者的官方範例就知道了

## src/ui/core.py 的作用 ?

src/ui/core.py (簡稱 core.py) 提供了基於 Thorpy2 的 UI 元件封裝，包含簡化按鈕、圖像按鈕、視窗、彈出框、頁面管理和鍵盤事件，為開發提供了通用性和統一性；以及**修補了 Thorpy2 的 Bug**

## 我該用哪個 ?

以 **core.py** 和 **Thorpy2** 為主。開發過程中，**你幾乎不會碰到有關 Pygame 的東西**


## 看完了嗎 ?

前往 **get_started.md**
