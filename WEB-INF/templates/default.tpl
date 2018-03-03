<!DOCTYPE html>
<html lang="de">
<head>
 <meta charset="utf-8">
 <title>pyMframe [$path]</title>	
 <!-- ist eine Anwendung, wir wollen nicht in Google auftauchen -->
 <meta name="robots" content="noindex, nofollow"> 
 <meta name="generator" content="pyFrame" />
 <meta name="author" content="W.Nagy" />
 <meta name="keywords" content="Python Micro FramWork" />
 <meta http-equiv="content-type" content="text/html; charset=utf-8">
 <link rel="stylesheet" type="text/css" href="/css/normal.css" />
 <link rel="stylesheet" type="text/css" href="/css/add.css" />
 $stylesheet
</head> 
<body>
 <header>
  <img src="../images/system-hibernate.png" onClick="document.location='?path=/authen&action=logout'" id="system-button" alt="Logout" title="Abmelden"/>
  <img src="../images/view-refresh-5.png" onClick="document.location.reload(true)" id="system-button" alt="Refresh" title="Bildschirm neu aufbauen"/>
  <a href="/"><img src="../images/mframe_logo_64x64.png" class="logo" /></a>
  <span class="application-name">pyMFrame</span>
  <div id="app-info">Version: $version $user $rights</div>
  <div id="backlink">$backlink</div>
  <nav><menu>$menu</menu></nav>
 </header>
<body>
  $flash
  <article>
  <div id="content">
   $body
  </div>
  </article>
  <footer>
  &nbsp;mframe V:$mframeversion &copy; W. Nagy 2013
  </footer>
 </body>
</html>

