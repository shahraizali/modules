import React, { useEffect } from "react"
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  FlatList,
  Pressable,
  SafeAreaView
} from "react-native"
import { useDispatch, useSelector } from "react-redux"
import { getTeamMembers } from "../../store/custom/team.slice"

const Team = ({ navigation }) => {
  
  const { entities } = useSelector(state => state.Team.getTeamMembers)

  const dispatch = useDispatch()

  const fetchData = async () => {
    await dispatch(getTeamMembers())
  }

  useEffect(() => {
    fetchData()
  }, [])

  const renderItem = ({ item }) => {
    
    return (
      <TouchableOpacity
        style={styles.personWrapper}
        onPress={() => navigation.navigate("teamDetails", { data: item })}
      >
        <Image
          style={styles.personImage}
          source={{ uri: item?.connect_user?.image }}
        />
        <View style={{ marginLeft: 10 }}>
          <Text allowFontScaling={false} style={styles.name}>{item?.connect_user?.user?.name}</Text>
          <Text allowFontScaling={false} style={styles.post}>{item?.connect_user?.designation}</Text>
          <Text allowFontScaling={false} style={styles.post}>{item?.connect_user?.company}</Text>
        </View>
      </TouchableOpacity>
    )
  }
  return (
    <SafeAreaView style={styles.main}>
      <View>
        <View style={{ position: "relative", marginTop: 40 }}>
          <Image
            style={styles.imageWrapper}
            source={require("./assets/background.png")}
          />
          <Image
            style={styles.TextImage}
            source={require("./assets/SummitGraphic.jpg")}
            resizeMode="contain"
          />
        </View>
      </View>
      <FlatList
        data={entities?.data}
        renderItem={renderItem}
        showsVerticalScrollIndicator={false}
      />
      <Pressable style={styles.toast} onPress={()=>{navigation.goBack()}}>
        <Text allowFontScaling={false} style={styles.toastText}>TEAM</Text>
      </Pressable>
    </SafeAreaView> 
  )
}

export default Team

const styles = StyleSheet.create({
  main: {
    position: "relative",
    flex: 1,
    display: "flex",
    alignItems: "center",
    flexDirection: "column"
  },
  imageWrapper: {
    width: 250,
    height: 250
  },
  TextImage: {
    top: -30,
    left: -40,
    width: 150,
    height: 80,
    position: "absolute",
    opacity: 0.7
  },
  personWrapper: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-start",
    marginTop: 30
  },
  personImage: {
    width: 100,
    height: 100,
    backgroundColor: "#d3d3d3"
  },
  name: {
    fontSize: 17,
    color: "brown",
    fontWeight: "800"
  },
  post: {
    color: "black",
    fontSize: 15,
    fontFamily: "Avenir-Regular"
  },
  toast: {
    top: "50%",
    left: -40,
    position: "absolute",
    backgroundColor: "rgba(0,0,0,0.7)",
    transform: [{ rotate: "-90deg" }],
    width: 120,
    height: 40,
    justifyContent: "center",
    alignItems: "center"
  },
  toastText: {
    fontWeight: "800",
    color: "white",
    fontSize: 16,
    letterSpacing: 0.5,
    padding: 0,
    margin: 0
  }
})