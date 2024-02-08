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

export interface Hand {
    cards: Card[];
    value?: number; 
    is_active?: boolean;  
  }
  
export interface FetchOptions extends RequestInit {}

export interface GameData {
    game_id: string;
}
  
export interface PlayerData {
    userID: string;
    balance: number;
    hand: Card[];
}
  
export type SuccessCallback<T> = (data: T) => void;
export type ErrorCallback = (errorMessage: string) => void;