from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.integration.aiohttp import BotFrameworkHttpAdapter
from botbuilder.core import BotFrameworkAdapterSettings
from botbuilder.core.integration import aiohttp_channel_service_routes
#from botbuilder.core.integration import ApplicationInsightsTelemetryClient
from botbuilder.schema import Activity
import aiohttp.web

service_name = "your-search-service-name"
index_name = "your-index-name"
api_key = "your-api-key"

search_client = SearchClient(endpoint=f"https://{service_name}.search.windows.net",
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))


def search_documents(query):
    results = search_client.search(query)
    documents = []
    for result in results:
        documents.append(result)
    return documents


class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_query = turn_context.activity.text
        search_results = search_documents(user_query)

        if search_results:
            response_message = "Here are the search results:\n"
            for result in search_results:
                response_message += f"{result['title']}: {result['description']}\n"
        else:
            response_message = "No results found."

        await turn_context.send_activity(MessageFactory.text(response_message))


# Example adapter and bot setup
adapter_settings = BotFrameworkAdapterSettings("app-id", "app-password")
adapter = BotFrameworkHttpAdapter(adapter_settings)

# Routes for bot endpoints
app = aiohttp.web.Application()
aiohttp_channel_service_routes(app,adapter, MyBot())
