# https://stackoverflow.com/questions/44977227/how-to-configure-main-py-init-py-and-setup-py-for-a-basic-package


###############################################################################################

# for 'python mypackage' execution without pip install
import sys
import pathlib
package_dir = pathlib.Path(__file__).resolve().parent# get fullpath to current package
#print( str(package_dir) + '/../' )
sys.path.append( str(package_dir) + '/../' )# append path where package exists

###############################################################################################

from nodepad import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QSurfaceFormat


def main():

    app = QApplication(sys.argv)
    QApplication.setStyle( 'Fusion' )# Required for overriding QTabBartab::paintEvent.

    # super sampling settings for opengl mode
    fmt = QSurfaceFormat()
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    mainWidget = MainWidget()
    mainWidget.show()
        
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()