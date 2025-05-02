from app.stores import Stores, LarkDataStore, BubbleDataStore, ReferenceStore
from .setup_services import base_manager
from .setup_constants import base_constants

stores = Stores(
    bubble_data_store=BubbleDataStore(
        base_manager=base_manager,
        table_id=base_constants.UNPROCESSED_TABLE_ID,
    )
)