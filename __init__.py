from aqt import gui_hooks
from aqt import mw
from aqt.utils import tooltip
from anki.cards import Card

def suspend_mature_cards() -> None:
    # Get config
    config = mw.addonManager.getConfig(__name__)
    threshold = config.get('suspend_threshold', 14)  # Default to 14 if not set
    excluded_decks = config.get('excluded_decks', [])  # Default to empty list if not set
    
    # Build deck exclusion filter string
    deck_filter = ""
    if excluded_decks:
        deck_filter = '-(' + ' OR '.join(f'deck:"{deck}"' for deck in excluded_decks) + ')'
    
    # Find all cards with interval > threshold that aren't already suspended, excluding specified decks
    cards_to_suspend = mw.col.find_cards(f"{deck_filter} prop:ivl>{threshold} -is:suspended")
    
    if not cards_to_suspend:
        return
        
    # Suspend all found cards
    for cid in cards_to_suspend:
        card = mw.col.get_card(cid)
        card.queue = -1
        mw.col.update_card(card)
    
    # Show a tooltip instead of a popup
    tooltip(f"Suspended {len(cards_to_suspend)} cards with intervals exceeding {threshold} days", period=3000)

# Register the hook to run after sync completes
gui_hooks.sync_did_finish.append(suspend_mature_cards)
