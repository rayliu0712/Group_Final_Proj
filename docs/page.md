# Page 介面

## 什麼是 Page ?

Page 是封裝 Thorpy 更新邏輯和事件的抽象基類，讓開發者不必手動管理畫面更新和監聽事件

一個 Page 代表一個**介面**。當**呼叫(而非創建)** 一個 Page 實例時，一個新的 loop 開始，畫面開始渲染，之前的 loops 則凍結，直到該 loop 結束

## Page 定義

```py
class Page(ABC):
    def __init__(self) -> None:
        """
        Page is lazy, call its instance to show
        """
        self._kandler = _KeyEventHandler(False)

    def __call__(self) -> None:
        self._kandler.clear()
        es: list[Element] = self._build()

        _fix_new_loop_cursor()
        match len(es):
            case 0:
                pass
            case 1:
                es[0].get_updater().launch(self._kandler)
            case _:
                Group(es, None).get_updater().launch(self._kandler)

    @abstractmethod
    def _build(self) -> list:
        pass
```

## 範例介面

1. 在 `src/ui/` 目錄底下新增一個 example.py 檔案

2. 在該檔案中，貼上以下內容

    ```py
    from .core import *

    class Example(Page):

        def _build(self):
            title = OutlinedText('This is an example page', 72)
            Screen.center(title)
            
            close_btn = SimpleImageButton('close_72dp.png', exit_app)
            Screen.topright(close_btn)

            return [title, close_btn]
    ```

3. 在其他地方調用

    調用範例一

    ```py
    from .core import *
    from .example import Example

    class Home(Page):

        def _build(self):
            title = OutlinedText('Home', 72)
            button = SimpleButton('example', Example())  # 當按下按鈕，啟動 Example Page

            group = Group([title, button])
            Screen.center(group)
            return [group]
    ```

    調用範例二

    ```py
    from .core import *
    from .example import Example

    class Home(Page):

        def _build(self):
            Example()()  # 直接啟動 Example Page
            # 下面的程式碼會凍結直到 Example Page 裡的關閉按鈕被按下
            # 結果 : 先顯示 Example Page，等到他關閉，才顯示 Home Page

            title = OutlinedText('Home', 72)
            Screen.center(title)
            return [title]
    ```

- `Example()` 和 `Example()()` 的差別 ?

    `Example()` 被視為一個函數，不會馬上啟動頁面，適合用在**事件綁定**
    
    `Example()()` 代表呼叫 `Example()` 函數，會馬上啟動頁面

    詳見 [Page 定義](#page-定義)

### 注意

- 所有負責介面的類別都必須 **繼承** `Page` 且 **覆寫** `_build()` 方法

- `_build()` 方法必須返回裝著元件的 `list`

- `_build()` 方法應該返回除了 popup (下個章節介紹) 之外所有的 elements

# Key Event Handler 鍵盤事件處理器

## 什麼是鍵盤事件處理器 ?

鍵盤事件處理器負責綁定(或稱註冊)和調用按鍵事件，在 `Page` 和 `Popup` 裡都有鍵盤事件處理器的實例

在 `Page` 裡叫做 `_kandler`，為 Protected 成員變數

在 `Popup` 裡叫做 `kandler`，為 Public 成員變數

`kandler` 為 <u>K</u>ey Event H<u>andler</u> 實例的常用縮寫

## 綁定定義

```py
class _KeyEventHandler:
    def __iadd__(self, args: tuple[Button | Action, list[int], list[int]]) -> Self:
        '''
        args[0] : button or action
        args[1] : mod keys, list[int] (can be empty)
        args[2] : keys, list[int] (cannot be empty)
        '''
        ...
```

## 綁定範例

```py
from pygame.constants import *  # Pygame 的 key constant

kandler += exit_app, [KMOD_ALT], [K_q]  # 綁定關閉遊戲到 alt + q 鍵

kandler += lambda: print('echo'), [], [K_e]  # 功能鍵(第二個)可以為空，但是普通鍵不行

kandler += play_btn, [], [K_RETURN]  # 綁定按鈕到 return 鍵 (非數字區的 enter 鍵)

def killer_move():  # 必殺技
    ...

kandler += killer_move, [KMOD_SHIFT, KMOD_CTRL, KMOD_ALT], [K_a, K_b, K_c]
# 功能鍵和普通鍵都支援同時多個
# 必須同時按下 shift + ctrl + alt + a + b + c 才能啟動必殺技
```

## 在 Page 中的綁定範例

```py
from .core import *  # 不用導入 pygame.constants，因為 core.py 已經導入

class Example(Page):

    def _build(self):
        close_btn = SimpleImageButton('close_72dp.png', exit_app)
        self._kandler += close_btn, [], [K_q]
        Screen.center(close_btn)

        return [close_btn]
```

## 看完了嗎 ?

前往 [Popup 彈窗](popup.md)
