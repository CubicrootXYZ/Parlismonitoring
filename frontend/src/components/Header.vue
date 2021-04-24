<template>
    <!-- Sidebar -->
    <ul class="navbar-nav toggled bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

        <!-- Sidebar - Brand -->
        <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">

            <div class="sidebar-brand-icon rotate-n-5">
                <i class="fas fa-university"></i>
            </div>
            <br>
            <div class="sidebar-brand-text mx-3">PARLISmonitoring</div>

        </a>

        <!-- Heading -->
        <div class="sidebar-heading">
            Home
        </div>

        <li class="nav-item">
            <a class="nav-link" href="/">
                <i class="fas fa-fw fa-home"></i>
                <span>Home</span></a>
        </li>

        <!-- Heading -->
        <div class="sidebar-heading">
            Dateien
        </div>

        <li class="nav-item">
            <a class="nav-link" href="/files/search">
                <i class="fas fa-fw fa-search"></i>
                <span>Suche</span></a>
        </li>

        <!-- Heading -->
        <div class="sidebar-heading">
            Statistik
        </div>

        <!--<li class="nav-item">
            <a class="nav-link" href="/files/latest">
                <i class="fas fa-fw fa-clock"></i>
                <span>Statistik</span></a>
        </li>-->

        <li class="nav-item">
            <a class="nav-link" href="/words/usage">
                <i class="fas fa-fw fa-clock"></i>
                <span>Wörter-Statistik</span></a>
        </li>

        <!-- Heading -->
        <div class="sidebar-heading">
            Mehr
        </div>

        <li class="nav-item">
            <a class="nav-link" href="/faq">
                <i class="fas fa-question-circle"></i>
                <span>FAQ</span></a>
        </li>

        <!-- Sidebar Toggler (Sidebar) -->
        <div class="text-center d-none d-md-inline">
            <button class="rounded-circle border-0" id="sidebarToggle"></button>
        </div>
    </ul>
    <!-- End of Sidebar -->


</template>