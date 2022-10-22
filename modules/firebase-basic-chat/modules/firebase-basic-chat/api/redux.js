import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { api } from "./api";
import { mapErrorMessage, parseDjangoError } from "./errorMessage";


export const chatListRequest = createAsyncThunk(
  "chat/chatListRequest",
  async (payload) => {
    const response = await api.apiChatListRequest(payload);
    return response.data;
  }
);

export const getMatchesRequest = createAsyncThunk(
  "user/getMatchesRequest",
  async (payload) => {
    const response = await api.apiGetMatchesRequest(payload);
    return response.data;
  }
);

export const chatDetailsRequest = createAsyncThunk(
  "chat/chatDetailsRequest",
  async (payload) => {
    const response = await api.apiChatDetailsRequest(payload);
    return response.data;
  }
);

export const sendMessageRequest = createAsyncThunk(
  "chat/sendMessageRequest",
  async (payload) => {
    const response = await api.apiSendMessageRequest(payload);
    return response.data;
  }
);

const initialState = {
  token: null,
  user: {},
  api: { loading: "idle", error: null },
  chatList: [],
  chatDetails: {}
};

export const slice = createSlice({
  name: "App",
  initialState: initialState,
  reducers: {
    setToken: (state, action) => {
      state.token = action.payload;
    },
    getToken: (state) => {
      return state.token;
    }

  },
  extraReducers: {
    [chatListRequest.pending]: (state) => {
      if (state.api.loading === "idle") {
        console.log("chatListRequest.pending");
        state.api.loading = "pending";
        state.api.error = null;
      }
    },
    [chatListRequest.fulfilled]: (state, action) => {
      console.log("fulfilled action", action, "state", state);
      if (state.api.loading === "pending") {
        console.log("chatListRequest.fulfilled");
        state.chatList = action.payload;
        state.api.loading = "idle";
      }
    },
    [chatListRequest.rejected]: (state, action) => {
      console.log("chatListRequest.rejected");
      if (state.api.loading === "pending") {
        console.log(action.error);
        state.api.error = action.error;
        state.api.loading = "idle";
      }
    },
    [chatDetailsRequest.pending]: (state) => {
      if (state.api.loading === "idle") {
        console.log("chatDetailsRequest.pending");
        state.api.loading = "pending";
        state.api.error = null;
      }
    },
    [chatDetailsRequest.fulfilled]: (state, action) => {
      console.log("fulfilled action", action, "state", state);
      if (state.api.loading === "pending") {
        console.log("chatDetailsRequest.fulfilled");
        state.chatDetails = action.payload;
        state.api.loading = "idle";
      }
    },
    [chatDetailsRequest.rejected]: (state, action) => {
      console.log("chatDetailsRequest.rejected");
      if (state.api.loading === "pending") {
        console.log(action.error);
        state.api.error = action.error;
        state.api.loading = "idle";
      }
    },
    [sendMessageRequest.pending]: (state) => {
      if (state.api.loading === "idle") {
        console.log("sendMessageRequest.pending");
        state.api.loading = "pending";
        state.api.error = null;
      }
    },
    [sendMessageRequest.fulfilled]: (state, action) => {
      console.log("fulfilled action", action, "state", state);
      if (state.api.loading === "pending") {
        console.log("sendMessageRequest.fulfilled");
        state.api.loading = "idle";
      }
    },
    [sendMessageRequest.rejected]: (state, action) => {
      console.log("sendMessageRequest.rejected");
      if (state.api.loading === "pending") {
        console.log(action.error);
        state.api.error = action.error;
        state.api.loading = "idle";
      }
    }
  }
});

export const { setToken } = slice.actions;
