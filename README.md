# 前言
做了一個簡單的小遊戲，~~應該還算好玩~~

# 構想
藉由一些裝飾或畫面等，剛好line bot可傳送照片，訊息提示，或按鈕選擇，所以便開始發想並實現。

# 使用說明
輸入任意開始初始狀態，之後就可以根據現在bot傳送的畫面及訊息等，按下想要執行的動作按鈕或根據要求輸入，最後通過遊戲
### 操作分為下列幾種
1.bot傳送的畫面及訊息有按鈕 -> 可以直接按下想要執行的按鈕
2.訊息中有提示可以輸入一些字母 -> 可以輸入字母
3.在任何狀態輸入"fsm" -> 得到fsm圖，狀態不改變
4.隨意輸入 -> 通常為沒有效果，狀態不改變

# 架構圖
## 用來解釋的圖
![](https://i.imgur.com/seesQhx.png)
上圖註：
雙紅線代表具備2種方向（go,return）
單藍線代表只具備箭頭的方向

左上角的未收錄代表有些線畫在這裡會使畫面混亂
1. 在end或start狀態時任意輸入，會 -> start
2. 輸入"fsm" -> 得到fsm圖，狀態不改變
3. 除\*_ lock、end或start狀態時任意輸入 -> 得到無效訊息，狀態不改變

## State說明
f/l/r/b四個各自分為2種狀態(檢查：用來做查看各面的物品/非檢查：用來轉向)

\*_ lock：鎖盒
1. 回答正確密碼解開 -> \*_ ans
2. 回答錯誤密碼 -> \*_ lock

其他state代表可能含有提示 ~~（不一定有）~~

## fsm_py內的function
into_\*()：從其他state進入該\state時執行
error()：\*_ lock回答錯誤密碼時執行
states_not_ch()：非可執行訊息出現時執行
fsm()：傳送fsm圖


# FSM圖片架構
![](https://i.imgur.com/CLBa2Qd.png)


# 使用示範
## 看向四面範例
![](https://i.imgur.com/4QTEX79.png)
## 檢查四面範例
![](https://i.imgur.com/bdbBPSZ.png)
## 檢查單一物件範例並返回
![](https://i.imgur.com/8mgI5Qw.png)
## 返回
![](https://i.imgur.com/VsZlBTK.png)
## 檢查鎖盒範例（正確）
（為了保留趣味，為了在DEMO時表現正確，程式中所有解謎都有使用"DEMO"作為完全正確字）
（同樣為了保留趣味，下方截圖只截取一部份）
![](https://i.imgur.com/dDuYvjv.png)
## 檢查鎖盒範例（錯誤）
![](https://i.imgur.com/H8eC7mF.png)
## 檢查最終鎖盒範例（正確）
（同樣為了保留趣味，為了在DEMO時表現正確，程式中所有解謎都有使用"DEMO"作為完全正確字）
![](https://i.imgur.com/LZa1S2S.png)
## 回到一開始範例
![](https://i.imgur.com/PtjIcP1.png)
## 一開始隨意輸入範例
![](https://i.imgur.com/o62OhXk.png)
## 其他狀態時隨意輸入範例
![](https://i.imgur.com/s9QAfTQ.png)

