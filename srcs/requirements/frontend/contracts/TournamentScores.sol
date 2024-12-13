// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TournamentScores {
    struct Score {
        address player;
        uint256 score;
    }

    Score[] public scores;

    event ScoreAdded(address indexed player, uint256 score);

    function addScore(uint256 _score) external {
        scores.push(Score(msg.sender, _score));
        emit ScoreAdded(msg.sender, _score);
    }

    function getScores() external view returns (Score[] memory) {
        return scores;
    }
}
