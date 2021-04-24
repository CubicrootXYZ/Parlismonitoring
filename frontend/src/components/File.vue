<template>

    <div class="card">
        <div class="head">
            <i class="fas fa-file-pdf"></i> {{ file.title }} <span style="float:right;" v-tooltip="'Permalink kopieren'"><i v-if="file.number != null" @click="copyLink" class="fas fa-link pointer"></i></span>
        </div>
        <div class="body row">

            <p class="col-md-12" v-if="file.word_count == null">
                <span class="badge badge-warning">Dokument (noch) nicht verschlagwortet</span>
            </p>

            <p class="col-md-6" v-if="file.publish_date != null">
                <b><i class="fas fa-calendar-alt"></i> Veröffentlicht am: </b>
                {{ file.publish_date.substring(0, 10) }}
            </p>

            <p class="col-md-6" v-if="file.number != null">
                <b><i class="fas fa-thumbtack"></i> Nummer: </b>
                {{ file.number }}
            </p>

            <p class="col-md-6" v-if="file.author != null">
                <b><i class="fas fa-user"></i> Autor: </b>
                {{ file.author }}
            </p>

            <p class="col-md-6" v-if="file.type != null">
                <b><i class="fas fa-layer-group"></i> Art: </b>
                {{ file.type }}
            </p>

            <p class="col-md-6" v-if="file.pages != null">
                <b><i class="fas fa-copy"></i> Seiten: </b>
                {{ file.pages }}
            </p>

            <p class="col-md-6" v-if="file.word_count != null && file.title_word_count != null">
                <b><i class="fas fa-font"></i> Wörter (Titel/Dokument): </b>
                {{ file.title_word_count }} / {{ file.word_count }}
            </p>

            <p class="col-md-6" v-if="file.file_size != null">
                <b><i class="fas fa-save"></i> Dateigröße: </b>
                {{ Math.round(file.file_size/1000) }} KB
            </p>

            <p class="col-md-12" v-if="file.link != null">
                <a :href="file.link" target="_blank" class="btn btn-primary">Zur Datei <i class="fas fa-chevron-circle-right"></i></a>
            </p>

        </div>
    </div>

</template>

<script>
export default {
  name: 'File',
  props: {
    file: []
  },
  methods: {
    copyLink() {
        let dummy = document.createElement("textarea");
        document.body.appendChild(dummy);
        dummy.value = this.$url + "/files/search?number=" + this.file.number;
        dummy.select();
        document.execCommand("copy");
        document.body.removeChild(dummy);
    }
  }
}
</script>