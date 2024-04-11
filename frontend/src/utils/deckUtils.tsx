import { error } from "console";
import {
  DealCardsResponse,
  DeckOfCardsApiResponse,
} from "../interfaces/apiResponses";
import { Card, Hand } from "../interfaces/types";
import { fetchData } from "./apiUtils";

const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export function shuffleDeck(
  gameId: string | null,
  setLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setError: React.Dispatch<React.SetStateAction<string | null>>
) {
  setLoading(true);
  setError("");

  fetchData<void>(
    `${BASE_URL}/game/shuffle/${gameId}/`,
    {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    },
    () => {
      // onSuccess callback logic
      console.log("Deck shuffled successfully");
      // Handle successful deck shuffle here, if there's any specific logic needed
    },
    (errorMessage: string) => {
      // onError callback logic
      console.error(errorMessage);
      setError(errorMessage);
    }
  ).finally(() => {
    setLoading(false);
  });
}

export function drawCard(gameId: string | null) : Promise<Card>{
  return new Promise((resolve, reject) => {
    fetchData<DeckOfCardsApiResponse>(
      `${BASE_URL}/game/draw/${gameId}/`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      },
      (data) => {
        // onSuccess callback logic
        if (data.cards && data.cards.length > 0) {
          resolve(data.cards[0]);
        } else {
          reject("Deck is Empty.");
        }
      },
      (errorMessage) => {
        // onError callback logic
        reject(errorMessage);
      }
    ).finally(() => {});
  });
}
