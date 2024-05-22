import { Routes, Route, BrowserRouter } from "react-router-dom";
import Authorization from "./components/authorization/authorization";
import { useContext, useEffect } from "react";
import { Context } from ".";
import { observer } from "mobx-react-lite";
import Header from "./components/header/Header";
import Profile from "./components/profile/Profile";

function App() {
  const { store } = useContext(Context);

  useEffect(() => {
    if (localStorage.getItem("token")) {
      store.checkAuth();
    }
  }, []);

  if (store.isLoading) {
    <div>Загрузка...</div>;
  }

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={store.isAuth ? <Header /> : <Authorization />}
          />
          <Route
            path="/profile"
            element={
              store.isAuth ? (
                <div>
                  <Header />
                  <Profile />
                </div>
              ) : (
                <Authorization />
              )
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default observer(App);
