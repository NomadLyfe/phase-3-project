import "../styles/Home.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api";
import Sidebar from "../components/Sidebar";

function Home({ isAuthorized }) {
    const navigate = useNavigate();
    const [color, setColor] = useState("white");

    const createMatch = async () => {
        try {
            const res = await api.post("/api/chessmatch/", {
                vs_computer: true,
                player_color: color,
            });
            navigate(`/chessmatch/${res.data.id}`);
        } catch (err) {
            alert("Failed to start match");
            console.error(err);
        }
    };

    return (
        <>
            <Sidebar isAuthorized={isAuthorized} />
            <div className="home-container">
                <h1>Welcome to Chess Arena</h1>
                <div className="color-select">
                    <label>
                        <input
                            type="radio"
                            value="white"
                            checked={color === "white"}
                            onChange={() => setColor("white")}
                        />
                        Play as White
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="black"
                            checked={color === "black"}
                            onChange={() => setColor("black")}
                        />
                        Play as Black
                    </label>
                </div>
                <div className="menu-buttons">
                    <button onClick={createMatch}>Play vs Computer</button>
                </div>
            </div>
        </>
    );
}

export default Home;
