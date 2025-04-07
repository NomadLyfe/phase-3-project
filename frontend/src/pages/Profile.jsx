import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/Profile.css";
import Sidebar from "../components/Sidebar";

function Profile({ isAuthorized }) {
    const [profile, setProfile] = useState(null);
    const [activeGames, setActiveGames] = useState([]);
    const [inactiveGames, setInactiveGames] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        api.get("/api/profile/").then((res) => {
            setProfile(res.data);
        });
        api.get("/api/chessmatches/").then((res) => {
            console.log(res.data);
            setActiveGames(res.data.filter((game) => game.game_over === false));
            setInactiveGames(
                res.data.filter((game) => game.game_over === true)
            );
        });
    }, []);

    const forfeitGame = async (id) => {
        const confirmed = window.confirm(
            "Are you sure you want to forfeit this match? (This will count as a loss.)"
        );
        if (!confirmed) return;
        try {
            await api.patch(`/api/chessmatch/${id}/forfeit/`).then((res) => {
                setActiveGames((prev) => prev.filter((g) => g.id !== id));
                setInactiveGames((prev) => [...prev, { ...res.data, id }]);
                setProfile((prev) => ({
                    ...prev,
                    losses: prev.losses + 1,
                }));
            });
        } catch (err) {
            alert("Failed to forfeit match.");
            console.error(err);
        }
    };

    const deleteGame = async (id) => {
        const confirmed = window.confirm(
            "Are you sure you want to delete this match?"
        );
        if (!confirmed) return;
        try {
            await api.delete(`/api/chessmatch/${id}/`);
            setInactiveGames((prev) => prev.filter((g) => g.id !== id));
        } catch (err) {
            alert("Failed to forfeit match.");
            console.error(err);
        }
    };

    if (!profile) return <div>Loading...</div>;

    return (
        <>
            <Sidebar isAuthorized={isAuthorized} />
            <div className="profile-wrapper">
                <h1 className="page-title">Your Profile</h1>
                <div className="profile-container">
                    <img
                        src={profile.avatar || "/default-avatar.png"}
                        alt="Profile"
                        className="profile-pic"
                    />
                    <div>
                        <h2>{profile.username}</h2>
                        <p>Wins: {profile.wins}</p>
                        <p>Losses: {profile.losses}</p>
                    </div>
                </div>
                <div className="games-container">
                    <div className="active-games">
                        <h2>Active Games</h2>
                        {activeGames.length === 0 ? (
                            <p>No active games.</p>
                        ) : (
                            <ul>
                                {activeGames.map((game) => (
                                    <li key={game.id} className="game-row">
                                        <button
                                            onClick={() =>
                                                navigate(
                                                    `/chessmatch/${game.id}`
                                                )
                                            }
                                        >
                                            Open Game #{game.id}
                                        </button>
                                        <button
                                            className="forfeit-button"
                                            onClick={() => forfeitGame(game.id)}
                                        >
                                            Forfeit
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
                <div className="games-container">
                    <div className="inactive-games">
                        <h2>Archived Games</h2>
                        {inactiveGames.length === 0 ? (
                            <p>No active games.</p>
                        ) : (
                            <ul>
                                {inactiveGames.map((game) => (
                                    <li key={game.id} className="game-row">
                                        <button
                                            onClick={() =>
                                                navigate(
                                                    `/chessmatch/${game.id}`
                                                )
                                            }
                                        >
                                            Open Game #{game.id}
                                        </button>
                                        <button
                                            className="forfeit-button"
                                            onClick={() => deleteGame(game.id)}
                                        >
                                            Delete
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}

export default Profile;
