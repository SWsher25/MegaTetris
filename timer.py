from pygame.time import get_ticks

class Timer:
    """
    Универсальный таймер для управления задержками и повторяющимися действиями.
    Может вызывать функцию по истечении времени, поддерживает повторение.
    """
    def __init__(self, duration, repeated = False, func = None):
        """
        duration: длительность таймера в мс
        repeated: если True — таймер будет автоматически перезапускаться
        func: функция, которую нужно вызвать по истечении таймера
        """
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.start_time = 0  # время последнего запуска
        self.active = False  # активен ли таймер

    def activate(self):
        """
        Активирует таймер, запоминая текущее время.
        """
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        """
        Отключает таймер и сбрасывает время запуска.
        """
        self.active = False
        self.start_time = 0

    def Update(self):
        """
        Проверяет, истёк ли таймер. Если да — вызывает функцию (если задана),
        сбрасывает таймер, и если repeated=True — запускает снова.
        """
        current_time = get_ticks()
        # Проверяем, что таймер активен и прошло достаточно времени
        if current_time - self.start_time >= self.duration and self.active:
            
            # call a function
            if self.func and self.start_time != 0:
                self.func()

            # reset timer
            self.deactivate()
            
            # repeat the timer
            if self.repeated:
                self.activate()