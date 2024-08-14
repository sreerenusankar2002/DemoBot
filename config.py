#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "1d390e34-054a-4477-a3bf-d521e7e31dc1")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Uat8Q~fF4yLTReTI6OBhD80kVWh13_a1uspumaV4")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "636bebcf-5a4b-41fe-9cbe-9633391bfeb4")
