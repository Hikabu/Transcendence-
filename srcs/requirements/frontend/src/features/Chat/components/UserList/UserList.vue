<template>
	<div class="user-list">
	<h3>Active Users</h3>
	<ul>
		<li v-for="user in activeUsers" :key="user" class="user-item">
		<span
			:class="usernameClass(user)"
			@click="showOptions(user)"
		>
			{{ user }}
		</span>
		<div v-if="selectedUser === user && user !== currentUser" class="user-options">
			<button @click="blockUser(user)">🚫 Block</button>
			<button @click="viewProfile(user)">👤 View Profile</button>
			<button @click="inviteToGame(user)">🎮 Invite to Game</button>
			<button @click="directMessage(user)">💬 Direct Message</button>
		</div>
		</li>
	</ul>
	</div>
</template>

<script>
export default {
	props: ['activeUsers', 'currentUser'],
	data() {
	return {
		selectedUser: null, // Track which user is clicked
	};
	},
	computed: {
	// Computed property to determine the class based on the user
	usernameClass() {
		return (user) => {
		return {
			'username': true, // Always apply the 'username' class
			'current-user': user === this.currentUser, // Apply 'current-user' if it's the current user
		};
		};
	}
	},
	methods: {
	showOptions(user) {
		if (user !== this.currentUser) {
		this.selectedUser = this.selectedUser === user ? null : user;
		} else {
		this.selectedUser = null;
		}
	},
	blockUser(user) {
		this.$emit('block-user', user);
		this.selectedUser = null;
	},
	viewProfile(user) {
		this.$emit('view-profile', user);
		this.selectedUser = null;
	},
	inviteToGame(user) {
		this.$emit('invite-to-game', user);
		alert(`Game invitation sent to ${user}!`);
		this.selectedUser = null;
	},
	directMessage(user) {
		this.$emit('direct-message', user);
		this.selectedUser = null;
	},
	},
};
</script>

<style scoped>
.user-list {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: flex-start;

	width: 250px;
	height: 400px;
	padding: 10px;

	font-size: 1.2rem;
	font-weight: 700;
	color: white;
	text-align: center;

	background-color: #4caf50;
	border-radius: 10px;
	box-shadow: 2px 2px 10px rgb(0 0 0 / 0.2);
}

.user-item {
	cursor: pointer;
	position: relative;
	padding: 10px;
}

.username {
	cursor: pointer;
	padding: 6px 10px;
	font-weight: 700;
	color: #ffffff;
}

.username:hover {
	text-decoration: underline;
}

.username.current-user {
	color: #ffcc00;  /* Change color for current user */
}

.user-options {
	position: absolute;
	z-index: 10;
	top: 50%;
	left: 100%;
	transform: translateY(-50%);

	display: flex;
	flex-direction: column;

	min-width: 150px;
	padding: 5px;

	background: white;
	border: 1px solid #cccccc;
	border-radius: 6px;
}

.user-options button {
	cursor: pointer;

	width: 100%;
	padding: 5px;

	text-align: left;

	background: none;
	border: none;
}

.user-options button:hover {
	background: #f0f0f0;
}
</style>
