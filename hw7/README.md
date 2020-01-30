# homework 7

## 自我檢核表

- [ ] 願意自己查資料
- [ ] 願意花很多時間debug
- [ ] 更了解 HTML 網頁設計
- [ ] 懂得操作 JavaScript 的外部函式庫
- [ ] 發現並解決 Callback function 「與世隔絕」的問題 (可能用到同步/異步觀念，略懂即可)
- [ ] 了解如何動態生成 html 物件 (利用 amcharts 官網 candlestick [範例程式碼](https://www.amcharts.com/docs/v4/reference/candlestick/))

## 內容

我們要修改 hw1 的程式碼，來做一個繪製K棒的頁面。index.html 在開啟時會向 startserver.py 請求價格資料，並繪製K棒圖形。

繪圖套件我們使用 [amchart 4](https://www.amcharts.com/)，資料我們使用 [2018/11/01~2018/11/30 EURUSD 1H 的匯率價格](https://github.com/RainBoltz/webing-from-scratch/blob/master/hw7/EURUSD_1_Hour_01.11.2018-30.11.2018.csv)。

顯示方式不限，請以最佳化使用者體驗為目標來呈現。