
import { observer } from "mobx-react";
import React, { useState } from "react";

import { Card } from "./types";

const BASE_URL = 'http://localhost:8000'

const CardGame = observer(function CardGame()  {
    const [card, setCard] = useState<Card | null>(null)
    const [gameId, setGameId] = useState<string | null>('')

    const shuffleDeck = () => {
        const url = gameId ? `${BASE_URL}/game/shuffle/${gameId}/` : `${BASE_URL}/game/shuffle/`;
        fetch(url)
        .then((response) => {
            if (!response.ok) {
                // If the response status indicates failure, throw an error to jump to the catch block.
                console.log(response.status)
                throw new Error("Failed to Shuffle Deck");
            }
            console.log(response.status)
            return response.json(); // Parse the JSON response if the room is found.
        })
        .then((data) => {
            if (data.game_id) {
                setGameId(data.game_id);
            }
        })
        .catch((error) => {
            console.error(error.message);
        });
    };

    const drawCard = () => {
        if (!gameId) return;
        fetch(`${BASE_URL}/game/draw/${gameId}/`)
        .then((response) => {
            if (!response.ok) {
                // If the response status indicates failure, throw an error to jump to the catch block.
                throw new Error("Failed to Draw Card");
            }
            return response.json(); // Parse the JSON response if the room is found.
        })
        .then((data) => {
            if (data.cards[0]) {
                console.log(data.cards[0])
                return setCard(data.cards[0])
            }
        });
    };

    return (
        <div>
            <button onClick={shuffleDeck}>Shuffle/Create Deck</button>
            <button onClick={drawCard} disabled={!gameId}>Draw Card</button>
            {card && <div><img src={card.image} alt={card.code} /></div>}
        </div>
    );
});

export default CardGame;