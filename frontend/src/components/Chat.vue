<template>
  <div class="fill-height d-flex flex-column fill-width" style="max-height: 100vh">
    <div v-if="!chatId">
      No chat :(
    </div>
    <v-container v-else fluid class="fill-height justify-center" style="overflow: auto">
      <v-col cols=6 md=8 sm=10>
          <div v-for="(item, index) in messages" :key="index"
               :class="['d-flex flex-row align-center', item.from == 'user' ? 'justify-end': null, (index > 0 && messages[index-1].from != item.from) ? 'mt-8' : 'mt-2']">
            <span v-if="item.from == 'user'" class="msg blue--text bg-blue-grey-lighten-5 rounded-xl px-4 py-2 mr-3">{{ item.msg }}</span>
            <v-avatar style="align-self: start" :color="item.from == 'user' ? 'indigo': 'red'" size="36">
              <v-img
                v-if="item.from !== 'user'"
                :src="botLogo"
                height="36"
                width="36"
                />
               <span v-else class="white--text">{{ item.from[0] }}</span>
            </v-avatar>
            <span v-if="item.from != 'user'" class="msg bg-blue-grey-lighten-4 rounded-xl px-4 py-2 blue--text ml-3">{{ item.msg }}</span>
          </div>
          <div ref="scrollSentinel"></div>
        </v-col>
    </v-container>
    <v-footer fixed class="fill-width" color="transparent">
      <v-container class="py-0 px-0 mx-0 w-100 d-flex justify-center" style="max-width:100%!important;">
          <v-col cols=6 md=8 sm=10>
            <div class="d-flex flex-row align-center justify-center align-items-center justify-items-center bg-transparent">
              <v-text-field v-model="currentMessage" placeholder="Type Something" @keypress.enter="send" variant="outlined" hide-details rounded></v-text-field>
              <v-btn icon="mdi-send" variant="tonal" class="ml-4" @click="send"/>
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

const props = defineProps({
  chatId: {
    type: [Number, null],
    required: true,
  },
});

const messages = ref([]);
const currentMessage = ref('');

const resetMessages = () => {
  messages.value = [];
};

const scrollSentinel = useTemplateRef('scrollSentinel');


const loadPreviousMessages = (chatId) => {
  messages.value = [
    { id: 1, msg: `Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId} Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}`, from: 'user' },
    { id: 1, msg: `Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId} Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}`, from: 'user' },
    { id: 1, msg: `Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId} Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}`, from: 'user' },
    { id: 1, msg: `Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId} Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}`, from: 'user' },
    { id: 1, msg: `Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId} Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}`, from: 'user' },
    { id: 1, msg: `Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId} Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}`, from: 'user' },
    { id: 1, msg: `Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId} Hello sadfmasjfdlsakjdf lasdjf sdlfj asd fasdf jasd fjas dfasd fasl kjfalsk djfal skjdl kdsjf lksjdflsdkfj sldk fj dsfrom chat ${chatId}`, from: 'user' },
    { id: 2, msg: `Hello to you!`, from: 'bot' },
  ];
};

const scrollChat = () => {
  setTimeout(()=>scrollSentinel.value.scrollIntoView({ behavior: 'smooth' }), 100);
};

const addLocalMessage = (msg) => {
  messages.value.push(msg);
  scrollChat();
};

const send = () => {
  if (currentMessage.value.trim() === '') return;
  addLocalMessage({ msg: currentMessage.value, from: 'user' });
  currentMessage.value = '';
  setTimeout(() => {
    addLocalMessage({ msg: `Hello to you!`, from: 'bot' });
  }, 1000);
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
