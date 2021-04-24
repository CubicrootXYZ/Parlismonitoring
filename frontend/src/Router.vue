<template>
    <component :is="routedComponent"></component>
</template>

<script>
import Index from "./Index";
import FilesSearch from "./FilesSearch";
import Faq from "./Faq";
import Error404 from "./Error404";
import WordUsage from "./WordUsage";
import Imprint from "./Imprint";

const routes = {
  "/": Index,
  "/files/search": FilesSearch,
  "/faq": Faq,
  "/words/usage": WordUsage,
  "/impressum": Imprint,
  "/imprint": Imprint,
  "/datenschutz": Imprint
};

export default {
  data() {
    return { current: window.location.pathname };
  },
  computed: {
    routedComponent() {
      if (this.current in routes) {
        return routes[this.current];
      } else {
        return Error404;
      }
    }
  }
};
</script>