import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/Profile.css";
import Sidebar from "../components/Sidebar";

function Profile({ isAuthorized }) {
    const [profile, setProfile] = useState(null);
    const [games, setGames] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        api.get("/api/profile/").then((res) => {
            setProfile(res.data);
        });
        api.get("/api/active-matches/").then((res) => {
            setGames(res.data);
        });
    }, []);

    const forfeitGame = async (id) => {
        const confirmed = window.confirm("Forfeit this game?");
        if (!confirmed) return;
        try {
            await api.delete(`/api/chessmatch/${id}/`);
            setGames((prev) => prev.filter((g) => g.id !== id));
            setProfile((prev) => ({ ...prev, losses: prev.losses + 1 }));
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
                <div className="profile-container">
                    <img
                        src={profile.avatar || "/default-avatar.png"}
                        alt="Profile"
                        className="profile-pic"
                    />
                    <h2>{profile.username}</h2>
                    <p>Wins: {profile.wins}</p>
                    <p>Losses: {profile.losses}</p>

                    <div className="active-games">
                        <h3>Active Games</h3>
                        {games.length === 0 ? (
                            <p>No active games.</p>
                        ) : (
                            <ul>
                                {games.map((game) => (
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
            </div>
        </>
    );
}

export default Profile;
