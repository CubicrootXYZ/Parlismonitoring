<template>
    <PermanentError v-if="apiSuccess == false" :message="errorMessage"></PermanentError>

    <h1>PARLISmonitoring</h1>
    <p class="text-primary" style="text-align: center; padding: 0.75rem; padding-top: 0;">Dokumente aus dem Landtag von Baden-Württemberg aufbereitet!</p>
    <p style="text-align: center; padding: 0.5rem; padding-top: 0;">
        <a href="https://github.com/CubicrootXYZ/Parlismonitoring" class="btn btn-primary" target="_blank"><i class="fab fa-github"></i> GitHub</a>
    </p>

    <h2>Fakten</h2>

    <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8">
            <div class="card facts m-1" v-if="apiSuccess == true && typeof data.biggest_title !== 'undefined' && data.biggest_title != null">
                <div class="body">
                    <i>{{ data.biggest_title }}</i>
                </div>
                <div class="head no-border">
                    Der längste Dokumententitel mit {{ data.biggest_words_title }} Wörtern.
                </div>
            </div>
        </div>
        <div class="col-md-2"> </div>

        <div class="col-md-2"> </div>
        <div class="col-md-8">
            <div class="card facts m-1" v-if="apiSuccess == true && typeof data.smallest_title !== 'undefined' && data.smallest_title != null">
                <div class="body">
                    <i>{{ data.smallest_title }}</i>
                </div>
                <div class="head no-border">
                    Der kürzeste Dokumententitel mit {{ data.smallest_title_words }} Wörtern.
                </div>
            </div>
        </div>
        <div class="col-md-2"></div>
    </div>


    <div class="row row-border">

        <MiniCard title="Gesammelte Dateien" :value="data.files_total" icon="fa-file" v-if="apiSuccess == true && typeof data.files_total !== 'undefined' && data.files_total != null"></MiniCard>
        <MiniCard title="Verschlagwortete Dateien" :value="data.files_tagged" icon="fa-file-signature" v-if="apiSuccess == true && typeof data.files_tagged !== 'undefined' && data.files_tagged != null"></MiniCard>
        <MiniCard title="Autoren" :value="data.authors" icon="fa-user" v-if="apiSuccess == true && typeof data.authors !== 'undefined' && data.authors != null"></MiniCard>
        <MiniCard title="Verschiedene Wörter" :value="data.words" icon="fa-font" v-if="apiSuccess == true && typeof data.words !== 'undefined' && data.words != null"></MiniCard>
        <MiniCard title="Größte Datei" :value="Math.round(data.biggest_file_size / 1000) + ' KB'" icon="fa-save" v-if="apiSuccess == true && typeof data.biggest_file_size !== 'undefined' && data.biggest_file_size != null"></MiniCard>
        <MiniCard title="Durchschnittliche Datei" :value="Math.round(data.avrg_file_size / 1000) + ' KB'" icon="fa-save" v-if="apiSuccess == true && typeof data.avrg_file_size !== 'undefined' && data.avrg_file_size != null"></MiniCard>
        <MiniCard title="Durchschnittlicher Titel" :value="Math.round(data.avrg_title_words) + ' Wörter'" icon="fa-heading" v-if="apiSuccess == true && typeof data.avrg_title_words !== 'undefined' && data.avrg_title_words != null"></MiniCard>
        <MiniCard title="Durchschnittliches Dokument" :value="Math.round(data.avrg_words) + ' Wörter'" icon="fa-file-word" v-if="apiSuccess == true && typeof data.avrg_title_words !== 'undefined' && data.avrg_title_words != null"></MiniCard>

    </div>

    <h2>Warum?</h2>

    <div class="row dark">

        <div class="col-md-2"></div>
        <div class="col-md-8">
            <div class="ml-2 mr-2 mb-4 card dark">
                <div class="body">
                    Warum hat sich jemand die Mühe gemacht eine Suchmaschine für Landtagsdokumente zu bauen die es beim Landtag selbst schon gibt?<br><br>
                    - Suche nach Wörtern in den Dateien selbst<br>
                    - Statistiken
                </div>
            </div>
        </div>
        <div class="col-md-2"></div>

    </div>

</template>

<script>
import MiniCard from "./components/MiniCard";
import PermanentError from "./components/PermanentError"

export default {
  components: {
    MiniCard,
    PermanentError
  },
  props: {
    label: { required: true, type: String },
    done: { default: false, type: Boolean }
  },
  data() {
    return {
      data: [],
      stats: null,
      apiSuccess: null,
      errorMessage: "Fehler"
    }
  },
  mounted() {
    fetch(this.$apiUrl + "/stats", {
        "method": "GET",
        "headers": {
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
            this.data = response.data;
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
  }
}


</script>