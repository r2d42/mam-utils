#!/usr/bin/env python3
import os
import requests

login_url = "https://www.myanonamouse.net/login.php"

login_data = {
        'email': os.environ.get("MAM_USERNAME"),
        'password': os.environ.get("MAM_PASSWORD")
}

