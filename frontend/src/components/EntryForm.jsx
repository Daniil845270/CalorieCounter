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
    <div className="min-h-screen flex items-center justify-center p-6">
      {/* wider container so we have room for 2 columns */}
      <div className="w-full max-w-5xl ">
        {/* PAGE HEADER + NAV BUTTONS */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold">Food items</h1>
              <p className="text-sm opacity-70 mt-1">
                Add new foods on the left. Browse saved items on the right.
              </p>
            </div>

            {/* 3 horizontal buttons */}
            <div className="flex flex-wrap gap-3">
              <button type="button" className="btn btn-outline">
                Button 1
              </button>
              <button type="button" className="btn btn-primary">
                Button 2
              </button>
              <button type="button" className="btn">
                Button 3
              </button>
            </div>
          </div>
        </div>

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

              {/* <input
                className="form-input"
                type="number"
                value={itemMass}
                onChange={(e) => setItemMass(e.target.value)}
                placeholder="item mass"
              /> */}

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

          {/* RIGHT: list */}
          <div className="w-full md:w-1/2"></div>
          <div className="bg-base-100 p-6 rounded-xl shadow-xl ring-1 ring-base-300">
            {/* Header */}
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold">Saved entries</h2>
                <p className="text-sm opacity-70">
                  {loading ? "Loading…" : `${entriesList.length} item(s)`}
                </p>
              </div>

              <button
                type="button"
                className="btn btn-sm"
                onClick={fetchLists}
                disabled={loading}
              >
                Refresh
              </button>
            </div>

            {/* Body */}

            <div className="mt-4 max-h-[70vh] overflow-y-auto">
              {loading && <p>Loading...</p>}

              {!loading && entriesList.length === 0 && (
                <div className="py-8 text-center opacity-70">
                  No entries yet. Add one on the left.
                </div>
              )}

              {!loading && entriesList.length > 0 && (
                <ul className="mt-4 space-y-3">
                  {entriesList.map((d) => (
                    <li
                      key={d.id}
                      className="relative p-4 rounded-xl bg-base-100 ring-1 ring-base-300 shadow-sm hover:shadow-md hover:bg-base-200 transition"
                    >
                      {/* Top-right action button */}
                      <button
                        type="button"
                        className="btn btn-xs btn-outline absolute top-4 right-4"
                        onClick={() => {
                          // you will add your logic here
                          console.log("Clicked item:", d.id);
                        }}
                      >
                        Action
                      </button>

                      <div className="font-bold text-lg pr-20">
                        {d.description} (write actual description later)
                      </div>

                      <div className="mt-2 text-sm opacity-80 tabular-nums pr-20">
                        <span className="inline-block mr-4">
                          Item type: {d.item_type}
                        </span>
                        <span className="inline-block mr-4">
                          Item mass: {d.item_mass}
                        </span>
                        <span className="inline-block mr-4">
                          Date consumed: {d.consumed_date}
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ItemForm;
