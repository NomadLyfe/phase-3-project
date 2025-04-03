import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/Chessmatch.css";
import Sidebar from "../components/Sidebar";

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

function Chessmatch({ isAuthorized }) {
    const [board, setBoard] = useState([]);
    const [playerColor, setPlayerColor] = useState("white");
    const [isVsComputer, setIsVsComputer] = useState(false);
    const [selected, setSelected] = useState(null);
    const [legalMoves, setLegalMoves] = useState([]);
    const [botHighlight, setBotHighlight] = useState([]);
    const [highlightCapture, setHighlightCapture] = useState([]);

    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const loadMatch = async () => {
            const res = await api.get(`/api/chessmatch/${id}/`);
            const match = res.data;
            setBoard(match.board);

            const userId = JSON.parse(
                atob(localStorage.getItem("access_token").split(".")[1])
            ).user_id;
            const isWhite = match.player_white === userId;
            setPlayerColor(isWhite ? "white" : "black");
            setIsVsComputer(
                match.player_white === null || match.player_black === null
            );

            if (!isWhite && match.player_white === null) {
                await triggerBotMove();
            }
        };
        loadMatch();

        const unselectOnClickAway = () => setSelected(null);
        window.addEventListener("click", unselectOnClickAway);
        return () => window.removeEventListener("click", unselectOnClickAway);
    }, [id]);

    const triggerBotMove = async () => {
        try {
            const res = await api.post(`/api/chessmatch/${id}/computer-move/`);
            setBoard(res.data.board);
        } catch (err) {
            console.error("Bot move failed", err);
        }
    };

    const fetchLegalMoves = async (from) => {
        try {
            const res = await api.post(`/api/chessmatch/${id}/legal-moves/`, {
                from,
            });
            setLegalMoves(res.data.moves);
            setHighlightCapture(
                res.data.moves
                    .filter((m) => m.type === "capture")
                    .map((m) => m.to)
            );
        } catch (err) {
            console.error("Failed to fetch legal moves", err);
        }
    };

    const handleMove = async (from, to) => {
        try {
            const res = await api.post(`/api/chessmatch/${id}/move/`, {
                from,
                to,
            });
            setBoard(res.data.board);
            setSelected(null);
            setLegalMoves([]);

            if (res.data.bot_move) {
                const [fromBot, toBot] = res.data.bot_move;
                highlightBotMove(fromBot, toBot);
            }
        } catch (err) {
            alert("Move failed");
            console.error(err);
        }
    };

    const handleCellClick = (x, y, e) => {
        e.stopPropagation();
        const piece = board[x][y];
        const isPlayerPiece =
            playerColor === "white"
                ? /[PRNBQK]/.test(piece)
                : /[prnbqk]/.test(piece);

        if (
            selected &&
            legalMoves.some((m) => m.to[0] === x && m.to[1] === y)
        ) {
            handleMove(selected, [x, y]);
        } else if (piece && isPlayerPiece) {
            setSelected([x, y]);
            fetchLegalMoves([x, y]);
        } else {
            setSelected(null);
            setLegalMoves([]);
        }
    };

    const handleForfeit = async () => {
        if (
            !window.confirm(
                "Are you sure you want to forfeit and delete this match?"
            )
        )
            return;
        try {
            await api.delete(`/api/chessmatch/${id}/`);
            navigate("/");
        } catch (err) {
            alert("Failed to forfeit match.");
            console.error(err);
        }
    };

    const highlightBotMove = (from, to) => {
        setBotHighlight([from, to]);
        setTimeout(() => setBotHighlight([]), 1200);
    };

    return (
        <>
            <Sidebar isAuthorized={isAuthorized} />
            <div className="chess-container">
                <h2>Chess Match</h2>
                <div
                    className={`chess-board ${
                        playerColor === "black" ? "flipped" : ""
                    }`}
                >
                    {board.map((row, i) => {
                        const rowIndex = playerColor === "white" ? i : 7 - i;
                        return (
                            <div key={i} className="board-row">
                                {board[rowIndex].map((_, j) => {
                                    const colIndex =
                                        playerColor === "white" ? j : 7 - j;
                                    const cell = board[rowIndex][colIndex];
                                    const isLight =
                                        (rowIndex + colIndex) % 2 === 0;
                                    const isLegalMove = legalMoves.some(
                                        (m) =>
                                            m.to[0] === rowIndex &&
                                            m.to[1] === colIndex
                                    );
                                    const isCapture = highlightCapture.some(
                                        ([cx, cy]) =>
                                            cx === rowIndex && cy === colIndex
                                    );
                                    const isBotFrom = botHighlight.some(
                                        ([x, y]) =>
                                            x === rowIndex && y === colIndex
                                    );
                                    const isBotTo =
                                        botHighlight.length === 2 &&
                                        botHighlight[1][0] === rowIndex &&
                                        botHighlight[1][1] === colIndex;

                                    return (
                                        <div
                                            key={j}
                                            className={`board-cell ${
                                                isLight
                                                    ? "light-square"
                                                    : "dark-square"
                                            } ${
                                                isLegalMove
                                                    ? "highlight-square"
                                                    : ""
                                            } ${
                                                isCapture
                                                    ? "capture-square"
                                                    : ""
                                            } ${
                                                isBotFrom || isBotTo
                                                    ? "bot-move"
                                                    : ""
                                            }`}
                                            onClick={(e) =>
                                                handleCellClick(
                                                    rowIndex,
                                                    colIndex,
                                                    e
                                                )
                                            }
                                        >
                                            {cell && (
                                                <span className="chess-piece">
                                                    {pieceImages[cell]}
                                                </span>
                                            )}
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
        </>
    );
}

export default Chessmatch;
