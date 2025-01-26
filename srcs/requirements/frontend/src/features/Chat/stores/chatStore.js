import { reactive } from 'vue';

// Create a reactive state object
const state = reactive({
  messages: [], // Array of chat messages
  onlineUsers: [], // Array of online users
  currentUser: { id: 1, username: 'CurrentUser' }, // Mock current user (replace with real auth)
});

// Export functions to interact with the state
export const useChatStore = () => {
  // Add a new message to the state
  const addMessage = (message) => {
    state.messages.push(message);
  };

  // Set the list of online users
  const setOnlineUsers = (users) => {
    state.onlineUsers = users;
  };

  // Block a user (mock implementation)
  const blockUser = (userId) => {
    state.onlineUsers = state.onlineUsers.filter((user) => user.id !== userId);
    console.log(`User ${userId} blocked`);
  };

  // Invite a user to play (mock implementation)
  const inviteToPlay = (userId) => {
    console.log(`User ${userId} invited to play`);
  };

  return {
    state,
    addMessage,
    setOnlineUsers,
    blockUser,
    inviteToPlay,
  };
};