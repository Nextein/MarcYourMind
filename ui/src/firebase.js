// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCOhoKYFD3zJ6tnrJ0anuf-OmYZZFV2qYA",
  authDomain: "marcyourmind-01.firebaseapp.com",
  projectId: "marcyourmind-01",
  storageBucket: "marcyourmind-01.appspot.com",
  messagingSenderId: "987086274814",
  appId: "1:987086274814:web:e739cbae2d3ebaebd6e5af"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export {
    app
};