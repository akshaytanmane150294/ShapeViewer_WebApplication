import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import PrismDetailPage from './components/PrismDetailPage';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/prism/:prismName" element={<PrismDetailPage />} />
      </Routes>
    </Router>
  );
}

export default App;

// import React from 'react';
// import Prism3DView from './Prism3DView';

// function App() {
//   return (
//     <div className="App">
//       <h2>Prism View</h2>
//       <Prism3DView prismDesignation="L40B20H100" />
//     </div>
//   );
// }

// export default App;
