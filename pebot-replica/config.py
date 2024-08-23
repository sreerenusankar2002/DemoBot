#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "6c4b0523-18ca-4336-af3a-d600c3fcf634")
    #LUIS_APP_ID = os.environ.get("LuisAppId", "ed99d1f4-cf27-4169-bd3e-ace7c62a4f3d")
    #LUIS_API_KEY = os.environ.get("LuisAPIKey", "9f93fb40c1ca4b1baf6723e26311cd01")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    #LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "futurifylang.cognitiveservices.azure.com/")
    CLU_ENDPOINT= os.environ.get("CluEndpoint", "https://futurifylang.cognitiveservices.azure.com/")
    CLU_API_KEY= os.environ.get("CluKey", "9f93fb40c1ca4b1baf6723e26311cd01")
    PROJECT_NAME= os.environ.get("ProjectName", "ReportGenerationBot")
    DEPLOYMENT_NAME= os.environ.get("DeploymentName", "ReportGeneration")


