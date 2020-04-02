<!-- Styles -->

<style>
#linediv {
    max-width: 100%;
    width:100%;
}

.box {
display: block;
position: relative;
  width:100%;
  height: 65vh !important;
  padding: 4vh;
  max-width: 100%;
}
</style>

<!-- Resources -->
<script src="<?php echo base_url('js/core.js');?>"></script>
<script src="<?php echo base_url('js/amchart.js');?>"></script>
<script src="<?php echo base_url('js/animated.js');?>"></script>

<?php if(isset($values['data'])):?>
<!-- Chart code -->
<script>
am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create("linediv", am4charts.XYChart);
chart.dateFormatter.dateFormat = "yyyy-MM-dd";


var data = <?php echo $values['data']; ?>;


chart.data = data;

// Create axes
var xAxis = chart.xAxes.push(new am4charts.DateAxis());
xAxis.dataFields.category = "category";
xAxis.renderer.grid.template.location = 0;

//xAxis.renderer.minGridDistance = 30;

var yAxis = chart.yAxes.push(new am4charts.ValueAxis());
<?php $i = 0;?>
<?php while ($i <= $values['amount']): ?>
// Create series
var series<?php echo $i;?> = chart.series.push(new am4charts.LineSeries());
series<?php echo $i;?>.dataFields.valueY = "value<?php echo $i;?>";
series<?php echo $i;?>.dataFields.dateX = "date";
series<?php echo $i;?>.tooltipText = "{value<?php echo $i;?>}";
series<?php echo $i;?>.tensionX = 1;
series<?php echo $i;?>.fillOpacity = 0.2;
series<?php echo $i;?>.strokeWidth = 3;
series<?php echo $i;?>.stroke = am4core.color("<?php echo $values['color'][$i];?>");
series<?php echo $i;?>.fill = am4core.color("<?php echo $values['color'][$i];?>");


var bullet = series<?php echo $i;?>.bullets.push(new am4charts.CircleBullet());

series<?php echo $i;?>.tooltip.pointerOrientation = "vertical";
<?php $i += 1;?>
<?php endwhile;?>

chart.cursor = new am4charts.XYCursor();
chart.cursor.snapToSeries = series;

//chart.scrollbarY = new am4core.Scrollbar();
chart.scrollbarX = new am4core.Scrollbar();

}); // end am4core.ready()
</script>
<?php endif;?>
<!-- HTML -->

<div class="container-fluid">


<div class="row">

	<div class="col-md-12" style="width: 100%">
	<h1 ><?php echo $title;?></h1><br>

	</div>
  <?php if(isset($values['data'])):?>
  <div class="col-md-12 searchwords">
  <small>Bis zu 6 Stichwörter eingeben</small>
  <form method="GET">
    <input type="text" name="search" placeholder="Suchwort1, Suchwort2" value="<?php if (isset($_GET['search'])) {echo $_GET['search'];}?>">
    <input type="checkbox" name="daily" value="true" <?php if (isset($_GET['daily']) && $_GET['daily'] == 'true') {echo("checked");}?>> <small>tagesgenaue Auflösung</small>
<br>
    <button type="submit" class="btn btn-success">Suchen</button>
    <a href="/stats/trends" class="btn btn-danger">Löschen</a>
  </form>
  <?php $i = 0; ?>
  <?php foreach ($values['searchwords'] as $word): ?>
  <span class="badge badge-pill badge-secondary" style="background-color: <?php echo $values['color'][$i];?>"><?php echo $word;?></span>
  <?php $i += 1;
  endforeach;?>
  
  </div>

</div>

</div>

<?php if (strlen($values['data']) < 3): ?>
<div class="container-fluid">


<div class="row msg">

	<div class="col-md-12" style="width: 100%">
	<h2>Keine Einträge</h2><br>

	</div>

</div>

</div>
<?php endif;?>
<div class="box">

<div id="linediv" style="width: 100%; height: 500px;"></div>
</div>
<?php endif;?>

<?php if(!isset($values['data'])):?>
</div>
</div>

<div class="container-fluid">


<div class="row msg">

	<div class="col-md-12" style="width: 100%">
	<h2>404 API down</h2><br>

	</div>

</div>

</div>
<?php endif;?>




