import { useState, useEffect } from "react";
import api from "../api";

function DescriptionForm({ route }) {
  const [itemName, setItemName] = useState("");
  const [proteinPer100g, setProteinPer100g] = useState("");
  const [carbohydratePer100g, setCarbohydratePer100g] = useState("");
  const [fatPer100g, setFatPer100g] = useState("");
  const [kcalPer100g, setKcalPer100g] = useState("");
  const [descriptionList, setDescriptionList] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDescriptionList = async () => {
    setLoading(true);

    try {
      const res = await api.get(route);
      console.log("successfully fetched descriptions");
      console.log(res.data);
      setDescriptionList(res.data);
    } catch (error) {
      console.log("failed to fetch descriptions");
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDescriptionList();
    // console.log(descriptionList);
  }, []);

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post(route, {
        Item_name: itemName,
        Protein_per_100g: proteinPer100g,
        Carbohydrate_per_100g: carbohydratePer100g,
        Fat_per_100g: fatPer100g,
        Kcal_per_100g: kcalPer100g,
      });
      alert("Description submitted successfully");
      //   console.log(res.data);
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div>
        {loading && <p>Loading...</p>}

        {!loading &&
          descriptionList.map((description) => (
            <li key={description.id}>
              {description.Item_name} - protein: {description.Protein_per_100g},
              carbs: {description.Carbohydrate_per_100g}, fat:{" "}
              {description.Fat_per_100g}, kcal: {description.Kcal_per_100g}
            </li>
          ))}
      </div>

      <form onSubmit={handleSubmit} className="form-container">
        <h1>{"A description form"}</h1>
        <input
          className="form-input"
          type="text"
          value={itemName}
          onChange={(e) => setItemName(e.target.value)}
          placeholder="item name"
        />
        <input
          className="form-input"
          type="number"
          value={proteinPer100g}
          onChange={(e) => setProteinPer100g(e.target.value)}
          placeholder="setProteinPer100g"
        />
        <input
          className="form-input"
          type="number"
          value={carbohydratePer100g}
          onChange={(e) => setCarbohydratePer100g(e.target.value)}
          placeholder="setCarbohydratePer100g"
        />
        <input
          className="form-input"
          type="number"
          value={fatPer100g}
          onChange={(e) => setFatPer100g(e.target.value)}
          placeholder="setFatPer100g"
        />
        <input
          className="form-input"
          type="number"
          value={kcalPer100g}
          onChange={(e) => setKcalPer100g(e.target.value)}
          placeholder="setKcalPer100g"
        />
        <button className="form-button" type="submit">
          {"Submit a description form"}
        </button>
      </form>
    </>
  );
}

export default DescriptionForm;
