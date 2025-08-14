import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './HomePage.css'; // 👈 Add this line

function HomePage() {
    const [prisms, setPrisms] = useState([]);
    const [selectedPrism, setSelectedPrism] = useState('');
    const [refreshKey, setRefreshKey] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://localhost:8000/api/prisms/list/')
            .then(res => {
                const uniquePrisms = [];
                const names = new Set();
                res.data.forEach(p => {
                    if (!names.has(p.prism_name)) {
                        names.add(p.prism_name);
                        uniquePrisms.push(p);
                    }
                });
                setPrisms(uniquePrisms);
            })
            .catch(console.error);
    }, [refreshKey]);

    const handleNext = () => {
        if (selectedPrism) {
            navigate(`/prism/${selectedPrism}`);
        }
    };

    const handleInstallPlugin = async () => {
        const github_url = prompt("Enter raw GitHub plugin URL (e.g., compute_cone.py):");
        if (!github_url) return;

        try {
            await axios.post('http://localhost:8000/api/prisms/install_plugin/', { github_url });
            alert("✅ Plugin installed successfully!");
            setRefreshKey(prev => prev + 1);
        } catch (err) {
            console.error("❌ Plugin install failed", err);
            alert("Plugin installation failed.");
        }
    };

    return (
        <div className="home-container">
            <h1 className="home-title">🧊 Prism Viewer</h1>

            <select
                className="home-select"
                onChange={(e) => setSelectedPrism(e.target.value)}
                value={selectedPrism}
            >
                <option value="">-- Choose Prism Type --</option>
                {prisms.map(p => (
                    <option key={p.prism_name} value={p.prism_name}>
                        {p.prism_name}
                    </option>
                ))}
            </select>

            <div className="home-button-row">
                <button
                    className="btn next-btn"
                    onClick={handleNext}
                    disabled={!selectedPrism}
                >
                    Next
                </button>

                <button
                    className="btn install-btn"
                    onClick={handleInstallPlugin}
                >
                    ➕ Install Plugin
                </button>
            </div>
        </div>
    );
}

export default HomePage;
