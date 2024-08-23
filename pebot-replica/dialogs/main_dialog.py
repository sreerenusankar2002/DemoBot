# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from search_details import SearchDetails
from report_details import ReportDetails
from intelli_ops_recognizer import IntelliOpsRecognizer
from helpers.clu_helper import CLUHelper, Intent
from .search_dialog import SearchDialog
from .report_dialog import ReportDialog
from openai import AzureOpenAI as OpenAI



service_name = "your-search-service-name"
index_name = "cosmosdb-index"
api_key = "d3SNUFno6nIq2CfCIiO3HXakDFvpisNgrDMpQSBSBMAzSeBQdGs7"
OpenAI.api_key = "26b9b38908e14bd0b87bfb7aac6ad032"

search_client = SearchClient(endpoint=f"https://futurifysearch.search.windows.net",
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))
search_client1 = SearchClient(endpoint=f"https://futurifysearch.search.windows.net",
                             index_name="cosmosdb-report-index",
                             credential=AzureKeyCredential(api_key))


def search_documents1(query):
    results = search_client1.search(query)
    documents = []
    for result in results:
        documents.append(result)
    return documents


def search_documents(query):
    results = search_client.search(query)
    documents = []
    for result in results:
        documents.append(result)
    return documents


client=OpenAI(azure_endpoint="https://tcs-retail-futurify.openai.azure.com/", api_key="26b9b38908e14bd0b87bfb7aac6ad032",api_version="2023-05-15")

def generate_gpt_response(prompt):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {
            "role": "user",
            "content": prompt,
            }
            ],
            max_tokens=150
        )
        return response.choices[0].message.content

class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: IntelliOpsRecognizer, search_dialog: SearchDialog, report_dialog: ReportDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer
        self._search_dialog_id = search_dialog.id
        self._report_dialog_id = report_dialog.id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(search_dialog)
        self.add_dialog(report_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the SearchDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(
                self._search_dialog_id, SearchDetails()
            )

        # Call LUIS and gather any potential Search details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await CLUHelper.execute_clu_query(
            self._luis_recognizer, step_context.context
        )

        print(intent)
        print("renu")


        if intent == Intent.SEARCH_KNOWLEDGE_ARCTICLE.value and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.
            await MainDialog._show_warning_for_unsupported_cities(
                step_context.context, luis_result
            )

            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._search_dialog_id, luis_result)

        elif intent == Intent.GENERATE_REPORT.value and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.

            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._report_dialog_id, luis_result)

        if intent == Intent.GET_LIST_OF_INCIDENTS.value:
            get_weather_text = "TODO: get weather flow here"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_weather_message)

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self,step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result
            print("sree")
            print(result)

        # if isinstance(result, SearchDetails):
        #     # Now we have all the booking details call the booking service.
        #     # how to get the user_query from the search dialog
        #     user_query = "what is the solution_suggestion to : " + result.application + " " + result.errorcode
        #     print(user_query)
        #     search_results = search_documents(user_query)
        #     print(search_results)
        #     #search_summary = " ".join([doc['content'] for doc in search_results])
        #     gpt_prompt = f"Based on the following information, respond to the query: {user_query}\n\n{search_results}"


        if isinstance(result, ReportDetails):
            # Now we have all the booking details call the booking service.
            # how to get the user_query from the search dialog
            user_query = f"{result.reporttype} report for {result.timeperiod} in {result.reportformat} format"
            report_results = search_documents1(user_query)
            print(report_results)
            #search_summary = " ".join([doc['content'] for doc in search_results])
            gpt_prompt = f"Based on the following information, respond to the query: {user_query}\n\n{report_results}"
        # Step 3: Get GPT-generated response
            gpt_response = generate_gpt_response(gpt_prompt)
            print(gpt_response)
            if gpt_response:
                response_message = "Here are the search results:\n"
            #for result1 in search_results:
                #response_message += f"{result1['title']}: {result1['description']}\n"
                response_message = gpt_response
            else:
                response_message = "No results found."
            # If the call to the booking service was successful tell the user.
            # time_property = Timex(result.travel_date)
            # travel_date_msg = time_property.to_natural_language(datetime.now())
            msg_txt = response_message
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)

        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)

    