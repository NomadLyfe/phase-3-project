import React from "react";
import { PIECE_IMAGES } from "../constants";

function Chessboard({
    board,
    playerColor,
    selected,
    legalMoves,
    highlightCapture,
    botHighlight,
    handleCellClick,
    capturedByOpponent,
    capturedByPlayer,
}) {
    const visualBoard =
        playerColor === "white" ? board : [...board].slice().reverse();

    const renderCapturedPieces = (pieces, direction = "down") => {
        const columns = [];
        const maxPerColumn = 8;
        for (let i = 0; i < pieces.length; i += maxPerColumn) {
            columns.push(pieces.slice(i, i + maxPerColumn));
        }

        return (
            <div className={`captured-container ${direction}`}>
                {columns.map((col, colIndex) => (
                    <div key={colIndex} className="captured-column">
                        {(direction === "up" ? [...col].reverse() : col).map(
                            (p, i) => (
                                <img
                                    key={i}
                                    className={`captured-piece ${
                                        p === p.toUpperCase()
                                            ? "whitePiece"
                                            : "blackPiece"
                                    }`}
                                    src={PIECE_IMAGES[p]}
                                    alt={p}
                                />
                            )
                        )}
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="chessboard-with-captures">
            {renderCapturedPieces(capturedByOpponent, "down")}
            <div className="board-bezel">
                <div
                    className={`chess-board ${
                        playerColor === "black" ? "flipped" : ""
                    }`}
                >
                    {visualBoard.map((row, i) => {
                        const rowIndex = playerColor === "white" ? i : 7 - i;
                        const visualRow =
                            playerColor === "white"
                                ? row
                                : [...row].slice().reverse();
                        return (
                            <div key={i} className="board-row">
                                {visualRow.map((_, j) => {
                                    const colIndex =
                                        playerColor === "white" ? j : 7 - j;
                                    const cell = board[rowIndex][colIndex];
                                    const isLight =
                                        (rowIndex + colIndex) % 2 === 0;

                                    const move = legalMoves.find(
                                        (m) =>
                                            m.to[0] === rowIndex &&
                                            m.to[1] === colIndex
                                    );
                                    const isHighlighted = !!move;
                                    const isCheckMove =
                                        move?.type === "check" ||
                                        move?.type === "checkmate";
                                    const isCapture = highlightCapture.some(
                                        ([cx, cy]) =>
                                            cx === rowIndex && cy === colIndex
                                    );
                                    const isBotFrom =
                                        botHighlight.length &&
                                        botHighlight[0][0] === rowIndex &&
                                        botHighlight[0][1] === colIndex;
                                    const isBotTo =
                                        botHighlight.length === 2 &&
                                        botHighlight[1][0] === rowIndex &&
                                        botHighlight[1][1] === colIndex;

                                    const isSelected =
                                        selected &&
                                        selected[0] === rowIndex &&
                                        selected[1] === colIndex;

                                    return (
                                        <div
                                            key={j}
                                            className={`board-cell ${
                                                isLight
                                                    ? "light-square"
                                                    : "dark-square"
                                            } ${
                                                isCheckMove
                                                    ? "check-square"
                                                    : isHighlighted
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
                                            } ${
                                                isSelected
                                                    ? "selected-square"
                                                    : ""
                                            }`}
                                            onClick={(e) =>
                                                handleCellClick
                                                    ? handleCellClick(i, j, e)
                                                    : null
                                            }
                                        >
                                            {cell && (
                                                <img
                                                    className={`chess-piece ${
                                                        cell ===
                                                        cell.toUpperCase()
                                                            ? "whitePiece"
                                                            : "blackPiece"
                                                    }`}
                                                    src={PIECE_IMAGES[cell]}
                                                    alt={cell}
                                                />
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        );
                    })}
                </div>
            </div>
            {renderCapturedPieces(capturedByPlayer, "up")}
        </div>
    );
}

export default Chessboard;
