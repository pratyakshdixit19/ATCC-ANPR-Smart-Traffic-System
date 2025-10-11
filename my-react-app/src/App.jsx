import { useState } from "react";

function App() {
  // --- ANPR state
  const [plateImage, setPlateImage] = useState(null);
  const [plateResult, setPlateResult] = useState("");

  // --- ATCC state
  const [trafficImage, setTrafficImage] = useState(null);
  const [trafficResult, setTrafficResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // --- ANPR handlers
  const handlePlateChange = (e) => setPlateImage(e.target.files[0]);

  const handlePlateUpload = async () => {
    if (!plateImage) return alert("Select a plate image!");
    const formData = new FormData();
    formData.append("file", plateImage);
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload", { method: "POST", body: formData });
      const data = await res.json();
      setPlateResult(data.plate_number);
    } catch (err) {
      console.error(err);
      setPlateResult("Error detecting plate!");
    }
    setLoading(false);
  };

  // --- ATCC handlers
  const handleTrafficChange = (e) => setTrafficImage(e.target.files[0]);

  const handleTrafficUpload = async () => {
    if (!trafficImage) return alert("Select a traffic image!");
    const formData = new FormData();
    formData.append("image", trafficImage);
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/analyze_traffic", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setTrafficResult(data);
    } catch (err) {
      console.error(err);
      setTrafficResult(null);
      alert("Error analyzing traffic!");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-start min-h-screen bg-gray-100 p-8 space-y-12">
      {/* --- ANPR Section --- */}
      <div className="bg-white p-6 rounded-lg shadow w-96">
        <h1 className="text-2xl font-bold text-blue-600 mb-4">🚗 ANPR Detection</h1>
        <input type="file" accept="image/*" onChange={handlePlateChange} className="mb-4"/>
        <button onClick={handlePlateUpload} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 mb-4">
          {loading ? "Detecting..." : "Upload & Detect Plate"}
        </button>
        {plateResult && <p className="mt-2 font-semibold">Detected Plate: {plateResult}</p>}
      </div>

      {/* --- ATCC Section --- */}
      <div className="bg-white p-6 rounded-lg shadow w-96">
        <h1 className="text-2xl font-bold text-green-600 mb-4">🚦 ATCC Traffic Analysis</h1>
        <input type="file" accept="image/*" onChange={handleTrafficChange} className="mb-4"/>
        <button onClick={handleTrafficUpload} className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 mb-4">
          {loading ? "Analyzing..." : "Upload & Analyze Traffic"}
        </button>

        {trafficResult && (
          <div className="mt-2 text-gray-800">
            <h2 className="font-semibold mb-1">Vehicle Counts:</h2>
            <ul>
              {trafficResult.counts && Object.entries(trafficResult.counts).map(([vehicle, count]) => (
                <li key={vehicle}>{vehicle}: {count}</li>
              ))}
            </ul>
            <p className="mt-2 font-bold">{trafficResult.signal_status}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
