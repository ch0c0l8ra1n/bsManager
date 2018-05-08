import BsManager
from distutils.core import setup

setup(
  name = 'BsManager',
  packages = ['BsManager'],
  version = BsManager.__version__,
  description = 'Native python3 api for bombsquad',
  author = 'Rajat Parajuli',
  author_email = 'rjpj@parajuli.me',
  url = 'https://github.com/rjpj2016/bsManager',
  download_url = 'https://github.com/rjpj2016/bsManager/archive/' + BsManager.__version__ + '.tar.gz',
  keywords = ['api', 'python3', 'bombsquad'],
  classifiers = [],
)
