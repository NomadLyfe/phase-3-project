import { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/Sidebar.css";
import { Menu } from "lucide-react";

function Sidebar({ isAuthorized }) {
    const [open, setOpen] = useState(false);

    return (
        <>
            <button className="sidebar-toggle" onClick={() => setOpen(!open)}>
                <Menu size={24} color="white" />
            </button>
            <div className={`sidebar ${open ? "open" : ""}`}>
                <nav>
                    <ul>
                        {isAuthorized ? (
                            <li>
                                <Link to="/">Home</Link>
                            </li>
                        ) : null}
                        {isAuthorized ? null : (
                            <li>
                                <Link to="/login">Login</Link>
                            </li>
                        )}
                        {isAuthorized ? null : (
                            <li>
                                <Link to="/register">Register</Link>
                            </li>
                        )}
                        {isAuthorized ? (
                            <li>
                                <Link to="/profile">Profile</Link>
                            </li>
                        ) : null}
                        {isAuthorized ? (
                            <li>
                                <Link to="/logout">Logout</Link>
                            </li>
                        ) : null}
                    </ul>
                </nav>
            </div>
        </>
    );
}

export default Sidebar;
