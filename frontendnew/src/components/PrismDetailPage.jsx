import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './PrismDetailPage.css';
import Prism3DView from './Prism3DView';

function PrismDetailPage() {
    const { prismName } = useParams();
    const [designations, setDesignations] = useState([]);
    const [selectedDesignation, setSelectedDesignation] = useState('');
    const [details, setDetails] = useState(null);
    const [show3D, setShow3D] = useState(false);

    // Get all designations for this prism type
    useEffect(() => {
        axios.get('http://localhost:8000/api/prisms/list/')
            .then(res => {
                const filtered = res.data.filter(p => p.prism_name === prismName);
                setDesignations(filtered);
                if (filtered.length > 0) setSelectedDesignation(filtered[0].designation);
            })
            .catch(console.error);
    }, [prismName]);

    // Get volume & surface area for selected designation
    useEffect(() => {
        if (!selectedDesignation) return;

        axios.get(`http://localhost:8000/api/prisms/${selectedDesignation}/compute/`)
            .then(res => setDetails(res.data))
            .catch(console.error);
    }, [selectedDesignation]);

    const handleChange = (e) => setSelectedDesignation(e.target.value);

    const open3DView = () => {
        setShow3D(true); // This will render the 3D view
    };

    return (
        <div className="detail-container">
            <h1 className="detail-title">{prismName} Designations</h1>

            <select className="detail-select" onChange={handleChange} value={selectedDesignation}>
                {designations.map(d => (
                    <option key={d.designation} value={d.designation}>
                        {d.designation}
                    </option>
                ))}
            </select>

            {details && (
                <div className="detail-stats">
                    <p>📦 Volume: {details.volume}</p>
                    <p>📐 Surface Area: {details.surface_area}</p>
                </div>
            )}

            <button className="render-button" onClick={open3DView}>
                🚀 3D Render
            </button>
            {show3D && (
                <div className="three-container">
                    <h3>🧊 3D View of {selectedDesignation}</h3>
                    <Prism3DView prismDesignation={selectedDesignation} />
                    <button onClick={() => setShow3D(false)}>❌ Close 3D View</button>
                </div>
            )}

        </div>
    );
}

export default PrismDetailPage;
