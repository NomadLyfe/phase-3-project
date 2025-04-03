import Form from "../components/Form";
import Sidebar from "../components/Sidebar";

function Login() {
    return (
        <>
            <Sidebar isAuthorized={false} />
            <div className="login-wrapper">
                <Form route="api/token/" method="login" />
            </div>
        </>
    );
}

export default Login;
