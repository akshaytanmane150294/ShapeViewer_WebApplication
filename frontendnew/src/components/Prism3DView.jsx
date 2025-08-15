import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

function PrismMesh({ data }) {
    const meshRef = useRef();

    useFrame(() => {
        if (meshRef.current) {
            meshRef.current.rotation.y += 0.01;
        }
    });

    if (!data || !data.prism_name) return null;

    debugger;
    const type = data.prism_name.toLowerCase();
    let geometry = null;

    switch (type) {
        case 'rectangular':
            geometry = <boxGeometry args={[data.length, data.height, data.width]} />;
            break;
        case 'cylinder':
            geometry = <cylinderGeometry args={[data.radius, data.radius, data.height, 64]} />;
            break;
        case 'cone':
            geometry = <coneGeometry args={[data.radius, data.height, 64]} />;
            break;

        case 'triangular':
            // 3-sided prism
            geometry = <cylinderGeometry args={[data.radius, data.radius, data.height, 3]} />;
            break;

        case 'pentagonal':
            // 5-sided prism
            geometry = <cylinderGeometry args={[data.radius, data.radius, data.height, 5]} />;
            break;

        case 'hexagonal':
            // 6-sided prism
            geometry = <cylinderGeometry args={[data.radius, data.radius, data.height, 6]} />;
            break;
        default:
            console.error("Unsupported prism type:", type);
            return null;
    }

    return (
        <mesh ref={meshRef}>
            {geometry}
            <meshStandardMaterial color="#00ff00" />
        </mesh>
    );
}

function Prism3DView({ prismDesignation }) {
    const [prismData, setPrismData] = useState(null);
    debugger;
    useEffect(() => {
        if (!prismDesignation) return;

        const fetchPrismData = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/prisms/${prismDesignation}/`);
                setPrismData(response.data);
                debugger;
            } catch (error) {
                console.error('Failed to fetch prism data:', error);
            }
        };

        fetchPrismData();
    }, [prismDesignation]);

    return (
        <div style={{ width: '600px', height: '400px', margin: '20px auto', background: '#f0f0f0' }}>
            <Canvas camera={{ position: [0, 0, 200], fov: 75 }}>
                <ambientLight intensity={0.6} />
                <directionalLight position={[10, 10, 10]} intensity={1} />
                <OrbitControls />
                {prismData && <PrismMesh data={prismData} />}
            </Canvas>
        </div>
    );
}

export default Prism3DView;
