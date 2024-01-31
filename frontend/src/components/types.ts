export interface Card {
    code: string;
    image: string;
    images: {
        svg: string;
        png: string;
    };
    value: string;
    suit: string;
}

export interface DeckOfCardsApiResponse {
    success: boolean;
    cards: Card[];
    deck_id: string;
    remaining: number;
  }

export interface FetchOptions extends RequestInit {}

export interface GameData {
    game_id: string;
}
  
export interface PlayerData {
    userID: string;
}
  
export type SuccessCallback<T> = (data: T) => void;
export type ErrorCallback = (errorMessage: string) => void;