import { useEffect, useState } from "react";
import { observer } from "mobx-react";

import {
  Card,
  Hand,
  FetchOptions,
  SuccessCallback,
  ErrorCallback,
  GameData,
  PlayerData,
} from "../interfaces/types";

import {
  DealCardsResponse,
  DeckOfCardsApiResponse,
} from "../interfaces/apiResponses";

import "../static/css/Hands.css";

const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

const CardGame = observer(function CardGame() {
  const [card, setCard] = useState<Card | null>(null);
  const [gameId, setGameId] = useState<string | null>("");
  const [playerId, setPlayerId] = useState<string | null>("");
  const [error, setError] = useState<string | null>("");
  const [isLoading, setLoading] = useState(false);

  const [dealerHand, setDealerHand] = useState<Hand | null>(null);
  const [playerHands, setPlayerHands] = useState<Hand[] | null>(null);

  async function fetchData<
    T
  >(url: string, options: FetchOptions, onSuccess: SuccessCallback<T>, onError: ErrorCallback): Promise<void> {
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`Failed to fetch from ${url}`);
      }
      const data = (await response.json()) as T;
      onSuccess(data);
    } catch (error) {
      if (error instanceof Error) {
        console.error(error.message);
        onError(error.message);
      } else {
        console.error("An unknown error occurred");
        onError("An unknown error occurred");
      }
    }
  }

  useEffect(() => {
    if (!playerId) {
      fetchData<PlayerData>(
        `${BASE_URL}/player/get_player/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        },
        (data) => {
          console.log(data);
          setPlayerId(data.userID);
        },
        setError
      );
    }
  }, [playerId]);

  useEffect(() => {
    if (!playerId) return;

    const createGame = () => {
      fetchData<GameData>(
        `${BASE_URL}/game/create/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        },
        (data) => {
          setGameId(data.game_id);
        },
        (errorMessage) => {
          setError(errorMessage);
        }
      );
    };

    fetchData<GameData>(
      `${BASE_URL}/player/get_game/`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      },
      (data) => {
        if (data.game_id) {
          setGameId(data.game_id);
        } else {
          // If no game is associated, create a new game
          createGame();
        }
      },
      (errorMessage) => {
        setError(errorMessage);
        // If error in fetching game, possibly create a new game
        createGame();
      }
    );
  }, [playerId]);

  useEffect(() => {
    if (gameId) {
      console.log(gameId);
      fetchData<GameData>(
        `${BASE_URL}/player/join/${gameId}/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        },
        () => {},
        setError
      );
    }
  }, [gameId]);

  const shuffleDeck = () => {
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
      (errorMessage) => {
        // onError callback logic
        console.error(errorMessage);
        setError(errorMessage);
      }
    ).finally(() => {
      setLoading(false);
    });
  };

  const drawCard = () => {
    setLoading(true);
    setError("");
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
          setCard(data.cards[0]);
        } else {
          throw new Error("No cards returned");
        }
        // Handle successful deck shuffle here, if there's any specific logic needed
      },
      (errorMessage) => {
        // onError callback logic
        console.error(errorMessage);
        setError(errorMessage);
      }
    ).finally(() => {
      setLoading(false);
    });
  };

  const dealCards = () => {
    setLoading(true);
    setError("");
    fetchData<DealCardsResponse>(
      `${BASE_URL}/game/deal/${gameId}/`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      },
      (data) => {
        // onSuccess callback logic
        if (data.dealer_hand && data.dealer_hand.cards.length > 0) {
          setDealerHand(data.dealer_hand);
        } else {
          throw new Error("No dealer hand returned");
        }
        if (data.player_hands && data.player_hands.length > 0) {
          setPlayerHands(data.player_hands);
        } else {
          throw new Error("No player hand returned");
        }
        // Handle successful deck shuffle here, if there's any specific logic needed
      },
      (errorMessage) => {
        // onError callback logic
        console.error(errorMessage);
        setError(errorMessage);
      }
    ).finally(() => {
      setLoading(false);
    });
  };

  const addHand = () => {
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
  };

  return (
    <div>
      <button onClick={addHand} disabled={!gameId || isLoading}>
        Add Hand
      </button>
      <button onClick={dealCards} disabled={!gameId || isLoading}>
        Deal Cards
      </button>
      <button onClick={shuffleDeck} disabled={!gameId || isLoading}>
        Shuffle Cards
      </button>
      <div>
        {/* Parent container for all hands */}
        <div>
          <h2>Dealer's Hand</h2>
          <div className="hand">
            {dealerHand &&
              dealerHand.cards.map((card, index) => (
                <img
                  key={index}
                  src={card.image}
                  alt={card.code}
                  className="card"
                />
              ))}
          </div>
        </div>
      </div>
      <div className="handsContainer">
        {playerHands &&
          playerHands.map((hand, handIndex) => (
            <div key={handIndex}>
              <h3>Player {handIndex + 1}'s Hand</h3>
              <div className="hand">
                {hand.cards.map((card, cardIndex) => (
                  <img
                    key={cardIndex}
                    src={card.image}
                    alt={card.code}
                    className="card"
                  />
                ))}
              </div>
            </div>
          ))}
      </div>
      {error && <div className="error">{error}</div>}
    </div>
  );
});
export default CardGame;
