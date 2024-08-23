# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.ai.luis import LuisApplication, LuisRecognizer
from botbuilder.core import Recognizer, RecognizerResult, TurnContext
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential
from msrest.authentication import CognitiveServicesCredentials



from config import DefaultConfig


class CommandRunner(Recognizer):
    def __init__(self, configuration: DefaultConfig):
        self._recognizer = None

        clu_is_configured = (
            configuration.CLU_ENDPOINT
            and configuration.CLU_API_KEY
            and configuration.PROJECT_NAME
            and configuration.DEPLOYMENT_NAME
        )
        if clu_is_configured:
            # Set the recognizer options depending on which endpoint version you want to use e.g v2 or v3.
            # More details can be found in https://docs.microsoft.com/azure/cognitive-services/luis/luis-migration-api-v3
           # luis_application = LuisApplication(
            #    configuration.LUIS_APP_ID,
             #   configuration.LUIS_API_KEY,
              #  "https://" + configuration.LUIS_API_HOST_NAME,
            #)

            #self._recognizer = LuisRecognizer(luis_application)
            # write this code to use the new CLU
           self._client = ConversationAnalysisClient(endpoint=configuration.CLU_ENDPOINT, credential=AzureKeyCredential(configuration.CLU_API_KEY))
           self._project_name = configuration.PROJECT_NAME
           self._deployment_name = configuration.DEPLOYMENT_NAME
           self._recognizer = True

    @property
    def is_configured(self) -> bool:
        # Returns true if luis is configured in the config.py and initialized.
        return self._recognizer is not None

    async def recognize(self, turn_context: TurnContext) -> RecognizerResult:
        if not self.is_configured:
            return None
