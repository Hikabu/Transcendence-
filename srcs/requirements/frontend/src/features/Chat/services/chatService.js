import axios from 'axios';

const API_URL = 'http://localhost:3000/api/chat';

// Fetch messages from the server
export const fetchMessages = async () => {
  try {
    const response = await axios.get(`${API_URL}/messages`);
    return response.data;
  } catch (error) {
    console.error('Error fetching messages:', error);
    return [];
  }
};

// Send a new message to the server
export const sendMessage = async (text) => {
  try {
    const response = await axios.post(`${API_URL}/messages`, { text });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    return null;
  }
};

// Fetch online users from the server
export const fetchOnlineUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/users`);
    return response.data;
  } catch (error) {
    console.error('Error fetching online users:', error);
    return [];
  }
};

// Block a user
export const blockUser = async (userId) => {
  try {
    await axios.post(`${API_URL}/block`, { userId });
    console.log(`User ${userId} blocked`);
  } catch (error) {
    console.error('Error blocking user:', error);
  }
};

// Invite a user to play
export const inviteToPlay = async (userId) => {
  try {
    await axios.post(`${API_URL}/invite`, { userId });
    console.log(`User ${userId} invited to play`);
  } catch (error) {
    console.error('Error inviting user:', error);
  }
};