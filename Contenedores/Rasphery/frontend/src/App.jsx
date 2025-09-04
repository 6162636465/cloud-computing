import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`${API}/todos`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        setTodos(await r.json());
      } catch (e) {
        console.error("Error cargando /todos:", e);
      }
    })();
  }, []);

  const add = async () => {
    if (!title.trim()) return;
    try {
      await fetch(`${API}/todos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, done: false }),
      });
      setTitle("");
      const r = await fetch(`${API}/todos`);
      setTodos(await r.json());
    } catch (e) {
      console.error("Error creando todo:", e);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "system-ui" }}>
      <h1>To-Do</h1>
      <p style={{ marginTop: "-0.5rem", color: "#555" }}>
        API: <code>{API}</code>
      </p>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Nueva tarea…"
          style={{ flex: 1 }}
        />
        <button onClick={add}>Agregar</button>
      </div>
      <ul>
        {todos.map((t) => (
          <li key={t.id}>{t.title} {t.done ? " " : ""}</li>
        ))}
      </ul>
    </div>
  );
}