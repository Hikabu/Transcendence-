<template>
	<div :class="messageClass">
		<strong class="username">{{ message.user }}</strong> 
		<span class="content">{{ message.content }}</span>
		<span class="timestamp">{{ message.timestamp }}</span>
	</div>
</template>

<script>
export default {
	props: ['message'],
	computed: {
		messageClass() {
			return {
				message: true,  // Base class
				'direct-message': this.message.content.startsWith('(DM'), // Highlight DMs
				'system-message': this.message.user.toLowerCase() === 'system', // Highlight system messages
			};
		}
	}
};
</script>

<style scoped>
/* General Message Styling */
.message {
	display: flex;
	flex-direction: column;

	max-width: 75%;
	margin-bottom: 10px;
	padding: 10px;

	background: #e1f5fe; /* Light blue for normal messages */
	border-radius: 8px;
}

/* Direct Messages */
.direct-message {
	background: #ffd54f; /* Yellow for direct messages */
	border-left: 5px solid #ff9800; /* Orange border for visibility */
}

/* System Messages */
.system-message {
	font-style: italic;
	color: #333333; /* Darker text for readability */
	text-align: center;

	background: #d3d3d3; /* Gray for system messages */
	border-left: none;
	border-radius: 8px;
}

/* Username Styling */
.username {
	font-weight: 700;
	color: #2c3e50;
}

/* Message Content */
.content {
	color: #34495e;
}

/* Timestamp */
.timestamp {
	align-self: flex-end;
	font-size: 0.8rem;
	color: gray;
}
</style>
