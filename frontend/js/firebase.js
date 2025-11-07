// Import the Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut, signInAnonymously } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.0.0/firebase-firestore.js";

  const firebaseConfig = {
    apiKey: "AIzaSyBFb1BxuqBt-N9u5YWgroqMVuSIQjRbtEc",
    authDomain: "aegis-d1a50.firebaseapp.com",
    projectId: "aegis-d1a50",
    storageBucket: "aegis-d1a50.firebasestorage.app",
    messagingSenderId: "405698913839",
    appId: "1:405698913839:web:bf420b565e7259fb8208da",
    measurementId: "G-KZTDL9HLPR"
  };


// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
// Re-export helper auth functions for pages to use (e.g. anonymous sign-in)
export { signInAnonymously, onAuthStateChanged, signOut };
