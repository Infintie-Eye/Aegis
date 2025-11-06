// /frontend/js/routeGuard.js
import { auth } from "./firebase.js";
import {
  onAuthStateChanged,
  signOut
} from "https://www.gstatic.com/firebasejs/11.0.0/firebase-auth.js";

const path = window.location.pathname.toLowerCase();

// Define routes
const publicPaths = ["/", "/index.html", "/pages/login.html", "/pages/sign_up.html"];
const isPublic = publicPaths.includes(path);
const isWaiting = path.endsWith("/pages/waiting.html") || path.endsWith("/waiting.html");

// Main guard
onAuthStateChanged(auth, async (user) => {
  // PUBLIC PAGES
  if (isPublic) {
    // If already logged in & verified, skip public pages
    if (user) {
      await user.reload();
      if (user.emailVerified) {
        window.location.replace("/pages/newdash.html");
      }
    }
    return; // allow public page
  }

  // WAITING PAGE (must be logged in; can be unverified)
  if (isWaiting) {
    if (!user) {
      window.location.replace("/pages/sign_up.html");
      return;
    }
    await user.reload();
    if (user.emailVerified) {
      window.location.replace("/pages/newdash.html");
    }
    return; // allow waiting page for unverified users
  }

  // PROTECTED PAGES (everything else)
  if (!user) {
    window.location.replace("/pages/login.html");
    return;
  }

  await user.reload();
  if (!user.emailVerified) {
    // Optional: sign out, then send to waiting
    // await signOut(auth);
    window.location.replace("/pages/waiting.html");
    return;
  }

  // user is logged in & verified → allow page
});
