####################################################
# OUR PROGRAM
####################################################

import views,models
from models import app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    app.debug=True
    app.run()
