

<div class="container-fluid">


<div class="row">

	<div class="col-md-12" style="width: 100%">
	<h1 ><?php echo $title;?></h1><br>

	</div>
  <?php if(isset($content)):?>
    <form method="GET">
  <div class="row searchwords">

    <div class="col-sm-2">
        <small>Suchwort eingeben</small><br>
        <input type="text" name="searchstring" placeholder="Suchwort" value="<?php if (isset($_GET['searchstring'])) {echo $_GET['searchstring'];}?>">
    </div>
    <div class="col-sm-2">
        <small>Autor (Partei) wählen</small><br>
        <select name="author">
            <option value="<?php if (isset($_GET['author'])) {echo $_GET['author'];}?>"><?php if (isset($_GET['author'])) {echo $_GET['author'];}?></option>
            <option value="">Alle</option>
            <?php foreach ($authors as $author): ?>
            <option value="<?php echo($author["author"]);?>"><?php echo($author["author"]);?></option>
            <?php endforeach;?>

        </select>
    </div>
    <div class="col-sm-2">
        <small>Typ eingeben</small><br>
        <input type="text" name="type" placeholder="Typ" value="<?php if (isset($_GET['type'])) {echo $_GET['type'];}?>">
    </div>
    <div class="col-sm-2">
        <small>Dateinummer eingeben</small><br>
        <input type="text" name="filenumber" placeholder="Typ" value="<?php if (isset($_GET['filenumber'])) {echo $_GET['filenumber'];}?>">
    </div>
    <div class="col-sm-2">
        <small>Suchen bis</small><br>
        <?php $date = new DateTime();?>
        <input type="date" name="date_end" placeholder="Typ" value="<?php if (isset($_GET['date_end'])) {echo $_GET['date_end'];} else {echo(date_format($date, 'Y-m-d'));}?>">
    </div>
    <div class="col-sm-2">
        <small>Suchen von</small><br>
        <?php  date_sub($date, date_interval_create_from_date_string('1 year'));?>
        <input type="date" name="date_begin" placeholder="Typ" value="<?php if (isset($_GET['date_begin'])) {echo $_GET['date_begin'];} else {echo(date_format($date, 'Y-m-d'));}?>">
    </div>
    <div class="col-sm-12 box">
        <small>Suche auf Dateiinhalte ausweiten (experimentell)</small><br>
        <input type="checkbox" name="experimental" value="true" <?php if (isset($_GET['experimental']) && $_GET['experimental'] == "true") {echo("checked");}?>>
    </div>

<br>
<div class="col-sm-12">
    <button type="submit" class="btn btn-success">Suchen</button>
    <a href="/search" class="btn btn-danger">Löschen</a>
</div>

  </form>
</div>


  <?php foreach ($content as $file): ?>
    <div class="card">
        <div class="card-header">
            <?php echo($file['title'])?>
        </div>

        <div class="card-body row">
            <div class="col-sm-6">
            <b>Autor:</b> <?php echo($file['author'])?>
            </div>

            <div class="col-sm-6">
            <b>Typ:</b> <?php echo($file['type'])?>
            </div>

            <div class="col-sm-6">
            <b>Nummer:</b> <?php echo($file['number'])?>
            </div>

            <div class="col-sm-4">
            <b>Datum:</b> <?php echo($file['date'])?>
            </div>

            <?php if (strlen($file['link']) > 5):?>
            <div class="col-sm-2">
            <a href="<?php echo($file['link'])?>" target="_blank" class="btn btn-success">PDF-Datei <i class="fas fa-chevron-right"></i></a>
            </div>
            <?php endif;?>
        </div>

    </div>

  <?php endforeach;?>
  
  </div>

</div>

</div>

<?php if (sizeof($content) < 1): ?>
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

<?php if(!isset($content)):?>
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




