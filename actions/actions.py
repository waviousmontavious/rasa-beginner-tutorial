from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction


class HealthForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_health_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        custom_slots = ["confirm_exercise"]
        required_slots = custom_slots + slots_mapped_in_domain
        return required_slots

    async def extract_confirm_exercise(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_intent_of_latest_message() == 'request_health_form':
            return {}
        last_bot_event = next(e for e in reversed(tracker.events) if e['event'] == 'bot')
        if last_bot_event['metadata']['template_name'] != 'utter_ask_confirm_exercise':
            return {}

        if tracker.get_intent_of_latest_message() == 'affirm':
            return {"confirm_exercise": True}
        else:
            return {"confirm_exercise": False, "exercise": "None"}


class SaveDataAction(Action):

    def name(self) -> Text:
        return "save_data"

    async def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        print('running Save Data Action')
        return []
