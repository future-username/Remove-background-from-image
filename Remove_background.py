from os import path, mkdir, listdir, environ

from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter

from tkinter import Tk, filedialog, Button, X, BOTH, Listbox, Frame, TOP, Scrollbar, LEFT, Y, END
from webbrowser import open_new


class Quality:
    @staticmethod
    def improve_img_quality(img: Image) -> Image:
        bbox = img.getbbox()
        img = img.crop(bbox)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        img = img.filter(ImageFilter.DETAIL)
        return img


class App:
    def __init__(self):
        environ['NUMPY_EXPERIMENTAL_ARRAY_FUNCTION'] = '0'
        environ['ORT_DISABLE_ENCLAVE'] = '1'

        if not path.isdir('images_without_bg'):
            mkdir('images_without_bg')

        self.__root = Tk()
        self.__root.geometry("300x300")
        self.__frame_top = Frame(self.__root)
        self.__frame_top.pack(side=TOP, fill=X)

        self.__frame_down = Frame(self.__root)
        self.__frame_down.pack(fill=BOTH, expand=1)
        self.__list_box = Listbox(self.__frame_down)
        self.__list_box.pack(side=LEFT, fill=BOTH, expand=1)

        remove_bg = RemoveBg(self.list_box)
        self.__folder_button = Button(self.__frame_top, text="Выбрать папку",
                                      command=lambda: remove_bg.remove_bg_images())
        self.__folder_button.pack(fill=X, expand=1)
        self.__image_button = Button(self.__frame_top, text="Выбрать изображение",
                                     command=lambda: remove_bg.remove_bg_image())
        self.__image_button.pack(fill=X, expand=1)

        self.__scroll = Scrollbar(self.__frame_down, command=self.__list_box.yview)
        self.__scroll.pack(side=LEFT, fill=Y)

    @property
    def list_box(self):
        return self.__list_box

    def draw(self):
        self.__root.mainloop()


class RemoveBg:
    def __init__(self, list_box: Listbox):
        self.__list_box = list_box

    def remove_bg_images(self) -> None:
        place = self.__get_target_path()
        for pict in listdir(place):
            if pict.endswith('.png') or pict.endswith('.jpg') or pict.endswith('.jpeg'):
                self.__list_box.insert(END, f'[+] Удаляю фон: "{pict}"...')
                output = remove(Image.open(path.join(place, pict)))
                output = Quality.improve_img_quality(output)
                output.save(path.join('images_without_bg', f'{pict.split(".")[0]}.png'))
            else:
                self.__list_box.insert(END, f'[!] В папке нет изображений')
                return
        self.__list_box.insert(END, '[+] Удаление завершено!')
        open_new(path.join('images_without_bg'))

    def __get_target_path(self) -> listdir:
        user_input = filedialog.askdirectory(title='Выберите папку с изображениями')
        if not user_input:
            self.__list_box.insert(END, '[!] Папка не выбрана')
            raise ValueError('Папка не выбрана')
        self.__list_box.insert(END, f"[-] Работаем с папкой {user_input}")
        return user_input

    def remove_bg_image(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            self.__list_box.insert(END, '[!] Изображение не выбрано')
            raise ValueError('Изображение не выбрано')
        if file_path.endswith(('.png', '.jpg', '.jpeg')):
            pict = file_path.split('/')[-1]
            self.__list_box.insert(END, f'[+] Удаляю фон: "{pict}"...')
            output = remove(Image.open(path.join(file_path)))
            output = Quality.improve_img_quality(output)

            output.save(path.join('images_without_bg', f'{pict.split(".")[0]}_enhanced.png'))
        self.__list_box.insert(END, '[+] Удаление завершено!')
        open_new(path.join('images_without_bg'))


if __name__ == '__main__':
    App().draw()
