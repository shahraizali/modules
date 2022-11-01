import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import chatDetails from "../screens/chatDetails";
import Conversations from "../screens/conversations";

const Stack = createStackNavigator();

export const AppNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: true }}>
      <Stack.Screen name="Conversations" component={Conversations} options={{ headerShown: false }} />
      <Stack.Screen name="chatDetails" component={chatDetails} options={{ headerShown: false }} />
    </Stack.Navigator>
  );
};
