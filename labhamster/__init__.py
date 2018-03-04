## Copyright 2016 - 2018 Raik Gruenberg

## This file is part of the LabHamster project (https://github.com/graik/labhamster). 
## LabHamster is released under the MIT open source license, which you can find
## along with this project (LICENSE) or at <https://opensource.org/licenses/MIT>.
from __future__ import unicode_literals

VERSION = (1,4,2)

__version__ = '.'.join([ str(i) for i in VERSION])

## https://docs.djangoproject.com/en/1.9/ref/applications/#configuring-applications
default_app_config = 'labhamster.apps.LabhamsterConfig'
