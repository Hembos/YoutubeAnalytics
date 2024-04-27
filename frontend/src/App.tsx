import { Routes, Route, BrowserRouter } from "react-router-dom";
import Authorization from "./components/authorization/authorization";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="*" element={<Authorization />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
