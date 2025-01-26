import { useChatStore } from '../stores/chatStore';

// Initialize WebSocket connection
const socket = new WebSocket('ws://localhost:3000');

// Set up WebSocket event listeners
export const setupSocket = () => {
  const chatStore = useChatStore();

  // Handle incoming messages
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'chatMessage') {
      // Add the new message to the state
      chatStore.addMessage(data.message);
    } else if (data.type === 'onlineUsers') {
      // Update the list of online users
      chatStore.setOnlineUsers(data.users);
    }
  };

  // Handle connection errors
  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  // Handle connection close
  socket.onclose = () => {
    console.log('WebSocket connection closed');
  };
};

// Send a message through the WebSocket
export const sendMessage = (message) => {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: 'chatMessage', message }));
  } else {
    console.error('WebSocket is not open');
  }
};

// Export the socket for use in other components
export default socket;