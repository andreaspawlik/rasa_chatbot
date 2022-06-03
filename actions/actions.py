# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from xml.parsers.expat import model

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from fuzzywuzzy import fuzz, process


def find_best_match(item_list, user_input, cap = 30):
    result = user_input
    ratio = 0
   
    for item in item_list:
        item_ratio = fuzz.ratio(item.lower(), user_input.lower())
       
        if item_ratio >= cap and item_ratio > ratio:
            result = item
            ratio = item_ratio
   
    return result

class ActionProvidePrice(Action):

    def name(self) -> Text:
        return "action_provide_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        brand = tracker.get_slot('brand')
        model = tracker.get_slot('model')
        color = tracker.get_slot('color')
        storage = tracker.get_slot('storage')
        
        df = pd.read_pickle('inventory.pkl')
       
        # this part of the code allows typos in user input.
        #  
        list_brand = df.Brand.unique().tolist()
        brand = find_best_match(list_brand, brand, cap=60)

        list_model = df.Type.unique().tolist()
        model = find_best_match(list_model, model, cap=60)

        list_color = df.Color.unique().tolist()
        color = find_best_match(list_color, color, cap=60)
    
        storage = ''.join(i for i in storage if i.isdigit()) ## remove nondigits
        storage += 'G' ## add unit as in the table
        
        msg = f'slot values: {brand}, {model}, {color}, {storage}'
        dispatcher.utter_message(text=msg)

        try:
            matches = df[(df.Brand==brand) & (df.Type==model) & (df.Storage==storage) & (df.Color==color)]['Price']

            price = matches.item()
            msg = f'The price {price} euros!'
            dispatcher.utter_message(text=msg)

        except:

            msg = 'The item cannot be found in the catalogue.'
            dispatcher.utter_message(text=msg)

        #return [SlotSet('brand', None), SlotSet('model', None), SlotSet('color', None), SlotSet('storage', None)]
