import os, subprocess, json


class RnnTagger:
    def __init__(self, language):
        self.lang = language
        self._init_tagger()

        if self.lang not in self.langs:
            raise TaggerError("Unknown language")

    def _init_tagger(self):
        self.langs = []

        try:
            files = os.listdir("/opt/app/RNNTagger/cmd")
        except Exception as e:
            raise TaggerError(f"Initializing failed with: {e}")

        for f in files:
            if "rnn-tagger" in f:
                self.langs.append(f.replace("rnn-tagger-", "").replace(".sh", ""))

    def _write_file(self, text):
        try:
            f = open("/opt/app/RNNTagger/test.txt", "w")
            f.write(text)
            f.close()
        except Exception as e:
            raise TaggerError(f"Failed to open file with: {e}")

    def _process(self):
        try:
            process = subprocess.Popen("/opt/app/RNNTagger/cmd/rnn-tagger-"+self.lang+".sh ./test.txt", stdout=subprocess.PIPE, shell=True)
            output, error = process.communicate()
    
            output = output.decode("utf-8")
            output = output.split("\n")
    
            tagged = []
    
            sentence = []
            for sen in output:
                if len(sen) == 0:
                    tagged.append(sentence)
                    sentence=[]
                sen = sen.split("\t")
                if len(sen) != 3:
                    continue
    
                sentence.append({"original": sen[0], "tag": sen[1], "root": sen[2]})
    
            tagged.append(sentence)
            tagged = [x for x in tagged if x != []]
        except Exception as e:
            raise TaggerError(f"Processing failed with: {e}")
        return tagged

    def tag(self, text):
        os.chdir("/opt/app/RNNTagger")
        self._write_file(text)
        return self._process()


class TaggerError(Exception):
    pass
