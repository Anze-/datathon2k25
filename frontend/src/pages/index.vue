<template>
  <!-- create a sidebar containing the list of active chat, with a button to create a new chat.
    The rest of the screen should be occupied by a Chat component. Each chat is identified by a unique id -->
  <!-- <v-app-bar app> -->
  <!--   <v-toolbar-title>Chat Application</v-toolbar-title> -->
  <!-- </v-app-bar> -->
  <v-navigation-drawer app permanent>
    <v-list>
      <v-list-item @click="createNewChat" prepend-icon="mdi-plus">
        <v-list-item-title>Create New Chat</v-list-item-title>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list>
      <v-list-item v-for="chat in chats" :key="chat.id" @click="openChat(chat.id)" :active="selectedChat === chat.id">
        <v-list-item-title>{{ chat.name }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
  <div class="fill-height d-flex flex-row justify-center fill-width">
    <Chat :chatId="selectedChat" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Chat from '@/components/Chat.vue';

const chats = ref([
  { id: 1, name: 'Chat 1' },
  { id: 2, name: 'Chat 2' },
  { id: 3, name: 'Chat 3' },
]);

const selectedChat = ref(null);

const createNewChat = () => {
  const newChat = {
    id: Date.now(),
    name: `Chat ${chats.value.length + 1}`,
  };
  chats.value.push(newChat);
  selectedChat.value = newChat.id;
};

const openChat = (chatId) => {
  selectedChat.value = chatId;
};

</script>
