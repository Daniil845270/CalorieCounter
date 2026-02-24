import { useState, useEffect } from "react";
import api from "../api";

function ItemForm({ descriptionRoute, entriesRoute }) {
  const [entryDescription, setEntryDescription] = useState("");
  const [itemType, setItemType] = useState("");
  const [itemMass, setItemMass] = useState("");
  const [entriesList, setEntriesList] = useState([]);
  const [descriptionsList, setDescriptionsList] = useState([]);

  const [loading, setLoading] = useState(false);

  const fetchLists = async () => {
    setLoading(true);

    try {
      const descriptionRes = await api.get(descriptionRoute);
      console.log("successfully descriptions entries");
      console.log(descriptionRes.data);
      setDescriptionsList(descriptionRes.data);
      const entriesRes = await api.get(entriesRoute);
      console.log("successfully fetched entries");
      console.log(entriesRes.data);
      setEntriesList(entriesRes.data);
    } catch (error) {
      console.log("failed to fetch entries");
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLists();
    // console.log(descriptionList);
  }, []);

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post(entriesRoute, {
        description: entryDescription,
        item_type: itemType,
        item_mass: itemMass,
      });
      alert("Description submitted successfully");
      console.log(res.data);
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
          entriesList.map((entry) => <li key={entry.id}>{entry.item_mass}</li>)}
      </div>

      <form onSubmit={handleSubmit} className="form-container">
        <h1>{"A description form"}</h1>
        <label htmlFor="description">Choose meal description: </label>

        <select
          id="description"
          name="description"
          value={entryDescription}
          onChange={(e) => setEntryDescription(e.target.value)}
        >
          <option key={0} value="" disabled>--Please choose an option--</option>
          {!loading &&
            descriptionsList.map((description) => (
              <option key={description.id} value={description.id}>
                {description.Item_name}
              </option>
            ))}
        </select>

        <label htmlFor="mealType">Choose meal type: </label>
        <select
          id="mealType"
          name="mealType"
          value={itemType}
          onChange={(e) => setItemType(e.target.value)}
        >
          <option key={0} value="" disabled>--Please choose an option--</option>
          <option value="B">Breakfast</option>
          <option value="L">Lunch</option>
          <option value="D">Dinner</option>
          <option value="S">Snack</option>
          <option value="O">Other</option>
        </select>
        <input
          className="form-input"
          type="number"
          value={itemMass}
          onChange={(e) => setItemMass(e.target.value)}
          placeholder="item mass"
        />
        <button className="form-button" type="submit">
          {"Submit a description form"}
        </button>
      </form>
    </>
  );
}

export default ItemForm;
