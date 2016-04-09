## Copyright 2012 Raik Gruenberg

## This file is part of the labhamster project (http://labhamster.sf.net)
## Labhamster is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.

## Labhamster is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.

## You should have received a copy of the GNU Affero General Public
## License along with labhamster. If not, see <http://www.gnu.org/licenses/>.
VERSION = (1,1,0)

__version__ = '.'.join([ str(i) for i in VERSION])

## https://docs.djangoproject.com/en/1.9/ref/applications/#configuring-applications
default_app_config = 'labhamster.apps.LabhamsterConfig'
