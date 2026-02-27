import { useState, useEffect } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import Header from "./Header";
import RightList from "./RightList";

function DescriptionForm({ route }) {
  const [itemName, setItemName] = useState("");
  const [proteinPer100g, setProteinPer100g] = useState("");
  const [carbohydratePer100g, setCarbohydratePer100g] = useState("");
  const [fatPer100g, setFatPer100g] = useState("");
  const [kcalPer100g, setKcalPer100g] = useState("");
  const [descriptionList, setDescriptionList] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

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
    <div className="min-h-screen flex items-center justify-center p-6">
      {/* wider container so we have room for 2 columns */}
      <div className="w-full max-w-5xl ">
        {/* PAGE HEADER + NAV BUTTONS */}
        <Header pageName="descriptions" />

        {/* stack on mobile, side-by-side on md+ */}
        <div className="flex flex-col md:flex-row gap-8 md:items-start ">
          {/* LEFT: form */}
          <div className="w-full md:w-1/2">
            <form
              onSubmit={handleSubmit}
              className="form-container bg-base-100 p-6 rounded-xl shadow-xl ring-1 ring-base-300"
            >
              <h1 className="text-2xl font-bold text-center mb-2">
                A description form
              </h1>

              {/* Food name stays full-width */}
              <fieldset className="fieldset">
                <legend className="fieldset-legend w-full">
                  <span className="block w-full text-center text-base md:text-lg font-semibold">
                    What is the name of the food item?
                  </span>
                </legend>
                <input
                  type="text"
                  className="input w-full"
                  placeholder="A salmon toast"
                  value={itemName}
                  onChange={(e) => setItemName(e.target.value)}
                />
              </fieldset>

              {/* Macros go into a 2-column grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <fieldset className="fieldset">
                  <legend className="fieldset-legend w-full">
                    <span className="block w-full text-center text-base md:text-lg font-semibold">
                      Protein (per 100g)
                    </span>
                  </legend>
                  <input
                    type="number"
                    className="input input-sm w-full max-w-xs mx-auto"
                    placeholder="0 to 100"
                    value={proteinPer100g}
                    onChange={(e) => setProteinPer100g(e.target.value)}
                  />
                </fieldset>

                <fieldset className="fieldset">
                  <legend className="fieldset-legend w-full">
                    <span className="block w-full text-center text-base md:text-lg font-semibold">
                      Carbohydrate (per 100g)
                    </span>
                  </legend>
                  <input
                    type="number"
                    className="input input-sm w-full max-w-xs mx-auto"
                    placeholder="0 to 100"
                    value={carbohydratePer100g}
                    onChange={(e) => setCarbohydratePer100g(e.target.value)}
                  />
                </fieldset>

                <fieldset className="fieldset">
                  <legend className="fieldset-legend w-full">
                    <span className="block w-full text-center text-base md:text-lg font-semibold">
                      Fat (per 100g)
                    </span>
                  </legend>
                  <input
                    type="number"
                    className="input input-sm w-full max-w-xs mx-auto"
                    placeholder="0 to 100"
                    value={fatPer100g}
                    onChange={(e) => setFatPer100g(e.target.value)}
                  />
                </fieldset>

                <fieldset className="fieldset">
                  <legend className="fieldset-legend w-full">
                    <span className="block w-full text-center text-base md:text-lg font-semibold">
                      Kcal (per 100g)
                    </span>
                  </legend>
                  <input
                    type="number"
                    className="input input-sm w-full max-w-xs mx-auto"
                    placeholder="e.g. 250"
                    value={kcalPer100g}
                    onChange={(e) => setKcalPer100g(e.target.value)}
                  />
                </fieldset>
              </div>

              <div className="flex justify-center mt-6">
                <button className="btn" type="submit">
                  Submit a description
                </button>
              </div>
            </form>
          </div>

          <RightList
            pageName="descriptions"
            loading={loading}
            descriptionList={descriptionList}
            fetchDescriptionList={fetchDescriptionList}
          />
        </div>
      </div>
    </div>
  );
}

export default DescriptionForm;
