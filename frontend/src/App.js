import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const statesAndCities = {
  AK: ["Anchorage"],
  AL: ["Birmingham", "Dothan", "Florence", "Mobile", "Montgomery"],
  AR: ["Fayetteville", "FortSmith", "HotSprings", "LittleRock"],
  AZ: ["Flagstaff", "LakeHavasuCity", "Phoenix", "PrescottValley", "SierraVista", "Tucson"],
  CA: ["Bakersfield", "Chico", "Fresno", "LosAngeles", "Modesto", "Oxnard", "Redding", "Riverside", "Sacramento", "Salinas", "SanDiego", "SanFrancisco", "SanJose", "SantaCruz", "SantaMaria", "SantaRosa", "Stockton", "Visalia"],
  CO: ["Boulder", "ColoradoSprings", "Denver", "FortCollins", "GrandJunction", "Greeley", "Pueblo"],
  CT: ["Bridgeport", "Hartford", "NewHaven"],
  DC: ["Washington"],
  DE: ["Dover"],
  FL: ["CapeCoral", "Crestview", "Deltona", "FortLauderdale", "FortMyers", "Gainesville", "HomosassaSprings", "Jacksonville", "Lakeland", "Miami", "Naples", "Ocala", "Orlando", "PalmBay", "PanamaCity", "Pensacola", "PortSt.Lucie", "PuntaGorda", "Sebastian", "Sebring", "Tallahassee", "Tampa"],
  GA: ["Athens", "Atlanta", "Augusta", "Columbus", "Macon", "Savannah", "Valdosta", "WarnerRobins"],
  HI: ["Hilo", "Honolulu", "Kahului"],
  IA: ["CedarRapids", "Davenport", "DesMoines", "IowaCity", "Waterloo"],
  ID: ["BoiseCity"],
  IL: ["Bloomington", "Champaign", "Chicago", "Decatur", "Peoria", "Rockford", "Springfield"],
  IN: ["Bloomington", "Elkhart", "Evansville", "FortWayne", "Indianapolis", "Kokomo", "Lafayette", "Muncie", "SouthBend", "TerreHaute"],
  KS: ["KansasCity", "Topeka", "Wichita"],
  KY: ["Elizabethtown", "Lexington", "Louisville"],
  LA: ["BatonRouge", "Lafayette", "LakeCharles", "NewOrleans", "Shreveport"],
  MA: ["Boston", "Springfield", "Worcester"],
  MD: ["Baltimore", "Hagerstown", "Salisbury"],
  ME: ["Portland"],
  MI: ["Adrian", "AnnArbor", "Detroit", "Flint", "GrandRapids", "Kalamazoo", "Lansing", "Muskegon", "Saginaw"],
  MN: ["Duluth", "Mankato", "Minneapolis", "Rochester", "St.Cloud"],
  MO: ["Columbia", "JeffersonCity", "KansasCity", "Springfield", "St.Louis"],
  MS: ["Gulfport", "Jackson"],
  MT: ["Billings", "Bozeman", "Kalispell"],
  NC: ["Asheville", "Charlotte", "Durham", "Greensboro", "Greenville", "Hickory", "Raleigh", "Wilmington", "Winston"],
  ND: ["Fargo"],
  NE: ["Lincoln", "Omaha"],
  NH: ["Manchester"],
  NJ: ["AtlanticCity", "OceanCity", "Vineland"],
  NM: ["Albuquerque"],
  NV: ["LasVegas", "Reno"],
  NY: ["Albany", "Buffalo", "NewYork", "Rochester", "Syracuse"],
  OH: ["Akron", "Canton", "Cincinnati", "Cleveland", "Columbus", "Dayton", "Toledo", "Youngstown"],
  OK: ["OklahomaCity", "Tulsa"],
  OR: ["Bend", "Eugene", "Medford", "Portland", "Salem"],
  PA: ["Allentown", "Chambersburg", "Erie", "Harrisburg", "Philadelphia", "Pittsburgh", "Pottsville", "Reading"],
  RI: ["Providence"],
  SC: ["Charleston", "Columbia", "Greenville", "Spartanburg"],
  SD: ["RapidCity"],
  TN: ["Chattanooga", "Jackson", "Knoxville", "Memphis", "Nashville", "Tullahoma"],
  TX: ["Abilene", "Amarillo", "Austin", "CorpusChristi", "Dallas", "ElPaso", "FortWorth", "Houston", "Killeen", "Lubbock", "McAllen", "SanAntonio", "Sherman"],
  UT: ["Ogden", "Provo", "SaltLakeCity", "St.George"],
  VA: ["Charlottesville", "Lynchburg", "Norfolk", "Richmond", "Roanoke", "VirginiaBeach"],
  VT: ["Burlington"],
  WA: ["Bellingham", "Seattle", "Spokane", "Tacoma", "Vancouver"],
  WI: ["Appleton", "GreenBay", "Madison", "Milwaukee"],
  WV: ["Charleston", "Huntington"],
  WY: ["Cheyenne", "Laramie"]
};

function App() {
  const [selectedState, setSelectedState] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [monthsAhead, setMonthsAhead] = useState(1);
  const [analysisField, setAnalysisField] = useState('adj_value');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError('');
      const response = await axios.post('http://localhost:8000/api/predict/', {
        state: selectedState,
        city: selectedCity,
        months_ahead: monthsAhead,
        analysis_field: analysisField,
      });
      setResults(response.data);
    } catch (error) {
      console.error("There was an error predicting the prices!", error);
      setError('There was an error predicting the prices.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Housing Price Predictor</h1>
      </header>
      <main className="App-main">
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="state">State:</label>
            <select id="state" value={selectedState} onChange={(e) => setSelectedState(e.target.value)}>
              <option value="">Select a state</option>
              {Object.keys(statesAndCities).map((state) => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="city">City:</label>
            <select id="city" value={selectedCity} onChange={(e) => setSelectedCity(e.target.value)} disabled={!selectedState}>
              <option value="">Select a city</option>
              {selectedState && statesAndCities[selectedState].map((city) => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="monthsAhead">Months Ahead:</label>
            <input type="number" id="monthsAhead" value={monthsAhead} onChange={(e) => setMonthsAhead(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="analysisField">Analysis Field:</label>
            <select id="analysisField" value={analysisField} onChange={(e) => setAnalysisField(e.target.value)}>
              <option value="adj_value">Adjusted Value</option>
              <option value="adj_price">Adjusted Price</option>
              <option value="price">Price</option>
            </select>
          </div>
          <button type="submit" className="submit-button">Predict</button>
        </form>
        {error && <p className="error">{error}</p>}
        {results && (
          <div className="results">
            <h2>Prediction Results</h2>
            <p>Predicted {analysisField}: {parseFloat(results.future_prices[results.future_prices.length - 1]).toFixed(2)}</p>
            <p>Model Accuracy: {parseFloat(results.accuracy).toFixed(2)}</p>
            <h2>Descriptive Analysis</h2>
            <img id="image" src={`data:image/png;base64,${results.over_time.plot1}`} alt="Over Time Plot" />
            <img id="image" src={`data:image/png;base64,${results.analysis.plot}`} alt="Analysis Plot" />
            <h3>Histogram Statistics</h3>
            <pre>{JSON.stringify(results.analysis.description, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

