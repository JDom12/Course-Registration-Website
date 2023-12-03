import "./assets/main.css";
import { createAuth0 } from '@auth0/auth0-vue';
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(router);
app.use(
    createAuth0({
        domain: "dev-hjuwlpaz5xp5u1h0.us.auth0.com",
        clientId: "qeC8FnVMWHpVKH49wGEgPxB7BkAtezeM",
        authorizationParams: {
            redirect_uri: window.location.origin
        }
    })
);
app.mount("#app");
