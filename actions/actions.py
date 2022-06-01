# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from xml.parsers.expat import model

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from fuzzywuzzy import fuzz, process


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
        # this part of the code allows typos in user input. threshold is 80% simiarity. 
        list_brand = df.Brand.unique().tolist()
        list_color = df.Color.unique().tolist()
        for lb in list_brand:
            if fuzz.ratio(lb.lower(), brand.lower()) >= 80:
                brand = lb
                break
        for lc in list_color:
            if fuzz.ratio(lc.lower(), color.lower()) >= 80:
                color = lc
                break

        price = df[(df.Brand==brand) & (df.Type==model) & (df.Storage==storage) & (df.Color==color)]['Price'].item()

        msg = f'The price {price} euros!'
        dispatcher.utter_message(text=msg)

        return 'hahaha'
