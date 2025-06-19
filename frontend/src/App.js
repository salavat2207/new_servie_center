import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ id: "", name: "", description: "", price: "", city_id: "", duration: "" });

  useEffect(() => {
    fetchProducts();
  }, []);

const fetchProducts = async () => {
  const res = await axios.get("http://localhost:8000/products");
  setProducts(res.data);
};

const handleSubmit = async (e) => {
  e.preventDefault();

  // Создаем новый объект с нужными типами
  const payload = {
    ...form,
    price: Number(form.price),
    city_id: Number(form.city_id),
    number: form.id.toString(), // если id — строка, или Number если число
  };

  try {
    await axios.post("http://localhost:8000/products/add", payload);
    setForm({ id: "", name: "", city_id: "", price: "", description: "", duration: "" });
    fetchProducts();
  } catch (error) {
    console.error("Ошибка при добавлении продукта:", error.response?.data || error.message);
  }
};

  const handleDelete = async (id) => {
    await axios.delete(`http://localhost:8000/api/products/${id}`);
    fetchProducts();
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Админка: Продукты</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        {["id", "name", "city_id", "price",  "description", "duration",].map((field) => (
          <input
            key={field}
            placeholder={field}
            value={form[field]}
            onChange={(e) => setForm({ ...form, [field]: e.target.value })}
            required
            style={{ marginRight: "1rem" }}
          />
        ))}
        <button type="submit">Добавить</button>
      </form>

      <ul>
        {products.map((p) => (
          <li key={p.id}>
            {p.name} — {p.price} ₽
            <button onClick={() => handleDelete(p.id)} style={{ marginLeft: "1rem" }}>
              Удалить
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;