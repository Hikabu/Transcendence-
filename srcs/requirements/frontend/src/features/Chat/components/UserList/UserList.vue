<template>
	<div class="user-list">
	  <h3>Online Users</h3>
	  <ul>
		<li v-for="user in onlineUsers" :key="user.id">
		  <div class="user-info">
			<span>{{ user.username }}</span>
			<div class="user-actions">
			  <button @click="blockUser(user.id)" class="block-button">Block</button>
			  <button @click="inviteToPlay(user.id)" class="invite-button">Invite to Play</button>
			</div>
		  </div>
		</li>
	  </ul>
	</div>
  </template>
  
  <script>
  export default {
	props: {
	  onlineUsers: {
		type: Array,
		required: true,
	  },
	},
	methods: {
	  blockUser(userId) {
		this.$emit('block-user', userId);
	  },
	  inviteToPlay(userId) {
		this.$emit('invite-to-play', userId);
	  },
	},
  };
  </script>
  
  <style scoped>
  .user-list {
	padding: 10px;
	border-left: 1px solid #ccc;
	background-color: #f9f9f9;
	height: 100%;
  }
  
  h3 {
	margin-bottom: 10px;
  }
  
  ul {
	list-style: none;
	padding: 0;
  }
  
  li {
	margin-bottom: 10px;
	padding: 8px;
	background-color: #fff;
	border-radius: 4px;
	border: 1px solid #ddd;
  }
  
  .user-info {
	display: flex;
	justify-content: space-between;
	align-items: center;
  }
  
  .user-actions {
	display: flex;
	gap: 8px;
  }
  
  button {
	padding: 4px 8px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
  }
  
  .block-button {
	background-color: #dc3545;
	color: white;
  }
  
  .block-button:hover {
	background-color: #c82333;
  }
  
  .invite-button {
	background-color: #28a745;
	color: white;
  }
  
  .invite-button:hover {
	background-color: #218838;
  }
  </style>