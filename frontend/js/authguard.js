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
  console.debug('[authguard] path=', path, 'user=', user ? user.uid : null);
  // PUBLIC PAGES
  if (isPublic) {
    // If already logged in & verified, skip public pages
    if (user) {
      await user.reload();
      console.debug('[authguard] public page check after reload:', {
        uid: user.uid,
        isAnonymous: user.isAnonymous,
        emailVerified: user.emailVerified,
        providers: user.providerData.map(p=>p.providerId)
      });
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
    console.debug('[authguard] waiting page check after reload:', {
      uid: user.uid,
      isAnonymous: user.isAnonymous,
      emailVerified: user.emailVerified,
      providers: user.providerData.map(p=>p.providerId)
    });

    // Only require email verification for password accounts. Social providers typically
    // provide already-verified emails and should not be forced to waiting.
    const hasPasswordProvider = user.providerData.some(p => p.providerId === 'password');
    if (hasPasswordProvider && !user.emailVerified) {
      // keep on waiting page
      return;
    }
    // otherwise proceed to app
    window.location.replace("/pages/newdash.html");
    return; // allow waiting page for unverified users
  }

  // PROTECTED PAGES (everything else)
  if (!user) {
    window.location.replace("/pages/login.html");
    return;
  }

  await user.reload();
  console.debug('[authguard] protected page check after reload:', {
    uid: user.uid,
    isAnonymous: user.isAnonymous,
    emailVerified: user.emailVerified,
    providers: user.providerData.map(p=>p.providerId)
  });

  const hasPassword = user.providerData.some(p => p.providerId === 'password');
  if (hasPassword && !user.emailVerified) {
    // Optional: sign out, then send to waiting
    // await signOut(auth);
    console.info('[authguard] redirecting to waiting — password user not verified', user.uid);
    window.location.replace("/pages/waiting.html");
    return;
  }

  // user is logged in & verified → allow page
});
