import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PrismDropdown = ({ onSelect }) => {
    const [prisms, setPrisms] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/prisms/list/')
            .then(res => {
                const uniqueMap = new Map();
                res.data.forEach(prism => {
                    if (!uniqueMap.has(prism.prism_name)) {
                        uniqueMap.set(prism.prism_name, prism);
                    }
                });
                setPrisms(Array.from(uniqueMap.values()));
            })
            .catch(err => console.error("Error loading prisms", err));
    }, []);

    return (
        <div>
            <h3>Select a Prism:</h3>
            <select onChange={(e) => onSelect(e.target.value)}>
                <option value="">-- Choose --</option>
                {prisms.map(prism => (
                    <option key={prism.designation} value={prism.designation}>
                        {prism.prism_name}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default PrismDropdown;
