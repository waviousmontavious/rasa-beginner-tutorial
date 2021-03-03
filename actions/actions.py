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
        if all(s in slots_mapped_in_domain for s in custom_slots):
            return slots_mapped_in_domain

        required_slots = custom_slots + slots_mapped_in_domain
        return required_slots

    async def extract_confirm_exercise(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        # todo - figure out why this keeps running even when the slot is filled
        print("Confirm Exercise Extractor is running")
        print(tracker.slots)
        if tracker.get_intent_of_latest_message() == 'request_health_form':
            return {"confirm_exercise": None}
        last_bot_event = next(e for e in reversed(tracker.events) if e['event'] == 'bot')
        if last_bot_event['metadata']['template_name'] != 'utter_ask_confirm_exercise':
            return {"confirm_exercise": None}

        if tracker.get_intent_of_latest_message() == 'affirm':
            return {"confirm_exercise": True}
        else:
            return {"confirm_exercise": False, "exercise": None}
