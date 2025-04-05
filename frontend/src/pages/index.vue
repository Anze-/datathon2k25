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
        <template v-slot:append>
          <v-btn
            icon="mdi-delete"
            variant="plain"
            size="medium"
            @click.stop="deleteChat(chat.id)"
          ></v-btn>
        </template>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
  <div class="fill-height d-flex flex-row justify-center fill-width">
    <Chat :chatId="selectedChat" />
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
import Chat from '@/components/Chat.vue';

const chats = ref([]);

const selectedChat = ref(null);
const increasingCounter = ref(0);

const createNewChat = () => {
  const newChat = {
    id: Date.now(),
    name: `Chat ${increasingCounter.value + 1}`,
  };
  increasingCounter.value++;
  chats.value.push(newChat);
  selectedChat.value = newChat.id;

};

// Load the chats from the session storage
onMounted(() => {
  createNewChat();
});

const deleteChat = (chatId) => {
  chats.value = chats.value.filter(chat => chat.id !== chatId);
  if (selectedChat.value === chatId) {
    selectedChat.value = chats.value.length > 0 ? chats.value[0].id : null;
  }
  if (chats.value.length === 0) {
    createNewChat();
  }
};

const openChat = (chatId) => {
  selectedChat.value = chatId;
};

</script>
