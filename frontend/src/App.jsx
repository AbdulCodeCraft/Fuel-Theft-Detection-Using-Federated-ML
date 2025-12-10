import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { ShieldCheck, AlertTriangle, Activity, Server } from "lucide-react";

const App = () => {
  const [data, setData] = useState({
    level: 0,
    status: "LOADING",
    history: [],
  });
  const [loading, setLoading] = useState(true);

  // Poll the Python Server every 1 second
  useEffect(() => {
    const interval = setInterval(() => {
      fetchStatus();
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await axios.get("http://localhost:5000/status");
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error connecting to server:", error);
    }
  };

  const getStatusColor = () => {
    if (data.status === "OFFLINE")
      return "bg-slate-700 border-slate-500 opacity-50"; // <--- NEW GREY COLOR
    if (data.status === "THEFT DETECTED")
      return "bg-red-600 border-red-400 shadow-[0_0_20px_rgba(220,38,38,0.7)]";
    if (data.status === "WARNING") return "bg-yellow-600 border-yellow-400";
    return "bg-emerald-600 border-emerald-400 shadow-[0_0_20px_rgba(5,150,105,0.5)]";
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      {/* HEADER */}
      <header className="flex items-center justify-between mb-10 border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300">
            SECURE FUEL MONITOR
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Federated Machine Learning System • v1.0
          </p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-slate-800 rounded-full border border-slate-600">
          <div
            className={`w-3 h-3 rounded-full ${
              loading ? "bg-gray-500" : "bg-green-400 animate-pulse"
            }`}
          ></div>
          <span className="text-xs font-mono">
            {loading ? "CONNECTING..." : "SYSTEM ONLINE"}
          </span>
        </div>
      </header>

      {/* MAIN GRID */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* CARD 1: STATUS */}
        <div
          className={`p-6 rounded-xl border-2 transition-all duration-300 flex flex-col items-center justify-center ${getStatusColor()}`}
        >
          {data.status === "THEFT DETECTED" ? (
            <AlertTriangle size={48} className="mb-2" />
          ) : (
            <ShieldCheck size={48} className="mb-2" />
          )}
          <h2 className="text-xl font-bold tracking-wider">{data.status}</h2>
          <p className="text-xs opacity-80 mt-1">Real-time Anomaly Detection</p>
        </div>

        {/* CARD 2: CURRENT LEVEL */}
        <div className="p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-lg flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <h3 className="text-slate-400 font-semibold">Fuel Distance</h3>
            <Activity className="text-blue-400" size={20} />
          </div>
          <div className="mt-4">
            <span className="text-5xl font-mono font-bold text-white">
              {data.level}
            </span>
            <span className="text-xl text-slate-500 ml-2">cm</span>
          </div>
          <p className="text-xs text-slate-500 mt-2">
            Ultrasonic Sensor Reading
          </p>
        </div>

        {/* CARD 3: ML MODEL STATUS */}
        <div className="p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-lg flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <h3 className="text-slate-400 font-semibold">Federated Model</h3>
            <Server className="text-purple-400" size={20} />
          </div>
          <div className="mt-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs px-2 py-1 bg-purple-900 text-purple-200 rounded">
                Isolation Forest
              </span>
              <span className="text-xs px-2 py-1 bg-blue-900 text-blue-200 rounded">
                Active
              </span>
            </div>
            <p className="text-sm text-slate-300">Global Weights Updated</p>
          </div>
          <div className="w-full bg-slate-700 h-1 mt-4 rounded-full overflow-hidden">
            <div className="bg-purple-500 h-full w-2/3 animate-[pulse_2s_infinite]"></div>
          </div>
        </div>
      </div>
      {/* ... Inside the grid div ... */}

      {/* CARD 4: LIVE ACCURACY (NEW) */}
      {/* <div className="p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-lg flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <h3 className="text-slate-400 font-semibold">Model Accuracy</h3>
          <div className="text-emerald-400 animate-pulse">● Live</div>
        </div>
        <div className="mt-4">
          <span className="text-5xl font-mono font-bold text-white">
            {data.accuracy || "98.5%"}
          </span>
        </div>
        <p className="text-xs text-slate-500 mt-2">
          Validation vs Logic Ground Truth
        </p>
      </div> */}
      {/* GRAPH SECTION */}
      <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl overflow-hidden">
        <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
          <Activity size={18} /> Live Sensor Feed
        </h3>

        <div className="flex justify-center w-full overflow-x-auto">
          <LineChart
            width={800}
            height={300}
            data={data.history.map((val, idx) => ({ time: idx, val }))}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="time" hide />
            <YAxis domain={[0, 20]} stroke="#94a3b8" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#1e293b",
                borderColor: "#334155",
              }}
              itemStyle={{ color: "#60a5fa" }}
            />
            <Line
              type="monotone"
              dataKey="val"
              stroke="#60a5fa"
              strokeWidth={3}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </div>
      </div>
    </div>
  );
};

export default App;
