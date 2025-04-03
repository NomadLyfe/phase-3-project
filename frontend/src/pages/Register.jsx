import Form from "../components/Form";
import Sidebar from "../components/Sidebar";

function Register() {
    return (
        <>
            <Sidebar isAuthorized={false} />
            <div className="register-wrapper">
                <Form route="api/user/register/" method="register" />
            </div>
        </>
    );
}

export default Register;
