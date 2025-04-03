import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/Chessmatch.css";

const pieceImages = {
  P: "♙",
  R: "♖",
  N: "♘",
  B: "♗",
  Q: "♕",
  K: "♔",
  p: "♟",
  r: "♜",
  n: "♞",
  b: "♝",
  q: "♛",
  k: "♚",
};

function Chessmatch() {
  const [board, setBoard] = useState([]);
  const [playerColor, setPlayerColor] = useState("white");
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    api.get(`/api/chessmatch/${id}/`).then((res) => {
      setBoard(res.data.board);

      const userId = JSON.parse(atob(localStorage.getItem("access_token").split(".")[1])).user_id;
      const isWhite = res.data.player_white === userId;
      setPlayerColor(isWhite ? "white" : "black");
    });
  }, [id]);

  const handleMove = (from, to) => {
    api.post(`/api/chessmatch/${id}/move/`, { from, to }).then((res) => {
      setBoard(res.data.board);
    });
  };

  const handleForfeit = async () => {
    const confirmed = window.confirm("Are you sure you want to forfeit and delete this match?");
    if (!confirmed) return;

    try {
      await api.delete(`/api/chessmatch/${id}/`);
      navigate("/");
    } catch (err) {
      alert("Failed to forfeit match.");
      console.error(err);
    }
  };

  return (
    <div className="chess-container">
      <h2>Chess Match</h2>
      <div className={`chess-board ${playerColor === "black" ? "flipped" : ""}`}>
        {board.map((row, i) => {
            const rowIndex = playerColor === "white" ? i : 7 - i;
            return (
            <div key={i} className="board-row">
                {board[rowIndex].map((_, j) => {
                const colIndex = playerColor === "white" ? j : 7 - j;
                const cell = board[rowIndex][colIndex];
                const isLight = (rowIndex + colIndex) % 2 === 0;

                return (
                    <div
                    key={j}
                    className={`board-cell ${isLight ? "light-square" : "dark-square"}`}
                    >
                    {cell && <span className="chess-piece">{pieceImages[cell]}</span>}
                    </div>
                );
                })}
            </div>
            );
        })}
      </div>
      <button className="forfeit-button" onClick={handleForfeit}>
        Forfeit
      </button>
    </div>
  );
}

export default Chessmatch;