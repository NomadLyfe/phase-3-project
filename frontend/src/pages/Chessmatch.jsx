import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/Chessmatch.css";
import Sidebar from "../components/Sidebar";
import Chessboard from "../components/Chessboard";

const formatElapsedTime = (seconds) => {
    const hrs = String(Math.floor(seconds / 3600)).padStart(2, "0");
    const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
    const secs = String(seconds % 60).padStart(2, "0");
    return `${hrs}:${mins}:${secs}`;
};

function Chessmatch({ isAuthorized }) {
    const [board, setBoard] = useState([]);
    const [playerColor, setPlayerColor] = useState("white");
    const [isVsComputer, setIsVsComputer] = useState(false);
    const [selected, setSelected] = useState(null);
    const [legalMoves, setLegalMoves] = useState([]);
    const [botHighlight, setBotHighlight] = useState([]);
    const [highlightCapture, setHighlightCapture] = useState([]);
    const [inCheck, setInCheck] = useState(false);
    const [checkMateStatus, setCheckMateStatus] = useState("");
    const [matchObj, setMatchObj] = useState(null);
    const [elapsedSinceStart, setElapsedSinceStart] = useState(0);
    const [elapsedSinceMove, setElapsedSinceMove] = useState(0);
    const [lastMoveTime, setLastMoveTime] = useState(null);
    const [historyIndex, setHistoryIndex] = useState(null);
    const [capturedByWhite, setCapturedByWhite] = useState([]);
    const [capturedByBlack, setCapturedByBlack] = useState([]);

    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const loadMatch = async () => {
            const res = await api.get(`/api/chessmatch/${id}/`);
            const match = res.data;
            setMatchObj(match);
            setCapturedByWhite(match.captured_by_white || []);
            setCapturedByBlack(match.captured_by_black || []);
            if (match.game_over) {
                setHistoryIndex(match.game_history.length - 1); // last move
            }
            setBoard(
                match.game_over
                    ? match.game_history[match.game_history.length - 1]
                    : match.board
            );
            const userId = JSON.parse(
                atob(localStorage.getItem("access").split(".")[1])
            ).user_id;
            const isWhite = match.player_white === userId;
            setPlayerColor(isWhite ? "white" : "black");
            setIsVsComputer(
                match.player_white === null || match.player_black === null
            );

            if (!isWhite && match.turn_color === "white")
                await triggerBotMove();
        };
        loadMatch();

        const unselectOnClickAway = () => {
            setSelected(null);
            setLegalMoves([]);
            setHighlightCapture([]);
        };
        window.addEventListener("click", unselectOnClickAway);
        return () => window.removeEventListener("click", unselectOnClickAway);
    }, [id]);

    useEffect(() => {
        const timer = setInterval(() => {
            const now = Date.now();

            if (matchObj?.created_at) {
                const startTime = new Date(matchObj.created_at).getTime();
                setElapsedSinceStart(Math.floor((now - startTime) / 1000));
            }

            if (lastMoveTime !== null) {
                setElapsedSinceMove(Math.floor((now - lastMoveTime) / 1000));
            }
        }, 1000);

        return () => clearInterval(timer);
    }, [lastMoveTime, matchObj]);

    const toBoardCoords = (x, y) =>
        playerColor === "white" ? [x, y] : [7 - x, 7 - y];

    const triggerBotMove = async () => {
        try {
            const res = await api.post(`/api/chessmatch/${id}/move/`, {});
            setBoard(res.data.board);
            if (res.data.bot_move) {
                highlightBotMove(res.data.bot_move.from, res.data.bot_move.to);
            }
            if (res.data.game_over) {
                alert("You lose by checkmate.");
                navigate("/");
            }
            setInCheck(res.data.in_check);
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
                    .filter(
                        (m) => m.type === "capture" || m.type === "en_passant"
                    )
                    .map((m) => m.to)
            );
        } catch (err) {
            console.error("Failed to fetch legal moves", err);
        }
    };

    const handleMove = (from, to) => {
        const [fromX, fromY] = from;
        const [toX, toY] = to;

        // simulate user move visually
        const tempBoard = JSON.parse(JSON.stringify(board));
        const visualCapturedPiece = tempBoard[toX][toY];
        tempBoard[toX][toY] = tempBoard[fromX][fromY];
        tempBoard[fromX][fromY] = null;
        setBoard(tempBoard);
        if (visualCapturedPiece) {
            if (playerColor === "white") {
                setCapturedByWhite([
                    ...capturedByWhite,
                    visualCapturedPiece.toLowerCase(),
                ]);
            } else {
                setCapturedByBlack([
                    ...capturedByBlack,
                    visualCapturedPiece.toUpperCase(),
                ]);
            }
        }
        setSelected(null);
        setLegalMoves([]);
        setHighlightCapture([]);

        api.post(`/api/chessmatch/${id}/move/`, { from, to })
            .then((res) => {
                setInCheck(res.data.in_check);
                console.log(res.data);
                setLastMoveTime(new Date(res.data.last_move_at).getTime());
                setElapsedSinceMove(0);
                if (res.data.bot_move) {
                    setTimeout(() => {
                        highlightBotMove(
                            res.data.bot_move.from,
                            res.data.bot_move.to
                        );
                        setBoard(res.data.board);
                        setCapturedByWhite(res.data.captured_by_white || []);
                        setCapturedByBlack(res.data.captured_by_black || []);
                        setInCheck(res.data.in_check_after_bot);
                        if (res.data.game_over) {
                            alert("You win by checkmate!");
                            navigate("/");
                        }
                        setLastMoveTime(
                            new Date(res.data.last_move_at).getTime()
                        );
                        setElapsedSinceMove(0);
                    }, 800);
                } else if (res.data.game_over) {
                    alert("You win by checkmate!");
                    navigate("/");
                } else {
                    setBoard(res.data.board);
                    setCapturedByWhite(res.data.captured_by_white || []);
                    setCapturedByBlack(res.data.captured_by_black || []);
                }
            })
            .catch((err) => {
                console.error("Move failed", err);
                alert("Move failed");
            });
    };

    const handleCellClick = (x, y, e) => {
        e.stopPropagation();
        const [row, col] = toBoardCoords(x, y);
        const piece = board[row][col];
        const isPlayerPiece =
            playerColor === "white"
                ? /[PRNBQK]/.test(piece)
                : /[prnbqk]/.test(piece);

        if (
            selected &&
            legalMoves.some((m) => m.to[0] === row && m.to[1] === col)
        ) {
            const from = selected;
            const to = [row, col];
            handleMove(from, to);
            setSelected(null);
        } else if (piece && isPlayerPiece) {
            setSelected([row, col]);
            fetchLegalMoves([row, col]);
        } else {
            setSelected(null);
            setLegalMoves([]);
            setHighlightCapture([]);
        }
    };

    const handleForfeit = async () => {
        if (
            !window.confirm(
                "Are you sure you want to forfeit this match? (This will count as a loss.)"
            )
        )
            return;
        try {
            await api.patch(`/api/chessmatch/${id}/forfeit/`);
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

    const durationIfOver =
        matchObj?.game_over && matchObj.ended_at
            ? Math.floor(
                  (new Date(matchObj.ended_at) -
                      new Date(matchObj.created_at)) /
                      1000
              )
            : null;

    const currentBoard =
        matchObj?.game_over && historyIndex !== null
            ? matchObj.game_history[historyIndex]
            : board;

    return (
        <>
            <Sidebar isAuthorized={isAuthorized} />
            <div className="chess-container">
                <h2>Chess Match</h2>
                <div className="match-timers">
                    <div className="timer-block">
                        <span className="timer-label">Elapsed Time:</span>
                        <span className="timer-value">
                            {matchObj?.game_over && durationIfOver !== null
                                ? formatElapsedTime(durationIfOver)
                                : formatElapsedTime(elapsedSinceStart)}
                        </span>
                    </div>
                    {matchObj?.game_over ? null : (
                        <div className="timer-block">
                            <span className="timer-label">Last move:</span>
                            <span className="timer-value">
                                {formatElapsedTime(elapsedSinceMove)}
                            </span>
                        </div>
                    )}
                </div>
                <Chessboard
                    board={currentBoard}
                    playerColor={playerColor}
                    selected={selected}
                    legalMoves={legalMoves}
                    highlightCapture={highlightCapture}
                    botHighlight={botHighlight}
                    handleCellClick={
                        matchObj?.game_over ? null : handleCellClick
                    }
                    capturedByOpponent={
                        playerColor == "white"
                            ? capturedByBlack
                            : capturedByWhite
                    }
                    capturedByPlayer={
                        playerColor == "white"
                            ? capturedByWhite
                            : capturedByBlack
                    }
                />
                {matchObj?.game_over && (
                    <div className="history-controls">
                        <button
                            onClick={() =>
                                setHistoryIndex((i) => Math.max(0, i - 1))
                            }
                            disabled={historyIndex <= 0}
                        >
                            ⬅️
                        </button>
                        <span className="history-index">
                            Move {historyIndex + 1} /{" "}
                            {matchObj.game_history.length}
                        </span>
                        <button
                            onClick={() =>
                                setHistoryIndex((i) =>
                                    Math.min(
                                        matchObj.game_history.length - 1,
                                        i + 1
                                    )
                                )
                            }
                            disabled={
                                historyIndex >= matchObj.game_history.length - 1
                            }
                        >
                            ➡️
                        </button>
                    </div>
                )}
                {inCheck && (
                    <p className="check-warning">
                        {playerColor === "white"
                            ? "AI is in check!"
                            : "You are in check!"}
                    </p>
                )}
                {checkMateStatus && (
                    <p className="checkmate-message">{checkMateStatus}</p>
                )}
                {matchObj?.game_over ? null : (
                    <button className="forfeit-button" onClick={handleForfeit}>
                        Forfeit
                    </button>
                )}
            </div>
        </>
    );
}

export default Chessmatch;
