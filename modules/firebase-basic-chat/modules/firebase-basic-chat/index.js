import React, { useRef, useContext, useEffect, useState } from "react";
import {
  Text,
  View,
  TouchableOpacity,
  FlatList,
  ImageBackground
} from "react-native";
import { OptionsContext, GlobalOptionsContext } from "@options";
import Conversations from "./screens/conversations";
const BasicChat = () => {
  // More info on all the options is below in the API Reference... just some common use cases shown here
  const options = useContext(OptionsContext);
  const gOptions = useContext(GlobalOptionsContext);

  const { styles } = options;

  return (
    <Conversations navigation={navigation}/>
  );
};

export default {
  title: "BasicChat",
  navigator: BasicChat
};
