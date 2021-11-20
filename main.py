from PyQt5.QtWidgets import *
import os
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Empty window")
workdir = ''

def choose():
    global workdir
    workdir = QFileDialog.getExistingDirectory()





def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result





def showfiles():
    extensions = ['.jpg','.png','.bmp','.svg','.eps','.jpeg','.gif','.txt']
    choose()
    filesname = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for filename in filesname:
        list_files.addItem(filename)
    














btn_folder = QPushButton('folder')
btn_left = QPushButton('left')
btn_right = QPushButton('right')
btn_mirror = QPushButton('mirror')
btn_sharp = QPushButton('sharp')
btn_bw = QPushButton('bw')

image1 = QLabel('image')


list_files = QListWidget()


h1 = QHBoxLayout()
h2 = QHBoxLayout()
h1.addWidget(btn_left)
h1.addWidget(btn_right)
h1.addWidget(btn_mirror)
h1.addWidget(btn_sharp)
h1.addWidget(btn_bw)

v1 = QVBoxLayout()  
v2 = QVBoxLayout()
v1.addWidget(btn_folder)
v1.addWidget(list_files)
v2.addWidget(image1)
v2.addLayout(h1)
h2.addLayout(v1)
h2.addLayout(v2)


btn_folder.clicked.connect(showfiles)

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.original = None
        self.changed = list()
        self.dir = None
        self.save_dir = "modified/"

    def loadImage(self,dir,filename):
        self.dir = dir 
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.original = Image.open(image_path)
    
    def showImage(self, path):
        image1.hide()
        pixmapimage = QPixmap(path)
        w, h = image1.width(), image1.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        image1.setPixmap(pixmapimage)
        image1.show() 
    
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.original.save(image_path)



        
    def do_bw(self):
        self.original = self.original.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)



    def do_left(self):
        self.original = self.original.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_right(self):
        self.original = self.original.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_mirror(self):
        self.original = self.original.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.original = self.original.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


def showchosenimage():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)


workimage = ImageProcessor()



list_files.currentRowChanged.connect(showchosenimage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_sharp.clicked.connect(workimage.do_sharp)













main_win.setLayout(h2)












main_win.show()
app.exec_()

