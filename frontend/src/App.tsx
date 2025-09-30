import './App.css'
import React, {useEffect, useState} from 'react';


function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/items')
    .then(response => response.json())
    .then(data => setItems(data))
    .catch(err => console.error('failed to fetch /api/items ',err));
    
  }, []);

  return (
    <>
      <h1>passwordless authentication system</h1>
      
      
      <ul>
        {items.map ((item, index) => (
          <li key={index}>{item}</li>
        ))}
      
      </ul>
      
      
    </>
  )
}

export async function getTime() {
  const r = await fetch("http://127.0.0.1:8000/time");
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json() as Promise<{ time: number }>;
}


export default App
