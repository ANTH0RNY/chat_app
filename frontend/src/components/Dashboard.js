import { useContext } from "react"; 
import { AuthContext } from "../AuthContext";
import { Navigate } from "react-router-dom"; 

function Dashboard({user}) {
  const { token, loading } = useContext(AuthContext);
  if (loading) {
    return null;
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return <h1>Dashboard: welcome {user} to your chat interface</h1>;
}

export default Dashboard;