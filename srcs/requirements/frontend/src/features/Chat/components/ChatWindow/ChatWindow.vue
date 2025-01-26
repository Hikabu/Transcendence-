<template>
	<div class="chat-window">
	  <div class="messages">
		<Message v-for="msg in messages" :key="msg.id" :message="msg" />
	  </div>
	  <div class="input-area">
		<input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
		<button @click="sendMessage">Send</button>
	  </div>
	</div>
  </template>
  
  <script>
  import Message from '../Message/Message.vue';
  
  export default {
	components: { Message },
	props: {
	  messages: {
		type: Array,
		required: true,
	  },
	},
	data() {
	  return {
		newMessage: '',
	  };
	},
	methods: {
	  sendMessage() {
		if (this.newMessage.trim()) {
		  this.$emit('send-message', this.newMessage);
		  this.newMessage = '';
		}
	  },
	},
  };
  </script>
  
  <style scoped>
  .chat-window {
	display: flex;
	flex-direction: column;
	height: 100%;
  }
  
  .messages {
	flex: 1;
	overflow-y: auto;
	padding: 10px;
	background-color: #f9f9f9;
  }
  
  .input-area {
	display: flex;
	padding: 10px;
	background-color: #fff;
	border-top: 1px solid #ccc;
  }
  
  input {
	flex: 1;
	padding: 8px;
	border: 1px solid #ccc;
	border-radius: 4px;
	margin-right: 10px;
  }
  
  button {
	padding: 8px 16px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
  }
  
  button:hover {
	background-color: #0056b3;
  }
  </style>