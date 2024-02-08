import {Card, Hand} from "./types"

export interface DeckOfCardsApiResponse {
    success?: boolean;
    cards?: Card[];
    deck_id?: string;
    remaining?: number;
  }

export interface DealCardsResponse {
    message?: string;
    error?: string;
    dealer_hand?: Hand;
    player_hands?: Hand[];
}
