import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, LabelList } from "recharts";

export default function MoodChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/mood-distribution")
      .then((res) => res.json())
      .then((json) => {
        const distribution = json.distribution;
        const chartData = Object.keys(distribution).map((mood) => ({
          mood,
          percentage: distribution[mood], // <-- match here
        }));
        setData(chartData);
      })
      .catch((err) => console.error("Error fetching mood distribution:", err));
  }, []);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <XAxis dataKey="mood" stroke="#fff" />
        <YAxis stroke="#fff" />
        <Tooltip />
        <Bar dataKey="percentage" barSize={25}>
          {data.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={
                entry.mood === "angry" ? "#e74c3c" :
                entry.mood === "happy" ? "#f1c40f" :
                entry.mood === "fear" ? "#27ae60" :
                entry.mood === "sad" ? "#3498db" :
                entry.mood === "disgusted" ? "#9b59b6" :
                entry.mood === "silly" ? "#95a5a6" : "#ff4d4d"
              }
            />
          ))}
          <LabelList dataKey="percentage" position="top" formatter={(val) => `${val}%`} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
