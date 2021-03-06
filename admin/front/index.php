<!doctype html>
<!--
	Solution by GetTemplates.co
	URL: https://gettemplates.co
-->
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <!-- custom CSS -->
    <link rel="stylesheet" href="css/style.css">
    <title>Admin - My youtube</title>
    <!-- Global site tag (gtag.js) - Google Analytics -->
</head>
<body class="fullscreen">
  <div class="d-flex" id="wrapper">

  <!-- Sidebar -->
  <div class="bg-light border-right" id="sidebar-wrapper">
    <div class="sidebar-heading">My youtube</div>
    <div class="list-group list-group-flush">
      <?php
      $available = scandir("/stats/");
      foreach ($available as $file){
        $res = explode(".html", $file);
        if (count($res) > 1){
          echo "<a onclick=\"switchiframe('./stats/".$res[0].".html')\" class=\"choice list-group-item list-group-item-action bg-light\">Stats ".$res[0]."</a>\n";
        }
      }
      ?>
      <a onclick="switchiframe('./phpmyadmin/')" class="choice list-group-item list-group-item-action bg-light">SQL</a>
    </div>
  </div>
  <!-- /#sidebar-wrapper -->

  <!-- Page Content -->
  <div id="page-content-wrapper">

    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
      <button class="btn btn-primary" id="menu-toggle">Menu</button>

      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto mt-2 mt-lg-0">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Liens
            </a>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" href="https://github.com/SCcagg5/My_Youtube">Github</a>
              <div class="dropdown-divider"></div>
            </div>
          </li>
        </ul>
      </div>
    </nav>

    <div class="container-fluid container-extend">
      <iframe frameborder="0" id="iframe" src="./phpmyadmin/" class="all">
      </iframe>
    </div>
  </div>
  <!-- /#page-content-wrapper -->

</div>
<!-- /#wrapper -->

<!-- Bootstrap core JavaScript -->
<script src="js/jquery-3.3.1.slim.min.js"></script>
<script src="js/bootstrap.bundle.min.js"></script>

<!-- Menu Toggle Script -->
<script>
  $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });

  function switchiframe(path){
    $("#iframe")[0].src = path;
  }
</script>


</body>
</html>
