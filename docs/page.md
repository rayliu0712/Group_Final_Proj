# Page 介面

如何建立一個空白介面 ?

1. 在 `src/ui/` 目錄底下新增一個 .py 檔案

2. 在該檔案中，貼上以下內容

```py
from .core import *

class EmptyPage(Page):

    def _build(self) -> list[Element]:
        title = OutlinedText('This is an empty page', 72)
        Screen.center(title)
        return [title]
```

