

<html>
   <head>
      <title><?php echo SITETITLE; ?> | <?php echo $title; ?></title>
      <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;">
      <!-- Theme CSS -->
      <link rel="stylesheet" type="text/css" href="<?php echo base_url('css/sb-admin-2.min.css');?>" />
      <link href="<?php echo base_url('css/all.css');?>" rel="stylesheet" type="text/css">
      <!-- jQuery -->
      <script src="<?php echo base_url('js/jquery-3.3.1.slim.min.js');?>" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <!-- Popper -->
      <script src="<?php echo base_url('js/popper.min.js');?>" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
      <!-- Bootstrap CSS and js -->
      <link rel="stylesheet" href="<?php echo base_url('css/bootstrap.min.css');?>">
      <script src="<?php echo base_url('js/bootstrap.min.js');?>" ></script>
      <!-- Charts -->
      <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js" integrity="sha256-qSIshlknROr4J8GMHRlW3fGKrPki733tLq+qeMCR05Q=" crossorigin="anonymous"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.min.js" integrity="sha256-xKeoJ50pzbUGkpQxDYHD7o7hxe0LaOGeguUidbq6vis=" crossorigin="anonymous"></script>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.css" integrity="sha256-IvM9nJf/b5l2RoebiFno92E5ONttVyaEEsdemDC6iQA=" crossorigin="anonymous" />
      <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.js" integrity="sha256-arMsf+3JJK2LoTGqxfnuJPFTU4hAK57MtIPdFpiHXOU=" crossorigin="anonymous"></script>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.css" integrity="sha256-aa0xaJgmK/X74WM224KMQeNQC2xYKwlAt08oZqjeF0E=" crossorigin="anonymous" />
      <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js" integrity="sha256-Uv9BNBucvCPipKQ2NS9wYpJmi8DTOEfTA/nH2aoJALw=" crossorigin="anonymous"></script>
      <!-- Custom CSS -->
      <link rel="stylesheet" type="text/css" href="<?php echo base_url('css/custom.css');?>" />
   </head>
   <body>
      <!-- Page Wrapper -->
      <div id="wrapper">
      <!-- Sidebar -->
      <ul class="navbar-nav bg-gradient-primary sidebar toggled sidebar-dark accordion" id="accordionSidebar">
         <!-- Sidebar - Brand -->
         <a class="sidebar-brand d-flex align-items-center justify-content-center" href="/">
            <div class="sidebar-brand-icon">
               <img src="<?php echo base_url('images/logo.png');?>">
            </div>
            <div class="sidebar-brand-text mx-3"><?php echo SITETITLE; ?></div>
         </a>
         <!-- Divider -->
         <hr class="sidebar-divider my-0">
         <!-- Nav Item - Dashboard -->
         <li class="nav-item">
            <a class="nav-link" href="/">
            <i class="fas fa-fw fa-home"></i>
            <span>Home</span></a>
         </li>
         <!-- Divider -->
         <hr class="sidebar-divider">
         <!-- Heading -->
         <div class="sidebar-heading">
            Trends
         </div>
         <!-- Nav Item - Dashboard -->
         <li class="nav-item">
            <a class="nav-link" href="/stats/trends">
            <i class="fas fa-fw fa-chart-line"></i>
            <span>Trends vergleichen</span></a>
         </li>
         <!-- Nav Item - Dashboard -->
         <li class="nav-item">
            <a class="nav-link" href="/stats/trendsbyparty">
            <i class="fas fa-fw fa-chart-bar"></i>
            <span>Trends nach Partei</span></a>
         </li>
         <!-- Divider -->
         <hr class="sidebar-divider">
         <!-- Heading -->
         <div class="sidebar-heading">
            Suche
         </div>
         <!-- Nav Item - Dashboard -->
         <li class="nav-item">
            <a class="nav-link" href="/search">
            <i class="fas fa-fw fa-search"></i>
            <span>Suche</span></a>
         </li>
         
         
         <!-- Divider -->
         <hr class="sidebar-divider">
         <!-- Nav Item - Dashboard -->
         <li class="nav-item">
            <a class="nav-link" href="/faq">
            <i class="fas fa-fw fa-question-circle"></i>
            <span>FAQ</span></a>
         </li>
         <li class="nav-item">
            <a class="nav-link" href="/imprint">
            <span>Impressum & Datenschutz</span></a>
         </li>
         <!-- Divider -->
         <hr class="sidebar-divider d-none d-md-block">
         <!-- Sidebar Toggler (Sidebar) -->
         <div class="text-center d-none d-md-inline">
            <button class="rounded-circle border-0" id="sidebarToggle"></button>
         </div>
      </ul>
      <!-- End of Sidebar -->
      <!-- Content Wrapper -->
      <div id="content-wrapper" class="d-flex flex-column">
      <!-- Main Content -->
      <div id="content">

         <!-- Sidebar Toggle (Topbar) -->
         <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
         <i class="fa fa-bars"></i>
         </button>
         
      </nav>
      <!-- End of Topbar -->

