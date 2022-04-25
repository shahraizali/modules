import React, { useRef, useContext, useEffect, useState } from "react"
import {
  Text,
  View,
  TouchableOpacity,
  FlatList,
  ImageBackground,
} from 'react-native'
import ActionSheet from "react-native-actionsheet"
import { pickFromCamera, pickFromGallery, uploadImage } from "./utils"
import { OptionsContext, GlobalOptionsContext } from '@options'
import VideoPlayer from 'react-native-video-controls';

const Camera = () => {
  // More info on all the options is below in the API Reference... just some common use cases shown here
  const actionSheet = useRef(null)
  const options = useContext(OptionsContext)
  const gOptions = useContext(GlobalOptionsContext)
  const [isLoading, setLoading] = useState(false)
  const ImagePickerOptions = [
    "Take Photo",
    "Record Video",
    "Choose from Gallery",
    "Cancel"
  ]
  const [data, setData] = useState([])

  const { styles, buttonText } = options

  const fetch_images = () => {
    fetch(`${gOptions.url}/modules/camera/user_wall/`)
      .then(response => response.json())
      .then(json => setData(json))
      .catch(error => console.log(error))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetch_images()
  }, [])

  const renderItem = ({ item }) => (
    <TouchableOpacity>
      {item.image ?
          <ImageBackground
          source={{ uri: `${gOptions.url}/${item.image}` }}
          style={styles.image}/>
          :
          <><VideoPlayer
            source={{uri: 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4' }}
            disableBack={true}
            paused={true}
            style={styles.image}
          /></>
      }
    </TouchableOpacity>
  )

  return (
    <View style={{ flex: 1 }}>
      <FlatList
        data={data}
        keyExtractor={item => item.created_at}
        renderItem={renderItem}
      />
      <ActionSheet
        ref={actionSheet}
        title={"Select Image"}
        options={ImagePickerOptions}
        cancelButtonIndex={3}
        onPress={async index => {
          let res
          switch (index) {
            case 0:
              res = await pickFromCamera('photo')
              res &&
                uploadImage(res, gOptions).then(() => {
                  fetch_images()
                })
              break
            case 1:
              res = await pickFromCamera('video')
              console.log('res video', res)
              res &&
                uploadVideo(res, gOptions).then(() => {
                  fetch_images()
                })
              break
            case 2:
              res = await pickFromGallery()
              res &&
                uploadImage(res, gOptions).then(() => {
                  fetch_images()
                })
              break
          }
        }}
      />
      <TouchableOpacity
        onPress={() => actionSheet.current.show()}
        style={styles.photoBtn}
      >
        <Text style={styles.photoBtnTxt}>{buttonText}</Text>
      </TouchableOpacity>
    </View>
  )
}

export default {
  title: 'Camera',
  navigator: Camera
}
