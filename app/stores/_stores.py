from .lark_data_store import LarkDataStore
from app.stores import BubbleDataStore, \
    ReferenceStore


class Stores:
    def __init__(
        self,
        bubble_data_store: BubbleDataStore,
    ):
        self.bubble_data_store: BubbleDataStore = bubble_data_store
