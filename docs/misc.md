# Misc 其他

## core.py 實用物件

```py
def lazy(func: Callable) -> Callable:  # 裝飾器
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        return lambda: func(*args, **kwargs)
    return wrapper


def quit_current_loop() -> None:
    thorpy.quit_current_loop()


def is_pygame_quit() -> bool:
    return any(e.type == pygame.QUIT for e in pygame.event.get())


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
```