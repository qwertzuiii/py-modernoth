import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QIcon

from tomllib import loads as tml
from json import loads as jsn

# Debug mode
is_Debug = True
#

# Loading config
cfg = open('config.toml', 'r').read()
cfg = tml(cfg)
#

# Loading theme list
theme_folder = 'bin/themes/'

theme_list = open(theme_folder + 'list.json', 'r').read()
theme_list = jsn(theme_list)
#

class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg['ui'], self)  # ui file load

        # Theme system
        self.theme_index = 0
        self.__theme_change()
        self.__theme_list_refresh()
        #
        
        self.ThemeBox.currentIndexChanged.connect(self.__theme_change_box)

    def __theme_list_refresh(self):
        themes = theme_list
        themes_len = len(themes)
        if is_Debug: print(themes_len)
        i = 0

        for theme in range(themes_len):
            self.ThemeBox.addItem(themes[i]['name'])
            i += 1

    def __theme_change_box(self, value):
        self.theme_index = value
        self.__theme_change()

    def __theme_change(self):
        # Loading theme stylesheet
        f   = theme_list[self.theme_index]['file']
        vf  = theme_list[self.theme_index]['varfile']
        n   = theme_list[self.theme_index]['name']
        opt = theme_list[self.theme_index]['opt']

        if opt == "":
            o = False
        else:
            o = True
        
        print('Loading Theme: ' + n + " [{}]".format(f))
        if o:
            print('OPT: {}'.format(opt))

        varsf = open(theme_folder + vf, 'r').read()
        varsf = jsn(varsf)

        style = open(theme_folder + f, 'r').read()

        if o:
            style_opt = open(theme_folder + opt, 'r').read()
        
        for var in varsf: # Replacing vars in variable file
            style = style.replace(var, varsf[var])

            if o:
                style_opt = style_opt.replace(var, varsf[var])

        if is_Debug:
            if o:
                open('STYLE.RESULT.--debug.css', 'w').write(style + "\n" + style_opt)
            else:
                open('STYLE.RESULT.--debug.css', 'w').write(style)

        if o:
            self.setStyleSheet(style + "\n" + style_opt)
        else:
            self.setStyleSheet(style)
        
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')