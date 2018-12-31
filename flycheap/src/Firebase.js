import * as firebase from 'firebase';
import firestore from 'firebase/firestore'

const settings = {timestampsInSnapshots: true};

const config = {
  apiKey: "AIzaSyCo2JYgMJDwHK2iLIot9qolbMNpKkAheBA",
  authDomain: "flycheap-285b7.firebaseapp.com",
  databaseURL: "https://flycheap-285b7.firebaseio.com",
  projectId: "flycheap-285b7",
  storageBucket: "flycheap-285b7.appspot.com",
  messagingSenderId: "190411101061"
};
firebase.initializeApp(config);

firebase.firestore().settings(settings);

export default firebase;
