# Earthdata Login
from netrc import netrc
from subprocess import Popen
from platform import system
from getpass import getpass
import os

# Direct access
import requests
import s3fs
import xarray as xr
import hvplot.xarray

# Harmony
from harmony import BBox, Client, Collection, Request, LinkType
from harmony.config import Environment
from pprint import pprint
import datetime as dt
