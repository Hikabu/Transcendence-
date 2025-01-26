<template>
	<div class="message" :class="{ 'message-sent': isSentByMe }">
	  <div class="message-sender">{{ message.sender.username }}</div>
	  <div class="message-text">{{ message.text }}</div>
	  <div class="message-time">{{ formatTime(message.timestamp) }}</div>
	</div>
  </template>
  
  <script>
  export default {
	props: {
	  message: {
		type: Object,
		required: true,
	  },
	},
	computed: {
	  isSentByMe() {
		return this.message.sender.id === 1; // Replace with real user ID
	  },
	},
	methods: {
	  formatTime(timestamp) {
		return new Date(timestamp).toLocaleTimeString();
	  },
	},
  };
  </script>
  
  <style scoped>
  .message {
	margin-bottom: 10px;
	padding: 8px;
	border-radius: 8px;
	background-color: #e9ecef;
	max-width: 70%;
  }
  
  .message-sent {
	background-color: #007bff;
	color: white;
	margin-left: auto;
  }
  
  .message-sender {
	font-weight: bold;
	margin-bottom: 4px;
  }
  
  .message-text {
	margin-bottom: 4px;
  }
  
  .message-time {
	font-size: 0.8em;
	color: #666;
	text-align: right;
  }
  
  .message-sent .message-time {
	color: #ddd;
  }
  </style>