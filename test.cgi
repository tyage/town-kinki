#!/usr/bin/perl

require './town_ini.cgi';
require './town_lib.pl';

&decode;

$url_adresu = 'ランキングへのURI';

$money += 10000;

#ログ更新
&temp_routin;
&log_kousin($my_log_file,$k_temp);

&header(gym_style);

print <<"EOM";
<html>
<head>
<META http-equiv="content-type" content="text/html; charset=Shift_JIS">
<script type="text/javascript"><!-- 
window.open("$url_adresu","_self");
--></script>
</head>
<body>
コメント
</body>
</html>
EOM

exit;