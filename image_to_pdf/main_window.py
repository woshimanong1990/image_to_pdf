# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import copy
import os
import logging
import json
import sys

from PIL import Image

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt


from image_to_pdf.UI_main import Ui_mainWindow
from image_to_pdf import variables

logger = logging.getLogger()


class CustomMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.selected_files = None
        self.save_file = None
        self.page_size = list(variables.DEFAULT_PAGE_SIZE)
        self.resize_page_size = list(variables.DEFAULT_RESIZE_PAGE_SIZE)
        self.image_site = list(variables.DEFAULT_IMAGE_SITE)
        self.need_save_config = False
        self.setting_file = None
        self.init_config()

    def init_config(self):
        try:
            if getattr(sys, 'frozen', False):
                bundle_dir = sys._MEIPASS
                cur_dir = os.path.join(bundle_dir, "config.json")
            else:
                cur_dir = os.path.dirname(os.path.abspath(__file__))
            self.setting_file = os.path.join(cur_dir, "config.json")
            if not os.path.exists(self.setting_file):
                return
            with open(self.setting_file, 'r') as f:
                config = json.load(f)
                self.resize_page_size = config.get("image_size", self.resize_page_size)
                self.need_save_config = config.get("need_save_config", False)
                self.ui.lineEdit.setText(str(self.resize_page_size[0]))
                self.ui.lineEdit_2.setText(str(self.resize_page_size[1]))
                self.ui.checkBox.setCheckState(self.need_save_config)

        except:
            logger.error("init_config", exc_info=True)

    def selectDirectory(self):
        files, _ = QFileDialog.getOpenFileNames(self, "请选择文件", filter="Image files (*.jpg *.gif *jpeg *png))")
        if not files:
            QMessageBox.critical(self, "错误", "没有选择文件")
            return
        # print(files)
        self.ui.selectFilesText.setText("\n".join(files))
        self.selected_files = files

    def selectSaveFileName(self):
        save_file, _ = QFileDialog.getSaveFileName(self, "请选择保存路径", filter="pdf (*pdf)")
        if not save_file:
            QMessageBox.critical(self, "错误", "没有选择文件")
            return
        self.ui.saveFileText.setText(save_file)
        self.save_file = save_file

    def get_resize(self, max_width, max_height, image_with, image_height):
        basewidth = max_width

        wpercent = (basewidth / float(image_with))
        hsize = int((float(image_height) * float(wpercent)))
        if hsize > max_height:
            hsize = max_height
        return basewidth, hsize

    def cover_to_pdf(self, pdf_path, images):
        images = copy.deepcopy(images)
        resize_page_size = tuple(self.resize_page_size)
        page_size = tuple(self.page_size)
        a4im = Image.new('RGB',
                         page_size,
                         (255, 255, 255))

        first_image = images.pop(0)
        img = Image.open(first_image)
        img = img.convert('RGB')
        image_resize = self.get_resize(resize_page_size[0], resize_page_size[1], img.size[0], img.size[1])
        img = img.resize(image_resize, Image.ANTIALIAS)
        image_site = int(self.page_size[0] - image_resize[0]) // 2, int(self.page_size[1] - image_resize[1]) // 2
        a4im.paste(img, image_site)
        other_images = []
        for i in images:
            a4im2 = Image.new('RGB',
                              page_size,
                              (255, 255, 255))
            img_2 = Image.open(i)
            img_2 = img_2.convert('RGB')
            image_resize = self.get_resize(resize_page_size[0], resize_page_size[1], img_2.size[0], img_2.size[1])
            img_2 = img_2.resize(image_resize, Image.ANTIALIAS)
            image_site = int(self.page_size[0] - image_resize[0]) // 2, int(self.page_size[1] - image_resize[1]) // 2
            # print("self.image_site", image_site)
            a4im2.paste(img_2, image_site)
            other_images.append(a4im2)

        a4im.save(pdf_path, save_all=True, append_images=other_images)

    def startCreate(self):
        try:
            if not self.selected_files:
                self.ui.selectFilesText.setFocusPolicy(Qt.StrongFocus)
                self.ui.selectFilesText.setFocus()
                QMessageBox.critical(self, "错误", "您还没有选择图片")
                return
            if not self.save_file:
                self.ui.saveFileText.setFocusPolicy(Qt.StrongFocus)
                self.ui.saveFileText.setFocus()
                QMessageBox.critical(self, "错误", "您还没有选择pdf保存路径")
                return
            self.cover_to_pdf(self.save_file, self.selected_files)
            os.system("start %s" % self.save_file)
        except:
            QMessageBox.critical(self, "错误", "生成pdf失败")
            logger.error("startCreate", exc_info=True)
        else:
            QMessageBox.information(self, "成功", "生成pdf成功")

    def closeDialog(self):
        self.close()

    def changeImageWidth(self):
        width_str = self.sender().text()
        try:
            new_value = int(width_str)
            if new_value < 1 or new_value >variables.DEFAULT_PAGE_SIZE[0]:
                QMessageBox.critical(self, "错误", "输入的值有误, 不符合有效值")
                return
            self.resize_page_size[0] = new_value
        except ValueError as e:
            QMessageBox.critical(self, "错误", "输入的值有误，需要是数字")
            return
        except:
            logger.error("changeImageWidth", exc_info=True)
            QMessageBox.critical(self, "错误", "未知的错误，请重试")
            return

    def changeImageHeight(self):
        height_str = self.sender().text()
        try:
            new_value = int(height_str)
            if new_value < 1 or new_value > variables.DEFAULT_PAGE_SIZE[1]:
                QMessageBox.critical(self, "错误", "输入的值有误, 不符合有效值")
                return
            self.resize_page_size[1] = new_value
            # print(self.resize_page_size, self.image_site)
        except ValueError as e:
            QMessageBox.critical(self, "错误", "输入的值有误，需要是数字")
            return
        except:
            logger.error("changeImageHeight", exc_info=True)
            QMessageBox.critical(self, "错误", "未知的错误，请重试")
            return

    def rememberConfig(self, isChecked):
        self.need_save_config = isChecked

    def closeEvent(self, event):
        if not self.need_save_config:
            event.accept()
            return
        if not self.setting_file:
            event.accept()
            return
        try:

            new_data = {
                "image_size": self.resize_page_size,
                "need_save_config": self.need_save_config
            }
            with open(self.setting_file, 'a+') as f:
                f.seek(0, 0)
                old_content = f.read()
                old_data = {}
                if old_content:
                    old_data = json.loads(old_content)
                    f.truncate(0)
                old_data.update(new_data)
                json.dump(old_data, f, indent=4, sort_keys=True)
        except PermissionError as e:
            self.showMessage("保存失败！ 权限不足，无法写入文件")
        except Exception as e:
            logger.error("closeEvent", exc_info=True)
        finally:
            event.accept()



