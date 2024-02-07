from pyzotero import zotero
import os
from dotenv import load_dotenv
load_dotenv()

def get_data_from_zotero(ZOTERO_KEY,IPBES_ZOTERO_ID,COLLECTION_IDS,CHAPTER_IDS,ALL_COLLECTIONS):
    zot = zotero.Zotero(IPBES_ZOTERO_ID, 'group', ZOTERO_KEY)
    for i in range(len(COLLECTION_IDS)):
        all_collection_items = []
        start = 0
        while True:
            items = zot.collection_items(COLLECTION_IDS[i], start=start, limit=100)
            if not items:
                break
            all_collection_items.extend(items)
            start += 100
        ALL_COLLECTIONS[f'collection_chapter_{CHAPTER_IDS[i]}']=all_collection_items
    return ALL_COLLECTIONS