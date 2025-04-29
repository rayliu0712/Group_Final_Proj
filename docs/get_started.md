# Get Started 新手上路

以下介紹開發此遊戲必備的基本知識

## Action 動作

代表一個不接受參數且返回任意類型的函數，定義如下

```py
type Action = Callable[[], Any]
```

Action 是點擊事件和鍵盤事件中最常用到的類型 


## Pygame Surface

最常見的實例是 `screen`，儲存著窗口的長寬資訊；不過已經被 core.py 裡的 `Screen` 類封裝


## Thorpy2 Element

Thorpy2 中所有 GUI 元件最終的父類都是 `Element`

## Thorpy2 Button

Thorpy2 中所有**點擊後能觸發事件**的元件最終的父類都是 `Button`，透過重新指定 `at_unclick` 註冊點擊事件

```py
button = Button('Click Me')
button.at_unclick = lambda: print('clicked !')
```

### 注意 :

雖然 `at_unclick` 其實是 Element 的成員函數，但是能否觸發點擊事件需要看 Element 的成員變數 `state` **是否不等於 'unactive' 和 'locked'**

而 Element 的 state 為 **'unactive'**， Button 的則覆寫為 **'normal'**。這就是為什麼一個元件即使能註冊點擊事件也不一定能觸發的關鍵原因


## Event Loop 事件循環

在所有 GUI 庫中(像是 Pygame, Qt 等)，都有一個主循環，負責**更新畫面**和**監聽事件**，他會**堵塞主線程直到循環結束**

Pygame 典型範例如下 :

```py
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse clicked')
        elif event.type == pygame.KEYDOWN:
            print('key pressed')
    
    # 更新遊戲狀態
    
    # 繪製畫面
    screen.fill((0, 0, 0))
    # 繪製其他元素...
    pygame.display.flip()
    
    # 控制幀率
    clock.tick(60)
```

Tkinter 典型範例如下 :

```py
def on_click():
    # 處理點擊事件
    print("按鈕被點擊")

button = tk.Button(root, text="點擊我", command=on_click)
button.pack()

# 啟動事件循環
root.mainloop()  # 這行代碼啟動了 Tkinter 的內建事件循環
```

## Thorpy2 Loop

Thorpy2 內建了事件循環，讓開發者不用處理繁瑣的事件循環

Thorpy2 典型範例如下 :

```py
title = thorpy.Text("Hello World")
title.set_font_color((0,0,0))
title.center_on(screen)

def before_gui():
    screen.fill((250, 250, 250))
tp.call_before_gui(before_gui)

player = title.get_updater().launch()  # 啟動 Thorpy2 的內建事件循環
```

值得一提的是，Thorpy2 的 Loop 是可以疊加的，裝載著 loops 的容器為 stack

只有 stack 最上面的 loop 會被循環，其他 loops 則會因此凍結，直到最上面的 loop 循環結束，被 pop 出去，才換人循環


## 看完了嗎 ?

前往 [Element](element.md)