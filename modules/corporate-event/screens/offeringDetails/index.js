import React from "react"
import { View, StyleSheet, ScrollView, Pressable, SafeAreaView } from "react-native"
import { Text, Image } from "react-native"

const OfferingDetails = ({ route, navigation }) => {
  navigation.setOptions({
    title: "Offerings",
    headerShown: true
  })
  const { data } = route?.params
  console.log(data)
  return (
    <SafeAreaView style={styles.container}>
    <ScrollView>
    <View style={styles.firstView}>
      <Image
        style={styles.topImageStyle}
        source={{ uri: data?.image }}
      />
    </View>

    <View style={styles.textContainer}>
      <View style={styles.descriptionContainer}>
        <Text allowFontScaling={false} style={styles.sessionTitle}>{data?.title}</Text>
        <View
          style={styles.scrollView}
          showsVerticalScrollIndicator={false}
        >
          <Text allowFontScaling={false} style={styles.descriptionStyle}>
            {data?.description}
          </Text>
        </View>
      </View>
    </View>
    </ScrollView>
  </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  descriptionStyle: {
    marginHorizontal: 35,
    textAlign: "justify",
    marginTop: 30,
    fontSize: 17,
    fontFamily: "Avenir-Regular",
    color: "#000"
  },
  descriptionContainer: { 
    flex: 1, 
    marginTop: 40, 
  },
  sideView: { 
    width: 60, 
    alignItems: "flex-start" 
  },
  textContainer: { 
    flexDirection: "row", 
    flex: 1 
  },
  firstView: { 
    marginHorizontal: 20 
  },
  sessionTitle: {
    color: "#6C170B",
    fontSize: 26,
    fontWeight: "700",
    alignSelf: "center",
    textAlign: "center",
    letterSpacing: 1
  },
  verticleTitle: { 
    color: "#6C170B", 
    fontSize: 18, 
    fontWeight: "700" 
  },
  verticleTitleView: {
    flexDirection: "column",
    transform: [{ rotate: "270deg" }],
    marginTop: 150,
    marginLeft: -90,
    padding: 10,
    width: 220
  },
  verticalText: {
    transform: [{ rotate: "180deg" }],
    fontSize: 26,
    color: "#fff",
    fontFamily: "GaramondPremrPro-It"
  },
  logoImage: {
    position: "absolute",
    width: 150,
    height: 100,
    alignSelf: "flex-start",
    opacity: 0.7,
    marginTop: 150
  },
  verticalView: {
    flexDirection: "column",
    backgroundColor: "rgba(0,0,0,0.6)",
    marginTop: 50,
    marginLeft: -70,
    width: 180,
    transform: [{ rotate: "90deg" }],
    paddingVertical: 7,
    paddingHorizontal: 30
  },
  scrollView: {
    flex: 1,
  },
  container: {
    flex: 1,
    backgroundColor: "#fff"
  },
  topImageStyle: {
    height: 250,
    width: "75%",
    position: "relative",
    alignSelf: "center",
    marginTop: 40,
    backgroundColor: "#d3d3d3"
  }
})

export default OfferingDetails