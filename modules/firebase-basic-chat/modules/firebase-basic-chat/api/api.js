import axios from "axios";
import { getGlobalOptions } from "@options";
import { storage } from "@modules/storage";

const global = getGlobalOptions();
const BASE_URL = global.url; // change your BASE_URL in `options/options.js` to edit this value

const authAPI = axios.create({
  baseURL: BASE_URL,
  headers: { Accept: "application/json", "Content-Type": "application/json" }
});


async function apiChatListRequest(payload) {
  const t = await storage.getToken(); 
  return authAPI.get("/modules/firebase-basic-chat/chat_list/", {
    headers: { Authorization: `Token ${t}` }
  });
}

async function apiChatDetailsRequest(payload) {
  const t = await storage.getToken();
  return authAPI.get(`/modules/firebase-basic-chat/chat_details/${payload?.id}/`, {
    headers: { Authorization: `Token ${t}` }
  });
}

async function apiSendMessageRequest(payload) {
  const t = await storage.getToken();
  return authAPI.post("/modules/firebase-basic-chat/send_message/", payload, {
    headers: { Authorization: `Token ${t}` }
  });
}

export const api = {
  apiChatListRequest,
  apiChatDetailsRequest,
  apiSendMessageRequest,
};
