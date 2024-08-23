# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from typing import Dict, Tuple
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
from botbuilder.core import IntentScore, TopIntent, TurnContext
from search_details import SearchDetails
from report_details import ReportDetails

class Intent(Enum):
    SEARCH_KNOWLEDGE_ARCTICLE = "SearchSolution"
    GENERATE_REPORT = "GenerateReport"
    GET_LIST_OF_INCIDENTS = "GetListIncidents"
    GET_LOGS= "GetLogs"
    NONE_INTENT = "NoneIntent"

def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents.items():
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)

class CLUHelper:
    def __init__(self, endpoint: str, api_key: str, project_name: str, deployment_name: str):
        self._client = ConversationAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        self._project_name = project_name
        self._deployment_name = deployment_name

    async def execute_clu_query(
        self, turn_context: TurnContext
    ) -> Tuple[Intent, object]:
        """
        Returns an object with preformatted CLU results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            # Analyze the text using CLU
            analysis = self._client.analyze_conversation (
                task = { 
                    "analysisInput": {
                    "conversationItem": 
                    {  "id": "1",
                        "participantId": "user1",
                        "text": turn_context.activity.text,
                        "modality": "text", 
                        "language": "en"  
                    } 
                 }, 
                "kind": "Conversation", 
                "parameters": 
                { "projectName": self._project_name, 
                 "deploymentName": self._deployment_name } },
               content_type="application/json"
            )

            # Determine the top intent
            result = analysis['result']
            print(result)
           # if analysis['result'].prediction.intents:
           # if analysis['result']['prediction']['intents']:
            #    sorted_intents = sorted(
             #       analysis['result']['prediction']['intents'].items(),
              #      key=lambda item: item[1].confidenceScore,
               #     reverse=True
                #)
                #intent = sorted_intents[0][0]
            intent = analysis['result']['prediction']['topIntent']
            print(intent)


            if intent == Intent.SEARCH_KNOWLEDGE_ARCTICLE.value:
                result = SearchDetails()

            elif intent == Intent.GENERATE_REPORT.value:
                result = ReportDetails()

                # Extract entities
                entities = analysis.result.prediction.entities
                to_entities = entities.get("To", [])
                if to_entities:
                    result.destination = to_entities[0]['text'].capitalize()
                from_entities = entities.get("From", [])
                if from_entities:
                    result.origin = from_entities[0]['text'].capitalize()
                date_entities = entities.get("datetime", [])
                if date_entities:
                    timex = date_entities[0]['timex']
                    if timex:
                        result.travel_date = timex[0].split("T")[0]
                else:
                    result.travel_date = None

        except Exception as exception:
            print(exception)

        return intent, result
