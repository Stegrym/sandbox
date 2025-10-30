import cv2
import sys, os
import numpy as np


def make_error_window(win_name):
    """Вставляет заставку при ошибке камеры
     в окно приложения"""

    SIZE = 400

    try:
        # Путь к картинке зависит от режима (.exe/IDE)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # sys._MEIPASS внутри exe файла
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(base_path, "images", "gray.jpg")
        img = cv2.imread(image_path)

        # Если всё прошло успешно, запускаем заставку ошибки
        if img is not None:
            cv2.resizeWindow(win_name, SIZE, SIZE)
            cv2.imshow(win_name, img)
            cv2.waitKey()
            cv2.destroyAllWindows()

    except Exception:
        pass
    finally:
        cv2.destroyAllWindows()


def main():
    WINDOW_NAME = 'Webcam'
    CAM_WINDOW_SIZE = (640, 480)

    cap = cv2.VideoCapture(0)  # Данные с камеры (0)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_GUI_NORMAL)  # Создаём окно с параметрами без значков

    # Если камера не сработала, поставили заставку
    if not cap.isOpened():
        make_error_window(WINDOW_NAME)
        exit()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)  # отзеркалил изображение
            frame = cv2.resize(frame, CAM_WINDOW_SIZE)  # размеры

            try:
                # Проверка на закрытие окна приложения
                window_visible = cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE)
                if window_visible != 1:
                    break
            except cv2.error:
                break

            # Условие закрытия окна клавишами "Esc", без него не работает!
            cv2.imshow(WINDOW_NAME, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # 27 = Esc
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
