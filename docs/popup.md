# Popup 彈窗

## Popup 定義

```py
class Popup:
    def __init__(self):
        """
        WARNING : don't construt popup by construtor. Instead, use class method
        Popup is lazy, call its instance to show
        """
        self.kandler = _KeyEventHandler(True)

    @classmethod
    def Alone(cls, element: Element) -> Self:
        ...

    @classmethod
    def LockAndLaunch(cls, be_locked_elements: list, be_launched_element: Element) -> Self:
        ...

    @classmethod
    def Merge(cls, element: Element, click_outside_cancel: bool) -> Self:  # 極少用
        ...
```

## 範例介面 & 鍵盤綁定範例

見 [home.py](../src/ui/home.py) 的 `Home.__popup_settings()`

## 看完了嗎 ?

前往 [Misc 其他](misc.md)