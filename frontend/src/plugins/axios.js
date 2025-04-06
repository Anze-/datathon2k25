// import axios
import axios from 'axios';

// create an instance of axios
const instance = axios.create({
  baseURL: 'http://localhost:8000', // replace with your server URL
  timeout: 1000000, // request timeout

});

const sendMessage = async (chatId, message) => {
  try {
    // pass the header X-Chat-Id with the chatId
    const response = await instance.post('/chat',
      {
        "userInput": message, "requestType": "q",
      },
      {
      headers: {
        'X-Chat-Id': chatId,
      },
    });
    return response.data.textResponse;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
}

export {
  sendMessage,
};
