<template>
    <PermanentError v-if="apiSuccess == false" :message="errorMessage"></PermanentError>

    <h2>
        Wörter-Statistik
    </h2>

    <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8 mb-4">

            <div class="card">
                <div class="head pointer" @click="toggleSearch">
                    Suche <span style="float: right;"><i v-if="searchCollapsed == true" class="pointer fas fa-chevron-right" @click="toggleSearch"></i> <i v-if="searchCollapsed == false" class="pointer fas fa-chevron-down" @click="toggleSearch"></i></span>
                </div>
                <transition name="fade">
                    <div v-bind:class="{ 'body': true, 'collapsible': true, 'collapsed': searchCollapsed }" >
                        <form id="searchForm" class="row">
                            <div class="input-group mb-3 col-md-12">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon1">Wort/Wörter: </span>
                                </div>
                                <input type="text" class="form-control" placeholder="z.B.: Auto,Bahnhof,Stuttgart" v-model="searchWord">
                            </div>

                            <button v-on:click.prevent="fetchData(searchWord)" class="btn btn-success"><i class="fas fa-search-plus"></i> Hinzufügen</button>&nbsp;&nbsp;
                            <button v-on:click.prevent="resetForm" class="btn btn-danger"><i class="fas fa-trash-alt"></i> Eingabe löschen</button>

                        </form>
                        <hr>
                        <p><b>Bisherige Wörter:</b></p>
                        <div class="row">
                            <div class="col-md-12 mb-2" v-for="d in data" :key="d">
                                <p>
                                    <span class="badge badge-primary" style="font-size: 112%;">{{ d.word }}</span> <button v-on:click="removeWord(d.word)" class="btn btn-danger" style="float: right;"><i class="fas fa-trash-alt"></i> Entfernen</button>
                                </p>
                            </div>
                        </div>

                    </div>
                </transition>
            </div>

        </div>
        <div class="col-md-2"></div>

        <div class="col-md-2"></div>
        <div class="col-md-8">
            <h3 class="text-center text-primary p-4 text-bold">
                Häufigkeit der Wörter nach Datum
            </h3>
        </div>
        <div class="col-md-2"></div>
    </div>

    <div class="row shittyfix m-2" style="width: calc(100% - 0.1rem)">
        <div class="col-md-1"></div>
        <div class="col-md-10">
            <LineChart ref="chart" :data="dataLines" :labels="dataLabels" style="padding: 0.5rem; min-height: 50vh;"></LineChart>
        </div>
        <div class="col-md-1"></div>
    </div>
</template>

<script>
import PermanentError from "./components/PermanentError";
import LineChart from "./components/LineChart";

export default {
  components: {
    LineChart,
    PermanentError
  },
  data() {
    let col = [
            "#2b64d6"
        ];
    return {
      data: [],
      apiSuccess: null,
      dataLines: [],
      dataLabels: [],
      searchCollapsed: true,
      searchWord: "",
      colors: col,
      colorsLen: col.length,
      maxDate: Date.parse("1970-01-01"),
      minDate: Date.now()
    }
  },
  mounted() {
    this.fetchData("test");
    this.calcData()
  },
  methods: {
    fetchData(word) {
        if (word == "") {
            return
        }
        this.apiSuccess = null;
        fetch(this.$apiUrl + "/words/usage?word=" + word, {
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
                this.data.push({
                    "word": word,
                    "data": this.arrayToDate(response.data)
                });
                this.apiSuccess = true;
                this.searchWord = "";
                this.calcData();
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
    arrayToDate(a) {
        var a_date = [];
        for (const [key, value] of Object.entries(a)) {
            let d = Date.parse(key);
            let ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
            let mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
            let da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);
            a_date[`${da}-${mo}-${ye}`] = value;

            if (d > this.maxDate) {
                this.maxDate = d;
            }

            if (d < this.minDate) {
                this.minDate = d;
            }
        }
        return a_date;
    },
    calcData() {
        console.log("calc data");
        let lines = [];
        let labels = [];
        var self = this;
        var col = "#888"
        let i = 0;
        // eslint-disable-next-line no-unused-vars
        this.data.forEach(function (item, index) {
        let line = [];

            for (var d = new Date(self.minDate); d <= new Date(self.maxDate); d.setDate(d.getDate() + 1)) {
                let ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
                let mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
                let da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);

                if (`${da}-${mo}-${ye}` in item.data) {
                    line.push(item.data[`${da}-${mo}-${ye}`]);
                } else {
                    line.push(0);
                }
            }

        if (i < self.colors.length) {
          col = self.colors[i];
        } else {
          col = self.getRandomColor();
          self.colors.push(col);
        }
        lines.push({
            label: item.word,
            borderColor: col,
            backgroundColor: col,
            fill: false,
            data: line,
            highlightEnabled: false,
            type: "line"
        })
        i += 1;
        });

        for (var d = new Date(self.minDate); d <= new Date(self.maxDate); d.setDate(d.getDate() + 1)) {
            let ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
            let mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
            let da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);
            labels.push(`${da}-${mo}-${ye}`);
        }
        this.dataLines = lines;
        console.log(lines);
        this.dataLabels = labels;
    },
    toggleSearch() {
        if (this.searchCollapsed) {
            this.searchCollapsed = false;
        } else {
            this.searchCollapsed = true;
        }
        this.$refs.chart.updateChart(); // TODO find better solution to update the chart, bc it breaks when position is changed
    },
    removeWord(word) {
        this.data = this.data.filter(x => {
        return x.word != word})
        if (this.colors.length > this.colorsLen) {
            this.colors.pop();
        }
        this.calcData()
    },
    getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

  }
};
</script>