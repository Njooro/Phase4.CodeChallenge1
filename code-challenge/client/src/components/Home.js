import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [heroes, setHeroes] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5555/heroes")
      .then((r) => r.json())
      .then(setHeroes);
  }, []);

  return (
    <section>
      <h2>All Heroes</h2>
      <ul>
        {heroes.map((hero) => (
          <li key={hero.id}>
            <Link to={`/heroes/${hero.id}`}>{hero.super_name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Home;
