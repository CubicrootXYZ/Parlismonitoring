<template id="page-top">
    <div id="wrapper">
        <Header></Header>
        <div id="content-wrapper" class="d-flex flex-column">
            <!-- Topbar -->
            <nav class="navbar navbar-expand navbar-light bg-white topbar static-top shadow">
                <!-- Sidebar Toggle (Topbar) -->
                <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
                    <i class="fa fa-bars"></i>
                </button>
                <!-- Topbar Navbar -->
                <ul class="navbar-nav ml-auto">

                </ul>
            </nav>
            <!-- End of Topbar -->

            <div id="content">
                <router class="container-fluid"></router>
                <Footer></Footer>
            </div>
        </div>
    </div>
</template>

<style>
  @import './assets/styles/sb-admin.css';
  @import './assets/styles/main.css';
  @import './assets/fontawesome-free/css/all.min.css';
</style>


<script>
window.$ = window.jQuery = require('jquery');

import Router from "./Router";
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'Parlismonitoring',
  components: {
    Router,
    Header,
    Footer
  },
  methods: {
    goTo(route) {
      window.location = route;
    }
  },
  mounted() {
    let externalScript = document.createElement('script')
    externalScript.setAttribute('src', '/js/sb-admin-2.js')
    document.head.appendChild(externalScript)
  }
};
</script>