import React, { useState } from "react";
import { StyleSheet, View, Text, TextInput, Button, Alert} from "react-native";
import { TouchableOpacity } from "react-native-gesture-handler";
import { useDispatch } from "react-redux";
import { loginRequest } from "../../api/redux";
import {storage} from "../../../../utils/storage";

export const forgotPass = (props) => {
  const {navigation } = props;
  const [email, setEmail] = useState('shahraiz@cb.com');
  const [password, setPassword] = useState('Admin123');

  const dispatch = useDispatch();
  // navigation.navigate('Home')

  const doSomething = () => {
      navigation.navigate('create')
      
  };

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Forgot Password</Text>
      <Text style={styles.subText}>Enter Email address</Text>
      <TextInput
        style={styles.inputEmail}
        value={Text}
        placeholder="Email"
        onChangeText={newText => setEmail(newText)}
        defaultValue={email}
        maxLength={20}
      />
      <View style={styles.subTextContainer}>
      </View>
      {/* <Text style={styles.underText}>Remember me Forgot Password?</Text> */}
      <View style={styles.buttonContainer}>
          <TouchableOpacity style={[styles.btn]} onPress={()=>{ doSomething() }}>
            <Text style={styles.btnText}>
            Send Verification
            </Text>
          </TouchableOpacity>
      </View>
      <Text style={styles.grey}>Or</Text>
      <View style={styles.signupcontainer}>
      <Text style={styles.sign}>Dont have an account?</Text>
      <TouchableOpacity>
              <Text style={styles.sign}>
              Sign up
              </Text>
      </TouchableOpacity>
      </View>
    </View>
  )
};

const styles = StyleSheet.create({
  signupcontainer:{
    flexDirection:'row',
    textAlign: 'center',
    alignItems: 'center',
    justifyContent:'center',
  },
  sign:{
    fontSize: 18,
    fontWeight: '400',
    color: "black",
    padding: 13,
    textAlign: 'center',
  },
  grey:{
    fontSize: 13,
    fontWeight: '400',
    color: "gray",
    textAlign: 'center',
    padding: 35,
  },
  button:{
    borderRadius:10,
    padding: 10,
    backgroundColor: 'red'
  },
  btn: {
    paddingHorizontal: 40,
    paddingVertical: 10,
    backgroundColor: 'black',
    borderRadius: 10
  },
  underText:{
    fontSize: 14,
    fontWeight: '400',
    color: "black",
    padding: 13,

  },
  btnText: {
    color: 'white'
  },
  subTextContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 0,
    paddingTop: 20
  },  
  inputEmail: {
    borderRadius: 10,
    borderWidth: 1,
    height: 45,
    paddingHorizontal: 15,
    borderColor: '#C4C4C4',
    textAlign: 'center',
  },
  input: {
    borderRadius: 10,
    borderWidth: 1,
    height: 45,
    paddingHorizontal: 15,
    borderColor: '#C4C4C4'
  },
  buttonContainer: {
    alignItems: 'center',
    flex: 1,
    paddingTop: 15
  },
  subText:{
    fontSize: 14,
    padding:10,
    fontWeight: '400',
    color: "black",
    textAlign: 'center'
  },
  container: {
    flex: 1,
    height: 100,
    padding: 13,
    backgroundColor: "white"
  },
  text: {
    fontSize: 42,
    fontWeight: '700',
    color: "black",
    textAlign: 'center',
    padding:60
  },
})


