<template>
    <div class="chat-window">
      <Message v-for="(message, index) in messages" :key="index" :message="message" />
    </div>
  </template>
  
  <script>
  import Message from '../Message/Message.vue';
  
  export default {
    components: { Message },
    props: ['messages'],
  };
  </script>
    
  <style scoped>
  .chat-window {
    overflow-y: auto;
    flex: 1;

    max-height: 70vh;
    padding: 15px;

    background: white;
    border-radius: 10px;
    box-shadow: 2px 4px 10px rgb(0 0 0 / 0.1);
  }
  </style>
  