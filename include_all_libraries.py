# typing
from typing import Callable, Dict, List, Any, Iterable, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from urllib.parse import urlparse
from lxml import html as html_lx
from bs4 import BeautifulSoup
from string import Template
from pprint import pprint
import itertools
import requests
import json
import time
import re
import os

# # Явно укажем, что экспортировать при "from common_imports import *"
# __all__ = [
#     "Callable", "Dict", "List", "Any", "Iterable", "Tuple",
#     "Counter", "defaultdict", "datetime", "timedelta", "SequenceMatcher",
#     "urlparse", "Template", "pprint", "itertools", "json", "time", "re", "os",
#     "requests", "html_lx", "BeautifulSoup",
# ]