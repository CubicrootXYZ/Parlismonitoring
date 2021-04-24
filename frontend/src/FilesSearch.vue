<template>
    <PermanentError v-if="apiSuccess == false" :message="errorMessage"></PermanentError>

    <h2>Dateisuche</h2>

    <!-- SEARCH -->
    <div class="row">
        <div class="container col-md-10 mb-3">
            <div class="card">
                <div class="head pointer" @click="toggleSearch">
                    Suche <span style="float: right;"><i v-if="searchCollapsed == true" class="pointer fas fa-chevron-right" @click="toggleSearch"></i> <i v-if="searchCollapsed == false" class="pointer fas fa-chevron-down" @click="toggleSearch"></i></span>
                </div>
                <transition name="fade">
                    <div v-bind:class="{ 'body': true, 'collapsible': true, 'collapsed': searchCollapsed }" >
                        <form id="searchForm" class="row">
                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Title: </span>
                                </div>
                                <input type="text" class="form-control" placeholder="z.B.: Auto,Bahnhof,Stuttgart" v-model="searchTitle">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Inhalt: </span>
                                </div>
                                <input type="text" class="form-control" placeholder="z.B.: Grötzingen,melden,Ausland" v-model="searchContent">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Autor: </span>
                                </div>
                                <select v-model="searchAuthor" class="custom-select form-control" multiple>
                                    <option v-for="author in dataAuthors" :value="author" :key="author">{{ author }}</option>
                                </select>
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Typ: </span>
                                </div>
                                <select v-model="searchType" class="custom-select" multiple>
                                    <option v-for="type in dataTypes" :value="type" :key="type">{{ type }}</option>
                                </select>
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Start: </span>
                                </div>
                                <input type="date" class="form-control" :max="today" v-model="searchStart">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Ende: </span>
                                </div>
                                <input type="date" class="form-control" :max="today" v-model="searchEnd">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Dokumenten-Nummer: </span>
                                </div>
                                <input type="text" class="form-control" placeholder="z.B.: 16/9045,15/9883" v-model="searchNumber">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Max. Seiten: </span>
                                </div>
                                <input type="number" class="form-control" placeholder="z.B.: 14" v-model="searchPageMax">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Min. Seiten: </span>
                                </div>
                                <input type="number" class="form-control" placeholder="z.B.: 3" v-model="searchPageMin">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Max. Wörter: </span>
                                </div>
                                <input type="number" class="form-control" placeholder="z.B.: 5420" v-model="searchWordsMax">
                            </div>

                            <div class="input-group mb-3 col-md-6">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Min. Wörter: </span>
                                </div>
                                <input type="number" class="form-control" placeholder="z.B.: 50" v-model="searchWordsMin">
                            </div>
                            <div class="col-md-12">
                                <button v-on:click.prevent="fetchData" class="btn btn-primary">Suchen</button>&nbsp;&nbsp;
                                <button v-on:click.prevent="resetForm" class="btn btn-danger">Suche löschen</button>
                            </div>
                        </form>
                    </div>
                </transition>
            </div>
        </div>
    </div>

    <!-- CONTENT -->
    <div class="row">
        <div class="col-md-2"></div>
        <div class="row dark col-md-8">

            <div class="col-md-12">
                <v-pagination
                        v-model="page"
                        :pages="pagination.total_pages"
                        :range-size="1"
                        :modelValue="1"
                        active-color="#DCEDFF"
                        @update:modelValue="pageUpdate"
                />
            </div>

            <div class="col-md-12" v-if="apiSuccess == null">
                <div class="self-building-square-spinner">
                    <div class="square"></div>
                    <div class="square"></div>
                    <div class="square"></div>
                    <div class="square clear"></div>
                    <div class="square"></div>
                    <div class="square"></div>
                    <div class="square clear"></div>
                    <div class="square"></div>
                    <div class="square"></div>
                </div>
            </div>

            <div class="col-md-2" v-if="data.length < 1 && apiSuccess != false && apiSuccess != null"></div>
            <div class="col-md-8" v-if="data.length < 1 && apiSuccess != false && apiSuccess != null">
                <div class="card">
                    <div class="body">
                        <p><b>Nichts gefunden?</b></p>
                        <p>Benutze weniger restriktive Sucheinstellungen.</p>
                        <p>Es kann durchaus sein, dass ältere Dokumente nicht im System gespeichert sind oder auch, dass bei der Verschlagwortung nicht alles Wörter richtig erkannt wurden. Dokumente werden auch nicht sofort verschlagwortet.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2" v-if="data.length < 1 && apiSuccess != false && apiSuccess != null"></div>

            <div class="col-md-12 p-2" v-for="file in data" :key="file">
                <File :file="file"></File>
            </div>

            <div class="col-md-12">
                <v-pagination
                        v-model="page"
                        :pages="pagination.total_pages"
                        :range-size="2"
                        modelValue="1"
                        active-color="#DCEDFF"
                        @update:modelValue="pageUpdate"
                />
            </div>

        </div>

    </div>

</template>

<script>
import PermanentError from "./components/PermanentError";
import File from "./components/File";
import VPagination from "@hennge/vue3-pagination";
import "@hennge/vue3-pagination/dist/vue3-pagination.css";

export default {
  components: {
    PermanentError,
    File,
    VPagination
  },
  props: {
    label: { required: true, type: String },
    done: { default: false, type: Boolean }
  },
  data() {
    let today = new Date();
    return {
      data: [],
      pagination: [],
      stats: null,
      apiSuccess: null,
      errorMessage: "Fehler",
      console: console,
      searchTitle: "",
      searchContent: "",
      searchStart: new Date(new Date().setDate(new Date().getDate()-182)).toISOString().substring(0, 10),
      searchEnd: today.toISOString().substring(0, 10),
      today: today.toISOString().substring(0, 10),
      searchNumber: "",
      searchPageMax: "",
      searchPageMin: "",
      searchWordsMax: "",
      searchWordsMin: "",
      searchType: [],
      searchAuthor: [],
      dataAuthors: [],
      dataTypes: [],
      searchCollapsed: true,
      params: window.location.search
          .substring(1)
          .split("&")
          .map(v => v.split("="))
          .reduce((map, [key, value]) => map.set(key, decodeURIComponent(value)), new Map())
    }
  },
  mounted() {
    this.checkParams();
    this.fetchData(1);
    this.fetchDataAuthors();
    this.fetchDataTypes();
  },
  methods: {
    checkParams() {
        if (this.params.has("number")) {
            this.searchNumber = this.params.get("number");
            this.searchStart = "1970-01-01";
        }
    },
    fetchData(page) {
        this.data = [];
        this.apiSuccess = null;
        fetch(this.$apiUrl + "/files", {
            "method": "POST",
            "headers": {
                'Content-type': 'application/x-www-form-urlencoded'
            },
            body: 'page=' + page
            + '&title=' + this.searchTitle
            + '&content=' + this.searchContent
            + '&start=' + this.searchStart
            + '&end=' + this.searchEnd
            + '&number=' + this.searchNumber
            + '&page_max=' + this.searchPageMax
            + '&page_min=' + this.searchPageMin
            + '&words_max=' + this.searchWordsMax
            + '&words_min=' + this.searchWordsMin
            + '&author=' + this.searchAuthor.join(",")
            + '&type=' + this.searchType.join(",")
        })
        .then(response => {
            if(response.ok){
                return response.json()
            } else{
                throw new Error("API response not okay.")
            }
        })
        .then(response => {
            if (response.status == "success") {
                console.log(response);
                this.data = response.data;
                this.pagination = response.pagination
                this.apiSuccess = true;
            } else {
                this.errorMessage = "Fehler: Fehlerhafte Antwort von der API erhalten. Sollte dieses Problem in 15 Minuten weiterhin bestehen bitte dem Administrator bescheid geben.";
                this.apiSuccess = false;
            }
        })
        .catch(err => {
            this.errorMessage = "Fehler: API-Daten nicht verfügbar. Sollte dieses Problem in 15 Minuten weiterhin bestehen bitte dem Administrator bescheid geben.";
            this.apiSuccess = false;
            console.log(err);
        });
    },
    pageUpdate(page) {
        this.fetchData(page);
    },
    search() {
        console.log(this.searchTitle);
    },
    fetchDataAuthors() {
        this.data = [];
        this.apiSuccess = null;
        fetch(this.$apiUrl + "/authors", {
            "method": "GET",
            "headers": {
                'Content-type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if(response.ok){
                return response.json()
            } else{
                throw new Error("API response not okay.")
            }
        })
        .then(response => {
            if (response.status == "success") {
                console.log(response);
                this.dataAuthors = response.data;
                this.apiSuccess = true;
            } else {
                this.errorMessage = "Fehler: Fehlerhafte Antwort von der API erhalten. Sollte dieses Problem in 15 Minuten weiterhin bestehen bitte dem Administrator bescheid geben.";
                this.apiSuccess = false;
            }
        })
        .catch(err => {
            this.errorMessage = "Fehler: API-Daten nicht verfügbar. Sollte dieses Problem in 15 Minuten weiterhin bestehen bitte dem Administrator bescheid geben.";
            this.apiSuccess = false;
            console.log(err);
        });
    },
    fetchDataTypes() {
        this.data = [];
        this.apiSuccess = null;
        fetch(this.$apiUrl + "/types", {
            "method": "GET",
            "headers": {
                'Content-type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if(response.ok){
                return response.json()
            } else{
                throw new Error("API response not okay.")
            }
        })
        .then(response => {
            if (response.status == "success") {
                console.log(response);
                this.dataTypes = response.data;
                this.apiSuccess = true;
            } else {
                this.errorMessage = "Fehler: Fehlerhafte Antwort von der API erhalten. Sollte dieses Problem in 15 Minuten weiterhin bestehen bitte dem Administrator bescheid geben.";
                this.apiSuccess = false;
            }
        })
        .catch(err => {
            this.errorMessage = "Fehler: API-Daten nicht verfügbar. Sollte dieses Problem in 15 Minuten weiterhin bestehen bitte dem Administrator bescheid geben.";
            this.apiSuccess = false;
            console.log(err);
        });
    },
    resetForm() {
      let today = new Date();
      this.searchTitle= "";
      this.searchContent= "";
      this.searchStart= new Date(new Date().setDate(new Date().getDate()-182)).toISOString().substring(0, 10);
      this.searchEnd= today.toISOString().substring(0, 10);
      this.today= today.toISOString().substring(0, 10);
      this.searchNumber= "";
      this.searchPageMax= "";
      this.searchPageMin= "";
      this.searchWordsMax= "";
      this.searchWordsMin= "";
      this.searchType= [];
      this.searchAuthor= [];
      this.fetchData(1);
    },
    toggleSearch() {
        if (this.searchCollapsed) {
            this.searchCollapsed = false;
        } else {
            this.searchCollapsed = true;
        }
    }
  }
};
</script>