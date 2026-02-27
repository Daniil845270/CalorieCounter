import { useNavigate } from "react-router-dom";

function Header({ pageName }) {
  const navigate = useNavigate();

  return (
    <div className="mb-8">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
        {pageName === "home" && (
          <div>
            <h1 className="text-4xl font-bold">Welcome to my application!</h1>
            <p className="text-sm opacity-70 mt-1">
              Welcome to my application!
            </p>
          </div>
        )}
        {pageName === "descriptions" && (
          <div>
            <h1 className="text-4xl font-bold">Food descriptions</h1>
            <p className="text-sm opacity-70 mt-1">
              Add new foods on the left. Browse saved items on the right.
            </p>
          </div>
        )}
        {pageName === "entries" && (
          <div>
            <h1 className="text-4xl font-bold">Food items</h1>
            <p className="text-sm opacity-70 mt-1">
              Add new foods on the left. Browse saved items on the right.
            </p>
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          {pageName === "home" && (
            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  navigate("/entry");
                }}
              >
                Entries page
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  navigate("/description");
                }}
              >
                Descriptions page
              </button>
            </div>
          )}

          {pageName === "descriptions" && (
            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => {
                  navigate("/");
                }}
              >
                Home page
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  navigate("/entry");
                }}
              >
                Entries page
              </button>
            </div>
          )}

          {pageName === "entries" && (
            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => {
                  navigate("/");
                }}
              >
                Home page
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  navigate("/description");
                }}
              >
                Descriptions page
              </button>
            </div>
          )}

          <button
            type="button"
            className="btn"
            onClick={() => {
              localStorage.clear();
              navigate("/login");
            }}
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default Header;
