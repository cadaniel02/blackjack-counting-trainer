import {
  DealCardsResponse,
  DeckOfCardsApiResponse,
} from "../interfaces/apiResponses";
import { Card, Hand } from "../interfaces/types";
import { fetchData } from "./apiUtils";

import { drawCard } from "./deckUtils";

const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export function dealCards(
  gameId: string | null,
  setLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setDealerHand: React.Dispatch<React.SetStateAction<Hand | null>>,
  setPlayerHands: React.Dispatch<React.SetStateAction<Hand[]>>,
  setError: React.Dispatch<React.SetStateAction<string | null>>
) {
  setLoading(true);
  setError("");
  fetchData<DealCardsResponse>(
    `${BASE_URL}/game/deal/${gameId}/`,
    {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    },
    (data: DealCardsResponse) => {
      // onSuccess callback logic
      if (data.dealer_hand && data.dealer_hand.cards.length > 0) {
        setDealerHand(data.dealer_hand);
      } else {
        throw new Error("Deck is Empty.");
      }
      if (data.player_hands && data.player_hands.length > 0) {
        setPlayerHands(data.player_hands);
      } else {
        throw new Error("Deck is Empty.");
      }
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

export function addHand(
  gameId: string | null,
  setLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setError: React.Dispatch<React.SetStateAction<string | null>>
) {
  setLoading(true);
  setError("");

  fetchData<void>(
    `${BASE_URL}/game/add_hand/${gameId}/`, // Update URL as needed based on your API endpoint
    {
      method: "POST", // Assuming adding a hand is a POST request; update as needed
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    },
    (_) => {},
    (errorMessage) => {
      // onError callback logic
      console.error(errorMessage);
      setError(errorMessage);
    }
  ).finally(() => {
    setLoading(false);
  });
}

export function hitHand(
  gameId: string | null,
  playerHands: Hand[],
  setLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setError: React.Dispatch<React.SetStateAction<string | null>>,
  setPlayerHands: React.Dispatch<React.SetStateAction<Hand[]>>,
  index: number
) {
  setLoading(true);
  setError("");
  drawCard(gameId)
    .then((card) => {
      const updatedHands = [...playerHands];
      const handToUpdate = { ...updatedHands[index] };
      handToUpdate.cards = [...handToUpdate.cards, card];
      updatedHands[index] = handToUpdate;
      setPlayerHands(updatedHands);
    })
    .catch((error) => {
      console.error(error);
      setError(error);
    })
    .finally(() => {
      setLoading(false);
    });
}

export function standHand(
    gameId: string | null,
    playerHands: Hand[],
    setLoading: React.Dispatch<React.SetStateAction<boolean>>,
    setError: React.Dispatch<React.SetStateAction<string | null>>,
    setPlayerHands: React.Dispatch<React.SetStateAction<Hand[]>>,
    index: number
){
    const updatedHands = [...playerHands];
    const handToUpdate = { ...updatedHands[index] };
    handToUpdate.is_active = false
    updatedHands[index] = handToUpdate;
    setPlayerHands(updatedHands);
}

