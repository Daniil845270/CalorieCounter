import { useState, useEffect } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import Header from "./Header";
import RightList from "./RightList";

function ItemForm({ descriptionRoute, entriesRoute }) {
  const [entryDescription, setEntryDescription] = useState("");
  const [itemType, setItemType] = useState("");
  const [itemMass, setItemMass] = useState("");
  const [entriesList, setEntriesList] = useState([]);
  const [descriptionsList, setDescriptionsList] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

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
    <div className="min-h-screen flex items-center justify-center p-6">
      {/* wider container so we have room for 2 columns */}
      <div className="w-full max-w-5xl ">
        {/* PAGE HEADER + NAV BUTTONS */}
        <Header pageName="entries" />

        {/* stack on mobile, side-by-side on md+ */}
        <div className="flex flex-col md:flex-row gap-8 md:items-start ">
          {/* LEFT: form */}
          <div className="w-full md:w-1/2">
            <form
              onSubmit={handleSubmit}
              className="form-container bg-base-100 p-6 rounded-xl shadow-xl ring-1 ring-base-300"
            >
              <h1 className="text-2xl font-bold text-center mb-2">
                An entry form
              </h1>

              {/* Styled description select (keeps the functional bits intact) */}
              <div className="form-control w-full">
                <label className="label" htmlFor="description">
                  <span className="label-text text-base md:text-lg font-semibold">
                    Choose meal description
                  </span>
                </label>

                <select
                  id="description"
                  name="description"
                  value={entryDescription}
                  onChange={(e) => setEntryDescription(e.target.value)}
                  className="select select-bordered w-full"
                  disabled={loading}
                >
                  <option value="" disabled>
                    --Please choose an option--
                  </option>

                  {!loading &&
                    descriptionsList.map((description) => (
                      <option key={description.id} value={description.id}>
                        {description.Item_name}
                      </option>
                    ))}
                </select>

                <label className="label">
                  <span className="label-text-alt opacity-70">
                    {loading
                      ? "Fetching descriptions…"
                      : "Select the saved food description."}
                  </span>
                </label>
              </div>

              {/* Meal type select (styled, functional bits kept) */}
              <div className="form-control w-full mt-4">
                <label className="label" htmlFor="mealType">
                  <span className="label-text text-base md:text-lg font-semibold">
                    Choose meal type
                  </span>
                </label>

                <select
                  id="mealType"
                  name="mealType"
                  value={itemType}
                  onChange={(e) => setItemType(e.target.value)}
                  className="select select-bordered w-full"
                >
                  <option value="" disabled>
                    --Please choose an option--
                  </option>
                  <option value="B">Breakfast</option>
                  <option value="L">Lunch</option>
                  <option value="D">Dinner</option>
                  <option value="S">Snack</option>
                  <option value="O">Other</option>
                </select>

                <label className="label">
                  <span className="label-text-alt opacity-70">
                    Pick the meal category for this entry.
                  </span>
                </label>
              </div>

              <fieldset className="fieldset">
                <legend className="fieldset-legend w-full">
                  <span className="block w-full text-center text-base md:text-lg font-semibold">
                    Item mass
                  </span>
                </legend>
                <input
                  type="number"
                  className="input input-sm w-full max-w-xs mx-auto"
                  placeholder="enter a number"
                  value={itemMass}
                  onChange={(e) => setItemMass(e.target.value)}
                />
              </fieldset>

              <div className="flex justify-center mt-6">
                <button className="btn" type="submit">
                  Submit an entry
                </button>
              </div>
            </form>
          </div>

          <RightList
            pageName="entries"
            loading={loading}
            entriesList={entriesList}
            fetchLists={fetchLists}
          />
        </div>
      </div>
    </div>
  );
}

export default ItemForm;
