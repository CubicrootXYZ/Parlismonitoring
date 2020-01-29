<!-- Styles -->
<style>
#chartdiv {
  width:100%;
  height: 45vh;
  padding-bottom: 4vh;
}
</style>

<!-- Resources -->
<script src="https://www.amcharts.com/lib/4/core.js"></script>
<script src="https://www.amcharts.com/lib/4/charts.js"></script>
<script src="https://www.amcharts.com/lib/4/plugins/wordCloud.js"></script>
<script src="https://www.amcharts.com/lib/4/themes/animated.js"></script>

<!-- Chart code -->
<script>
am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end


var chart = am4core.create("chartdiv", am4plugins_wordCloud.WordCloud);
var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());

series.accuracy = 3;
series.step = 15;
series.rotationThreshold = 0.7;
series.maxCount = 200;
series.minWordLength = 2;
series.labels.template.tooltipText = "{word}: {value} Erwähnungen";
series.fontFamily = "Courier New";

series.data = <?php echo $wordcloud_all ?>;

series.dataFields.word = "tag";
series.dataFields.value = "weight"; 
series.maxFontSize = am4core.percent(8);
series.minFontSize = am4core.percent(3);

series.heatRules.push({
 "target": series.labels.template,
 "property": "fill",
 "min": am4core.color("#c7c7c7"),
 "max": am4core.color("#000000"),
 "dataField": "value"
});

//series.text = "Though yet of Hamlet our dear brother's death The memory be green, and that it us befitted To bear our hearts in grief and our whole kingdom To be contracted in one brow of woe, Yet so far hath discretion fought with nature That we with wisest sorrow think on him, Together with remembrance of ourselves. Therefore our sometime sister, now our queen, The imperial jointress to this warlike state, Have we, as 'twere with a defeated joy,-- With an auspicious and a dropping eye, With mirth in funeral and with dirge in marriage, In equal scale weighing delight and dole,-- Taken to wife: nor have we herein barr'd Your better wisdoms, which have freely gone With this affair along. For all, our thanks. Now follows, that you know, young Fortinbras, Holding a weak supposal of our worth, Or thinking by our late dear brother's death Our state to be disjoint and out of frame, Colleagued with the dream of his advantage, He hath not fail'd to pester us with message, Importing the surrender of those lands Lost by his father, with all bonds of law, To our most valiant brother. So much for him. Now for ourself and for this time of meeting: Thus much the business is: we have here writ To Norway, uncle of young Fortinbras,-- Who, impotent and bed-rid, scarcely hears Of this his nephew's purpose,--to suppress His further gait herein; in that the levies, The lists and full proportions, are all made Out of his subject: and we here dispatch You, good Cornelius, and you, Voltimand, For bearers of this greeting to old Norway; Giving to you no further personal power To business with the king, more than the scope Of these delated articles allow. Farewell, and let your haste commend your duty. Tis sweet and commendable in your nature, Hamlet,To give these mourning duties to your father: But, you must know, your father lost a father; That father lost, lost his, and the survivor bound In filial obligation for some term To do obsequious sorrow: but to persever In obstinate condolement is a course Of impious stubbornness; 'tis unmanly grief; It shows a will most incorrect to heaven, A heart unfortified, a mind impatient, An understanding simple and unschool'd: For what we know must be and is as common As any the most vulgar thing to sense, Why should we in our peevish opposition Take it to heart? Fie! 'tis a fault to heaven, A fault against the dead, a fault to nature, To reason most absurd: whose common theme Is death of fathers, and who still hath cried, From the first corse till he that died to-day, 'This must be so.' We pray you, throw to earth This unprevailing woe, and think of us As of a father: for let the world take note, You are the most immediate to our throne; And with no less nobility of love Than that which dearest father bears his son, Do I impart toward you. For your intent In going back to school in Wittenberg, It is most retrograde to our desire: And we beseech you, bend you to remain Here, in the cheer and comfort of our eye, Our chiefest courtier, cousin, and our son."; 

}); // end am4core.ready()
</script>

<!-- HTML -->
<div id="chartdiv"></div>

<div class="container-fluid home">


<div class="row welcome">

	<div class="col-md-12" style="width: 100%">
	<h1 ><?php echo SITETITLE;?></h1><br>
	<h2 class="">Dokumente suchen, Trends erkennen, Auswertungen einsehen</h2>
	<br>
	<a href="/trends" class="btn btn-warning">Trends anschauen <i class="fas fa-angle-right"></i></a>
	</div>

</div>

</div>

<div class="wordclouds">

	<?php $i = 0;
	if (isset($wordclouds[0]['color_bg'])):
	?>
	<?php foreach ($wordclouds as $wordcloud): ?>
	<div class="cloud" style="background-color: <?php echo $wordcloud['color_bg']; ?>">
	<span class="title" style="color: <?php echo $wordcloud['color1']; ?>;"><?php echo $wordcloud['name']; ?></span>
	<style>
	#chartdiv<?php echo $i;?> {
		height: 500px;
		
	}
	</style>

	<!-- Chart code -->
	<script>
	am4core.ready(function() {

	// Themes begin
	am4core.useTheme(am4themes_animated);
	// Themes end


	var chart = am4core.create("chartdiv<?php echo $i;?>", am4plugins_wordCloud.WordCloud);
	var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());

	series.accuracy = 2;
	series.step = 10;
	series.rotationThreshold = 0.7;
	series.maxCount = 200;
	series.minWordLength = 2;
	series.labels.template.tooltipText = "{word}: {value} Erwähnungen";
	series.fontFamily = "Courier New";

	series.data = <?php echo $wordcloud['data'] ?>;

	series.dataFields.word = "tag";
	series.dataFields.value = "weight"; 
	series.maxFontSize = am4core.percent(15);
	series.minFontSize = am4core.percent(4);

	series.heatRules.push({
	"target": series.labels.template,
	"property": "fill",
	"min": am4core.color("<?php echo $wordcloud['color2']; ?>"),
	"max": am4core.color("<?php echo $wordcloud['color1']; ?>"),
	"dataField": "value"
	});

	
	}); // end am4core.ready()
	</script>

	<!-- HTML -->
	<div id="chartdiv<?php echo $i;?>"></div>
</div>

<?php $i += 1;?>
<?php endforeach;
endif;?>

</div>