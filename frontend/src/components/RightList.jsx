function RightList({
  pageName,
  loading,
  entriesList,
  descriptionList,
  fetchDescriptionList,
  fetchLists,
}) {
  return (
    <div className="w-full md:w-1/2">
      <div className="bg-base-100 p-6 rounded-xl shadow-xl ring-1 ring-base-300">
        {/* Header - difficult refactor */}
        <div className="flex items-start justify-between gap-4">
          <div>
            {/* For this exact line to work, the pageName must always be exactly either
             "entries" or "descriptions" strings*/}
            <h2 className="text-2xl font-bold">Saved {pageName}</h2>
            <p className="text-sm opacity-70">
              {pageName === "entries" &&
                (loading ? "Loading…" : `${entriesList.length} item(s)`)}
              {pageName === "descriptions" &&
                (loading ? "Loading…" : `${descriptionList.length} item(s)`)}
            </p>
          </div>

          <button
            type="button"
            className="btn btn-sm"
            onClick={pageName === "entries" ? fetchLists : fetchDescriptionList}
            disabled={loading}
          >
            Refresh
          </button>
        </div>

        {/* Body */}
        <div className="mt-4 max-h-[70vh] overflow-y-auto">
          {loading && <p>Loading...</p>}

          {/* no items case */}
          {!loading &&
            (pageName === "entries"
              ? entriesList.length === 0
              : descriptionList.length === 0) && (
              <div className="py-8 text-center opacity-70">
                No items yet. Add one on the left.
              </div>
            )}

          {/* the actual entries list */}
          {pageName === "entries" && !loading && entriesList.length > 0 && (
            <ul className="mt-4 space-y-3">
              {entriesList.map((d) => (
                <li
                  key={d.id}
                  className={`relative p-4 rounded-xl bg-base-100 ring-1 ring-base-300 
                    shadow-sm hover:shadow-md hover:bg-base-200 transition`}
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

          {/* the actual descriptions list */}
          {pageName === "descriptions" &&
            !loading &&
            descriptionList.length > 0 && (
              <ul className="mt-4 space-y-3">
                {descriptionList.map((d) => (
                  <li
                    key={d.id}
                    className={`relative p-4 rounded-xl bg-base-100 ring-1 ring-base-300 
                    shadow-sm hover:shadow-md hover:bg-base-200 transition`}
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

                    <div className="font-bold text-lg pr-20">{d.Item_name}</div>

                    <div className="mt-2 text-sm opacity-80 tabular-nums pr-20">
                      <span className="inline-block mr-4">
                        Protein: {d.Protein_per_100g}
                      </span>
                      <span className="inline-block mr-4">
                        Carbs: {d.Carbohydrate_per_100g}
                      </span>
                      <span className="inline-block mr-4">
                        Fat: {d.Fat_per_100g}
                      </span>
                      <span className="inline-block">
                        Kcal: {d.Kcal_per_100g}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
        </div>
      </div>
    </div>
  );
}

export default RightList;
