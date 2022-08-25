# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import logging
logger = logging.getLogger(__name__)

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import wikipedia

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""
    
    # s.koushik - > some how i couln't make the programm lead to here

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_clarify")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]


class ActionTest(Action):
    def name(self) -> Text:
        return "action_test"
    def run(self,dispatcher,tracker,domain):
        dispatcher.utter_message(text="Here")
        logger.error("in custom action error")
        logger.debug("in custom action debug")
        return []
    
    
class ActionGetWikiData(Action):
    def name(self) -> Text:
        return "action_get_wiki_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            #logger.debug(tracker.latest_message)
            usr_query = tracker.latest_message['text']
            # tracker.latest_message look as foollows
            # {'intent': {'name': 'nlu_fallback', 'confidence': 0.3}, 'entities': 
            # [], 'text': 'msg that you would ask', 'message_id': '1f0f37c1c5724e8693e46112acefa25a', 'metadata': {}, 'text_tokens': [[0, 4]], 'intent_ranking': [{'name': 'nlu_fallback', 'confidence': 0.3}, {'name': 'affirm', 'confidence': 0.27907925844192505}, {'name': 'mood_great', 'confidence': 0.0973411351442337}, {'name': 'deny', 'confidence': 0.05721075087785721}, {'name': 'causes_of_fault', 'confidence': 0.02676660567522049}, {'name': 'greet', 'confidence': 0.02565963752567768}, {'name': 'pros_cons_nickel', 'confidence': 0.022358154878020287}, {'name': 'fault_types', 'confidence': 0.016350051388144493}, {'name': 'PCM_safety', 'confidence': 0.014910494908690453}, {'name': 'cell_capacity_effective', 'confidence': 
            # 0.01431310549378395}, {'name': 'equalizing_charge_need', 'confidence': 0.014114963822066784}], 'response_selector': 
            # {'all_retrieval_intents': [], 'default': {'response': {'responses': None, 'confidence': 0.0, 'intent_response_key': 
            # None, 'utter_action': 'utter_None'}, 'ranking': []}}}
            #print('Entity to be searched is: ' + usr_query)
            #dispatcher.utter_message('Process started')
            
            # get the list of topics from wikipedia
            topics = wikipedia.search(usr_query)
            if topics:
                #if any related topics found the chech the summary for the first topic
                spar_response = wikipedia.summary(title=topics[0],sentences=3)
                logger.info(spar_response)
            else:
                spar_response = "Sorry, I could not find any answer for you at the moment."    
            
            dispatcher.utter_message(spar_response)
            return [UserUtteranceReverted()]
            
        except Exception as err:
            logger.error(err)
            dispatcher.utter_message("Sorry, I could not find any answer for you at the moment.")
            return [UserUtteranceReverted()]