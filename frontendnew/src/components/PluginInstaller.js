// PluginInstaller.js
import React, { useState } from 'react';
import axios from 'axios';

const PluginInstaller = ({ onInstalled }) => {
    const [url, setUrl] = useState('');
    const [status, setStatus] = useState('');

    const handleInstall = () => {
        axios.post('http://localhost:8000/prisms/install_plugin/', { url })
            .then(_ => {
                setStatus('✅ Plugin installed!');
                if (onInstalled) onInstalled();  // <- This will trigger parent to refresh list
            })
            .catch(_ => setStatus('❌ Installation failed.'));
    };

    return (
        <div>
            <h3>Install Plugin</h3>
            <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="GitHub URL"
            />
            <button onClick={handleInstall}>Install</button>
            <p>{status}</p>
        </div>
    );
};

export default PluginInstaller;
