#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId","743cc4ff-f921-478c-8199-9420df9f67d5")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword","VQf8Q~EskGI36FzPfAGXq5-GAHtBigZUSgrllcKZ")
    
