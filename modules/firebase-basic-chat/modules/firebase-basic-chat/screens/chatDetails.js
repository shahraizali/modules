import React, { useState, useEffect, useContext } from "react";
import { StyleSheet, View, Text, Image, SafeAreaView, TouchableOpacity, Dimensions, ActivityIndicator, Pressable } from "react-native";
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";
import { useSelector, useDispatch } from "react-redux";

import { FlatList, TextInput } from "react-native-gesture-handler";
import { chatDetailsRequest, sendMessageRequest } from "../api/redux";

import database from "@react-native-firebase/database";
import ProfileIcon from "../components/ProfileIcon";

import { GlobalOptionsContext, OptionsContext, getOptions } from "@options"

const ChatScreen = (params) => {
  const gOptions = useContext(GlobalOptionsContext);
  const options = useContext(OptionsContext);

  const { enableFirebase, pollingInterval } = options;
  console.log("gOptions", gOptions);
  console.log("options", options);
  
  const { navigation, route } = params;
  const { userId } = route?.params;
  const store = useSelector((state) => state.App);
  const [profileDetails, setProfileDetails] = useState({});
  const [messages, setMessages] = useState([]);
  const [triggerFB, setTriggerFB] = useState("asdad");
  const dispatch = useDispatch();
  useEffect(() => {
    console.log("store:", store);
    dispatch(chatDetailsRequest({ id: userId })).then(
      (res) => {
        setMessages(res.payload?.messages);
        setProfileDetails(res.payload?.user);
      } // end of then
    ); // end of dispatch
    const senderId = store.myProfile?.id;
    console.log("sender-----", userId, senderId);
    if (enableFirebase){
      const reference1 = database().ref("/matches/" + userId + "-" + senderId);
      const reference2 = database().ref("/matches/" + senderId + "-" + userId);
      reference1.on("value", (snapshot) => {
        console.log("snapshot reference1:", snapshot.val());
        setTriggerFB(snapshot.val());
      });
      reference2.on("value", (snapshot) => {
        console.log("snapshot reference2:", snapshot.val());
        setTriggerFB(snapshot.val());
      });
    }
  }, []);

  // setInterval(() => {
  //   dispatch(chatDetailsRequest({ id: userId })).then(
  //     (res) => {
  //       setMessages(res.payload?.messages);
  //       setProfileDetails(res.payload?.user);
  //     } // end of then
  //   ); // end of dispatch
  // }, pollingInterval);

  useEffect(() => {
    dispatch(chatDetailsRequest({ id: userId })).then(
      (res) => {
        setMessages(res.payload?.messages);
        setProfileDetails(res.payload?.user);
      } // end of then
    ); // end of dispatch
    setTimeout(
      () => {
        setLoaded(true);
      }
      , 1500);
  }, [triggerFB]);

  useEffect(() => {
    if (store.api.loading === "pending") {
      dispatch(chatDetailsRequest({ id: userId })).then(
        (res) => {
          setMessages(res.payload?.messages);
          setProfileDetails(res.payload?.user);
        } // end of then
      ); // end of dispatch
    }
    console.log("messages:", messages);
  }, [store.api.loading]);
  let flatListRef = React.useRef();
  const [loaded, setLoaded] = useState(false);
  const deviceHeight = Math.round(Dimensions.get("window").height);
  return (
    <SafeAreaView style={styles.container}>
      { !loaded &&
        <View style={{ height: deviceHeight, justifyContent: "center" }}>
          <ActivityIndicator color={"orange"} ></ActivityIndicator>
      </View>}
      <View style={styles.chatContainer}>
        <HeaderSection
          profileDetails={profileDetails}
          navigation={navigation}></HeaderSection>
        <KeyboardAwareScrollView
          resetScrollToCoords={{ x: 0, y: 0 }}
          showsVerticalScrollIndicator={false}
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={{ flex: 1 }}
        >
          <View style={{ flex: 1 }}>
            <FlatList
              reference={(ref) => { flatListRef = ref; }}
              inverted
              style={{ flex: 0.8 }}
              data={[...messages].reverse()}
              renderItem={({ item }) => (
                  item?.is_sender
                    ? <SenderMessageComponent message={item}></SenderMessageComponent>
                    : <RecieverMessageComponent message={item}></RecieverMessageComponent>
                )
              }
              keyExtractor={(item, index) => index.toString()}
              ref={flatListRef}
            />
          </View>
        </KeyboardAwareScrollView>
        <View >
            <LastSectionComponent user={profileDetails}></LastSectionComponent>
          </View>
      </View>
    </SafeAreaView>
  );
};

export default ChatScreen;

const HeaderSection = ({ profileDetails, navigation }) => {
  return (
    <View style={styles.topheader}>
      <View style={styles.headerleftSection}>
        <TouchableOpacity onPress={() => { navigation.goBack(); }}>
          <Text>&lt;Back</Text>
        </TouchableOpacity>
        <ProfileIcon
          image_src={profileDetails?.user_profile_image}
          styleContainer={styles.tinyLogoHeader}
          styleImage={{ width: 40, height: 40 }}
          styleLiveStatus={styles.styleLiveStatus}
          />
        <Text style={styles.usernameheader}>{profileDetails?.name}</Text>
      </View>
      <View style={styles.headerRightIcon}>
        <Image style={styles.phoneImage} source={require("../assets/Vector.png")}></Image>
        <Image style={styles.CameraImage} source={require("../assets/camerapicture.png")}></Image>
      </View>
    </View>
  );
};

const SenderMessageComponent = ({ message }) => {
  console.log("message", message);
  const [showTime, setShowTime] = useState(false);
  return (
    <View style={styles.senderMessageContainer}>
        <ProfileIcon
          color="green"
          image_src={message?.user_profile_image}
          styleContainer={styles.item}/>
        <Pressable style={styles.senderMessageTextContainer} onPress={()=>{
          setShowTime(!showTime);
        }}>
          <Text style={styles.senderMessageText}
          multiline={true}
          numberOfLines={3}
          round={true}
          >{message?.text}</Text>
          {
            showTime && (
              <Text style={{ 
                textAlign: "right",
                marginBottom: -25,
                paddingTop: 13,
                fontSize: 10, color: "grey", }}>{message?.created_at}</Text>
            )
          }
        </Pressable>
    </View>
  );
};

const RecieverMessageComponent = ({ message }) => {
  const [showTime, setShowTime] = useState(false);
  return (
    <View style={styles.receiverMessageContainer}>
        <Pressable style={styles.receiverMessageTextContainer}
        onPress={()=>{
          setShowTime(!showTime);
        }}>
          <Text style={styles.senderMessageText}
          multiline={true}
          numberOfLines={3}
          round={true}
          >{message?.text}</Text>
          {
            showTime && (
              <Text style={styles.messageTimeText}>{message?.created_at}</Text>
            )
          }
        </Pressable>
        <ProfileIcon
          image_src={message?.user_profile_image}
          styleContainer={styles.redlogo}
          is_live={message?.is_live}
          />
    </View>
  );
};

const LastSectionComponent = ({ user }) => {
  const [text, setText] = useState("");
  const dispatch = useDispatch();
  const sendText = () => {
    dispatch(sendMessageRequest({
      message: text,
      receiver: user?.id
    }));
    setText("");
  };
  return (
    <View style={styles.LastSection}>
      <View style={styles.Rowsection}>
        <Image style={styles.cameraIcon} source={require("../assets/cameraicon.png")}></Image>
        <View style={styles.InputSection}>
            <TextInput placeholder="Enter"
            style={styles.messageInput}
            onChangeText={text => setText(text)}
            value={text}
            ></TextInput>
            <View style={styles.LowerRightSection}>
              <Image style={styles.smileImage} source={require("../assets/smile.png")}></Image>
              <Image style={styles.MicImage} source={require("../assets/mic.png")}></Image>
            </View>
        </View>
        <TouchableOpacity onPress={() => { text && sendText(); }}>
          <Image style={styles.ArrowImage} source={require("../assets/arrowShape.png")}></Image>
        </TouchableOpacity>
      </View>
  </View>
  );
};



const styles = StyleSheet.create({
  // this stylesheet is for the top section header
  container: {
    flex: 1,
    fontSize: 20,
    padding: 5,
    textAlign: "center",
    backgroundColor: "white",
    paddingBottom: 25
  },
  chatContainer: {
    flex: 1
  },
  topheader: {
    flexDirection: "row",
    margin: 10,
    padding: 10,
    backgroundColor: "rgba(241,241,241,1)",
    borderRadius: 12,
    justifyContent: "space-between",
    alignItems: "center"
  },
  headerRightIcon: {
    flexDirection: "row",
    margin: 10

  },
  tinyLogoHeader: {
    marginLeft: 15,
    width: 40,
    height: 40
  },
  styleLiveStatus: {
    marginTop: 20,
    right: -15,
    marginRight: 10
  },
  usernameheader: {
    marginLeft: 20
  },
  headerleftSection: {
    flexDirection: "row",
    alignItems: "center"
  },
  phoneImage: {
    marginHorizontal: 7
  },
  CameraImage: {
    marginTop: 3,
    marginLeft: 3
  },
  // ---------------------------------------------------
  // sendermessagecomponent stylesheet
  senderMessageContainer: {
    flex: 1,
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginVertical: 10,
  },
  item: {
    marginLeft: 10
  },
  tinyLogo: {
    marginLeft: 10,
    width: 55,
    height: 50
  },
  tinyLogoRight: {
    width: 55,
    height: 50
  },
  senderMessageTextContainer: {
    paddingHorizontal: 15,
    paddingVertical: 10,
    backgroundColor: "rgba(252, 241, 214, 1)",
    borderRadius: 10,
    width: "75%",
    marginRight: 10,
  },
  senderMessageText: {
    fontWeight: "bold",
    padding: 10,
    color: "#284752"
  },
  // -------------------------------------
  // reciver component
  receiverMessageContainer: {
    flex: 1,
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    alignItems: "flex-end",
    marginTop: 10,
    marginBottom: 20
  },
  item2: {
    marginRight: 10
  },
  receiverMessageTextContainer: {
    paddingHorizontal: 15,
    paddingVertical: 10,
    backgroundColor: "mistyrose",
    borderRadius: 10,
    width: "70%",
    marginLeft: 10,
    fontWeight: "bold"
  },
  redlogo: {
    marginRight: 20
  },
  // ---------------------------------------

  // lastsectioncomponent

  Rowsection: {
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    paddingHorizontal: 10
  },
  InputSection: {
    backgroundColor: "rgba(241, 241, 241, 1)",
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 10,
    width: "75%"
  },
  smileImage: {
    marginHorizontal: 7
  },
  MicImage: {
    marginTop: 3,
    marginLeft: 3
  },
  LowerRightSection: {
    flexDirection: "row",
    margin: 8,
    position: "absolute",
    right: 0
  },
  cameraIcon: {
  },
  ArrowImage: {
    // marginLeft:15,
  },
  LastSection: {
    borderTopWidth: 1,
    paddingTop: 10,
    borderTopColor: "rgba(241, 241, 241, 1)"
  },
  messageInput: {
    paddingHorizontal: 10,
    paddingVertical: 14,
    backgroundColor: "rgba(241, 241, 241, 1)",
    borderRadius: 10,
    marginRight: 50
  },
  messageTimeText: { 
    textAlign: "right",
    marginBottom: -25,
    paddingTop: 13,
    fontSize: 10, color: "grey", 
  }
});
