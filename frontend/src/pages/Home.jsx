import { useNavigate } from "react-router-dom";
import Header from "../Components/Header";

function Home() {
  const navigate = useNavigate();

  return <Header pageName="home" />;
}

export default Home;
