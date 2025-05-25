# Element 元件

如果你還不知道有哪些常用的 Thorpy 元件，先去看 <https://thorpy.org/doc/elements.html>

以下函數 ( mk開頭 ) 是為了簡化元件設定而創造出來的 helper function

```py
def mkButton(text: str, onclick: Optional[Action] = None) -> Button:
    btn = Button(text)
    btn.at_unclick = onclick
    return btn


def mkImageButton(filename: str, onclick: Optional[Action] = None) -> ImageButton:
    imgbtn = ImageButton("", pygame.image.load(f"assets/image/{filename}"))
    imgbtn.at_unclick = onclick
    return imgbtn


def mkBox(children: list, mode: Literal["v", "h", "grid", None] = "v") -> Box:
    box = Box(children, False)
    if mode:
        box.sort_children(mode)
    return box


def mkTitleBox(title: str, children: list, mode: Literal["v", "h", "grid", None] = "v") -> Box:
    titlebox = TitleBox(title, children, False)
    if mode:
        titlebox.sort_children(mode)
    titlebox.set_opacity_bck_color(191)  # 256 * 3/4 - 1
    return titlebox
```

## Screen 螢幕

### 定義

```py
class Screen:
    # Singleton
    def __new__(cls) -> Surface:
        return thorpy.parameters.screen

    @staticmethod
    def width() -> int:
        return Screen().get_width()

    @staticmethod
    def height() -> int:
        return Screen().get_height()

    @staticmethod
    def center(element: Element) -> None:
        element.center_on(Screen())

    @staticmethod
    def topleft(element: Element) -> None:
        element.set_topleft(0, 0)

    @staticmethod
    def topright(element: Element) -> None:
        element.set_topright(Screen.width(), 0)

    @staticmethod
    def bottomleft(element: Element) -> None:
        element.set_bottomleft(0, Screen.height())

    @staticmethod
    def bottomright(element: Element) -> None:
        element.set_bottomright(Screen.width(), Screen.height())
```

### 範例

```py
screen = Screen()  # 取得螢幕，通常情況下不會有需要取得螢幕的需求

screen_width = Screen.width()  # 取得螢幕的寬
screen_height = Screen.height()  # 取得螢幕的長

Screen.center(element)  # 置中
Screen.topleft(element)  # 置於左上角
Screen.topright(element)  # 置於右上角
Screen.bottomleft(element)  # 置於左下角
Screen.bottomright(element)  # 置於右下角
```

## 看完了嗎 ?

前往 [Page 頁面](page.md)