import { useEffect, useState } from 'react';
import { ethers } from 'ethers';
import TournamentScoresABI from '../../config/TournamentScoresABI.json';

const CONTRACT_ADDRESS = "";

function ScoreManager({ playerScore }) {
    const [scores, setScores] = useState([]);

    const fetchScores = async () => {
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const contract = new ethers.Contract(CONTRACT_ADDRESS, TournamentScoresABI, provider);
        const fetchedScores = await contract.getScores();
        setScores(fetchedScores);
    };

    const addScore = async () => {
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        const contract = new ethers.Contract(CONTRACT_ADDRESS, TournamentScoresABI, signer);
        const transaction = await contract.addScore(playerScore);
        await transaction.wait();
        fetchScores();
    };

    useEffect(() => {
        fetchScores();
    }, []);

    return (
        <div>
            <button onClick={addScore}>Save Score to Blockchain</button>
            <ul>
                {scores.map((score, index) => (
                    <li key={index}>
                        Player: {score.player}, Score: {score.score}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ScoreManager;
