import { useEffect, useState } from "react";
import { observer } from "mobx-react";

import {
  Card,
  Hand,
  GameData,
  PlayerData,
} from "../interfaces/types";

import {
  DealCardsResponse,
  DeckOfCardsApiResponse,
} from "../interfaces/apiResponses";

import "../static/css/Hands.css";

import { fetchData } from "../utils/apiUtils";

import { shuffleDeck, drawCard } from "../utils/deckUtils";
import { dealCards, addHand, hitHand, standHand } from "../utils/gameUtils";

const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

const CardGame = observer(function CardGame() {
  const [gameId, setGameId] = useState<string | null>("");
  const [playerId, setPlayerId] = useState<string | null>("");
  const [error, setError] = useState<string | null>("");
  const [isLoading, setLoading] = useState(false);

  const [dealerHand, setDealerHand] = useState<Hand | null>(null);
  const [playerHands, setPlayerHands] = useState<Hand[]>([]);

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
        (errorMessage) => {
          setError(errorMessage);
        }
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
        // If error in fetching game, create a new game
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
        (errorMessage) => {
          setError(errorMessage);
        }
      );
    }
  }, [gameId]);

  function isHandDisabled(index : number) {
    return !gameId || isLoading || !playerHands[index].is_active || playerHands[index].cards.length === 0
  }

  const shuffle = () => {
    shuffleDeck(gameId, setLoading, setError)
  };

  const deal = () => {
    dealCards(gameId, setLoading, setDealerHand, setPlayerHands, setError)
  };

  const add = () => {
    addHand(gameId, setLoading, setError)
  };

  const hit = (index : number) => {
    hitHand(gameId, playerHands, setLoading, setError, setPlayerHands, index)
  }

  const stand = (index : number) => {
    standHand(gameId, playerHands, setLoading, setError, setPlayerHands, index)
  }


  return (
    <div>
      <button onClick={add} disabled={!gameId || isLoading}>
        Add Hand
      </button>
      <button onClick={deal} disabled={!gameId || isLoading}>
        Deal Cards
      </button>
      <button onClick={shuffle} disabled={!gameId || isLoading}>
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
              <button onClick={() => hit(handIndex)} disabled={isHandDisabled(handIndex)}>
                Hit
              </button>
              <button onClick={() => stand(handIndex)} disabled={isHandDisabled(handIndex)}>
                Stand
              </button>
              <button onClick={() => hit(handIndex)} disabled={isHandDisabled(handIndex)}>
                Split
              </button>
              <button onClick={() => hit(handIndex)} disabled={isHandDisabled(handIndex)}>
                Double
              </button>
            </div>
          ))}
      </div>
      {error && <div className="error">{error}</div>}
    </div>
  );
});
export default CardGame;
