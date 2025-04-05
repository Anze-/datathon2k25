<template>
  <div class="fill-height d-flex flex-column fill-width" style="max-height: 100vh; width:100%">
    <v-container fluid :class="['fill-height full-width justify-center', messages.length > 0 ? 'align-start' : 'align-center']" style="overflow: auto">
      <v-col cols=6 md=8 sm=10 v-if="messages.length > 0">
          <div v-for="(item, index) in messages" :key="index"
               :class="['d-flex flex-row align-center', item.from == 'user' ? 'justify-end': null, (index > 0 && messages[index-1].from != item.from) ? 'mt-8' : 'mt-2']">
            <span v-if="item.from == 'user'" class="msg blue--text bg-blue-grey-lighten-5 rounded-xl px-4 py-2 mr-3">
              {{ item.loading ? 'Loading...' : item.msg }}
            </span>
            <v-avatar style="align-self: start" :color="item.from == 'user' ? 'indigo': 'red'" size="36">
              <v-img
                v-if="item.from !== 'user'"
                :src="botLogo"
                height="36"
                width="36"
                />
               <span v-else class="white--text">{{ item.from[0] }}</span>
            </v-avatar>
            <span v-if="item.from != 'user'" class="msg bg-blue-grey-lighten-4 rounded-xl px-4 py-2 blue--text ml-3">
              {{ item.loading ? 'Loading...' : item.msg }}
            </span>
          </div>
          <div ref="scrollSentinel"></div>
        </v-col>
        <v-col cols=6 md=8 sm=10 v-else>
          <div class="d-flex flex-column align-center justify-center fill-height">
            <v-avatar size="100" color="indigo">
              <v-img
                :src="botLogo"
                height="128"
                width="128"
                />
            </v-avatar>
            <h1 class="mt-4">Welcome to Gieni</h1>
            <p class="text-center">Type your message and hit enter to start chatting with Gieni.</p>
          </div>
        </v-col>
    </v-container>
    <v-footer fixed class="fill-width" color="transparent">
      <v-container class="py-0 px-0 mx-0 w-100 d-flex justify-center" style="max-width:100%!important;">
          <v-col cols=6 md=8 sm=10>
            <div class="d-flex flex-row align-center justify-center align-items-center justify-items-center bg-transparent">
              <v-text-field v-model="currentMessage" placeholder="Type Something" @keypress.enter="send" variant="outlined" hide-details rounded></v-text-field>
              <v-btn icon="mdi-send" variant="tonal" class="ml-4" @click="send" :disabled="loading"/>
            </div>
          </v-col>
      </v-container>
    </v-footer>
  </div>
</template>

<script setup>
  // Get prop chatId
import { ref, watch, onMounted, defineProps, useTemplateRef } from 'vue';

import botLogo from '@/assets/logo.jpeg';

import {sendMessage} from "@/plugins/axios";

const props = defineProps({
  chatId: {
    type: [String, null],
    required: true,
  },
});

const messages = ref([]);
const currentMessage = ref('');
const loading = ref(false);

const resetMessages = () => {
  messages.value = [];
};

const scrollSentinel = useTemplateRef('scrollSentinel');


const loadPreviousMessages = (chatId) => {
  const chats = JSON.parse(sessionStorage.getItem('chats'));
  if (chats && chats[chatId]) {
    messages.value = chats[chatId];
    scrollChat();
  } else {
    resetMessages();
  }
};
const persistMessages = () => {
  const chats = JSON.parse(sessionStorage.getItem('chats')) || {};
  chats[props.chatId] = messages.value;
  sessionStorage.setItem('chats', JSON.stringify(chats));
};

const scrollChat = () => {
    setTimeout(()=>{
    if (scrollSentinel.value)
      scrollSentinel.value.scrollIntoView({ behavior: 'smooth' })
    } , 100);
};

const addLocalMessage = (msg) => {
  messages.value.push(msg);
  scrollChat();
  persistMessages();
};

const send = () => {
  if (loading.value) return;
  if (currentMessage.value.trim() === '') return;
  addLocalMessage({ msg: currentMessage.value, from: 'user', loading: false });
  loading.value = true;
  addLocalMessage({ msg: '', from: 'bot', loading: true });
  sendMessage(props.chatId, currentMessage.value)
    .then((msg) => {
      messages.value.splice(messages.value.length - 1, 1);
      addLocalMessage({ msg: msg, from: 'bot', loading: false });
    })
    .catch((error) => {
      messages.value.splice(messages.value.length - 1, 1);
      addLocalMessage({ msg: 'Error: ' + error.message, from: 'bot', loading: false });
    }).finally(() => {
      loading.value = false;
    });
  currentMessage.value = '';
};

watch(
  () => props.chatId,
  (newChatId) => {
    resetMessages();
    loadPreviousMessages(newChatId);
    scrollChat();
  },
);
</script>

<style scoped>
.msg {
  max-width: 50%;
}
</style>
