# Element 元件

元件分為**Thorpy 元件**和**簡單元件**

如果你還不知道有哪些常用的 Thorpy 元件，先去看 <https://thorpy.org/doc/elements.html>

簡單元件是為了簡化 Thorpy 元件 API 所創造出來的。如果 Thorpy 元件有對應的簡單元件，請使用簡單元件而非 Thorpy 元件

以下介紹簡單元件

## Simple Button 簡單按鈕

### 定義

```py
class SimpleButton(Button):
    def __init__(self, text: str, onclick: Optional[Action] = None):
        # onclick=None 代表不註冊或是推遲註冊點擊事件
        ...
```

### 範例

```py
button1 = SimpleButton('1', lambda: print('1 clicked !'))

button2 = SimpleButton('2')
button2.at_unclick = lambda: print('2 clicked !')
```

## Simple Image Button 簡單圖片按鈕


### 定義

```py
class SimpleImageButton(ImageButton):
    def __init__(self, filename: str, onclick: Optional[Action] = None):
        # 圖片須放在 assets/image/ 底下，他會從那裡找
        ...
```

### 範例

```py
close_btn = SimpleImageButton('close_72dp.png', exit_app)
```

## Simple Title Box 簡單標題盒

他與 Thorpy Title Box 其中重要的差別就是預設的不透明度改為 75%

### 定義

```py
class SimpleTitleBox(TitleBox):
    def __init__(self, title: str, children: list[Element], mode: Optional[str] = 'v'):
        # mode 可以是 'v', 'h', None
        # mode='v' 代表垂直排列
        # mode='h' 代表水平排列
        # mode=None 代表不排列
        ...
```

### 範例

```py
easy_button = SimpleButton('Easy', lambda: print('Easy'))
hard_button = SimpleButton('Hard', lambda: print('Hard'))
box = SimpleTitleBox('Choose Difficulty', [easy_button, hard_button], 'h')
```

## Screen 螢幕

### 定義

```py
class Screen():
    def __new__(cls) -> Surface:
        return thorpy.parameters.screen

    @staticmethod
    def center(element: Element) -> None:
        element.center_on(Screen())

    @staticmethod
    def width() -> int:
        return Screen().get_width()

    @staticmethod
    def height() -> int:
        return Screen().get_height()
```

### 範例

```py
screen = Screen()  # 取得螢幕，通常情況下不會有需要取得螢幕的需求

screen_width = Screen.width()  # 取得螢幕的寬
screen_height = Screen.height()  # 取得螢幕的長
```

## 元件對齊

### 定義

元件的 `左上角/右上角/左下角/右下角/中間` 對齊到 `螢幕的(x, y)`

螢幕的 x 從左到右，螢幕的 y 從上到下。螢幕左上角為 (0, 0)，螢幕右下角為 (螢幕寬, 螢幕高)

```py
element.set_topleft(0, 0) # 元件左上角對齊到 螢幕的(0, 0)

element.set_topright(Screen.width(), 0) # 元件右上角對齊到 螢幕的(螢幕寬, 0)

element.set_bottomleft(0, Screen.height())  # 元件左下角對齊到 螢幕的(0, 螢幕高)

element.set_bottomright(Screen.width(), Screen.height())  # 元件左下角對齊到 螢幕的(螢幕寬, 螢幕高)

Screen.center(element)  # 元件置中
```

## 看完了嗎 ?

前往 [頁面](page.md)