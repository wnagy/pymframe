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
  <a href="/"><img src="../images/mframe_logo_64x64.png" class="logo" /></a><span class="application-name">pyMFrame</span>
  <div id="app-info">Version: $version mframe V:$mframeversion</div>
  <div id="backlink">&nbsp;</div>
 </header>
 <article>
 $flash
 <pre style="font-family:courier;text-align:center">
               __  _______                  
    ___  __ __/  |/  / __/______ ___ _  ___ 
   / _ \/ // / /|_/ / _// __/ _ `/  ' \/ -_)
  / .__/\_, /_/  /_/_/ /_/  \_,_/_/_/_/\__/ 
 /_/   /___/                                
  </pre>
      <br />
      <fieldset class="loginmask"><legend>Anmeldung</legend>
      <form name="login" style="display:inline" action="">
       <input type="hidden" name="path" value="/authen" />
       <br />Benutzer:<input size="16" id="id1" type="text" value="" name="user" mode="dashed" /> 
       <br />Passwort:<input size="16" type="password" value="" name="password" mode="dashed" /> 
       <br />
       <br /><input type="submit" value="Anmelden" class="mask" />
       <br />
      </form>
     </fieldset>
  </article>
  <footer id="footer">
  &nbsp;$version &copy; W. Nagy 2013
  </footer>

 </body>
</html>
 <script type="text/javascript">
    document.getElementById("id1").focus()
 </script>
