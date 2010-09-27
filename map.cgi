#!/usr/bin/perl

#--------------------------------------#
#            　 マップ            　　 #
#                                  　　#
#　　Copyright (c) 2008　チャゲ   　　 #
# 　 web：http://tyage.a.orn.jp/ 　　  #
# 　 mail：tyage2@nifmail.jp     　　  #
#--------------------------------------#

require './town_ini.cgi';
require './town_lib.pl';
&decode;

if($in{'mode'} eq "idou"){&idou;}
if($in{'mode'} eq "map"){&map;}

exit;

######################
#　以下サブルーチン　#
######################
sub map{
   #=====ゲストファイルOPEN=====#
   open(GST,"< $guestfile");
   eval{ flock (GST, 1); };
   foreach(<GST>){
      ($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
      if($hyouzi_check eq "off"){next;}
      if($mati_name==0 or !$mati_name){$keihan .= "$sanka_name<br>";}
      elsif($mati_name==1){$biwako .= "$sanka_name<br>";}
      elsif($mati_name==2){$nara .= "$sanka_name<br>";}
      elsif($mati_name==3){$wakayama .= "$sanka_name<br>";}
      else{&error("エラー");}
   }
   close(GST);

   if(!$keihan){$keihan="誰もいません";}
   if(!$biwako){$biwako="誰もいません";}
   if(!$nara){$nara="誰もいません";}
   if(!$wakayama){$wakayama="誰もいません";}

   #=====MAP表示=====#
   &header(ginkou_style);
   print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi height="100"><tr>
<td bgcolor=#ffffff>●陽気な駅員<br>
「ここは見てのとおり駅だよ。<br>
　でも普通の駅じゃあないんだ！<br>
　こそこそ隠れてない人がどこにいるか瞬時で分かっちゃう、高性\能\な駅なんだよ。<br>
　下のＭＡＰから電車を使えばどこでもいけるよ。」</td>
<td  bgcolor=#333333 align=center width=35%>
<font color="#ffffff" size="5"><b>ＳＴＡＴＩＯＮ</b></font>
</td>
</tr></table>
<br>
<center>
<table width="400" cellpadding="0" cellspacing="0" border="1" style="z-index:1;"><tr>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokutekiti value="0">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/keihansin-s.gif" width="200" height="150" title="京阪神ストリート" align="left" valign="top"><center><input type=submit value=京阪神ストリートへ style="border:1px solid;"></center><br><font color="#ffffff"><b>$keihan</b></font></td>
</form>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokutekiti value="1">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/biwako-s.gif" width="200" height="150" title="近江レイク" align="left" valign="top"><center><input type=submit value=近江レイクへ style="border:1px solid;"></center><br><font color="#ffffff"><b>$biwako</b></font></td>
</form>
</tr><tr>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokutekiti value="3">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/wakayama-s.gif" width="200" height="150" title="和歌山アイランド" align="left" valign="top"><center><input type=submit value=和歌山アイランド style="border:1px solid;"></center><br><font color="#ffffff"><b>$wakayama</b></font></td>
</form>
<form method=POST action="./station.cgi">
<input type=hidden name=command value="densya">
<input type=hidden name=maemati value="$in{'town_no'}">
<input type=hidden name=mokutekiti value="2">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>idou<>">
<td background="img/nara-s.gif" width="200" height="150" title="奈良シティ" align="left" valign="top"><center><input type=submit value=奈良シティ style="border:1px solid;"></center><br><font color="#ffffff"><b>$nara</b></font></td>
</form>
</tr></table>
</center>
EOM
exit;
}

sub idou{
   if(!$in{'maemati'}){&error("あなたはどこから来たの？");}
   if(!$in{'mokuteki'}){&error("あなたはどこに行くの？");}
   if($in{'maemati'}==$in{'mokuteki'}){&error("街に戻るんなら普通の戻ればいいでしょうに");}
   $matiidou_time2=3;
   $soutai=$in{'maemati'} + $in{'mokuteki'};

   if($soutai==0){&error("気分的にエラー");}
   elsif($soutai==1){$nedan=2500;}
   elsif($soutai==2){$nedan=3000;}
   elsif($soutai==3){$nedan=4000;}
   elsif($soutai==4){$nedan=2000;}
   elsif($soutai==5){$nedan=3500;}
   else{&error("気分的にエラー");}

   $money -= $nedan;

   &temp_routin;
   &log_kousin($my_log_file,$k_temp);
   #=====ゲストファイルOPEN=====#
   open(GST,"< $guestfile");
   eval{ flock (GST, 1); };
   foreach(<GST>){
       ($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
       if($hyouzi_check eq "off"){next;}
       if($mati_name==0 or !$mati_name){$keihan .= "$sanka_name<br>";}
       elsif($mati_name==1){$biwako .= "$sanka_name<br>";}
       elsif($mati_name==2){$nara .= "$sanka_name<br>";}
       elsif($mati_name==3){$wakayama .= "$sanka_name<br>";}
       else{&error("エラー");}
   }
   close(GST);
   if(!$keihan){$keihan="誰もいません";}
   if(!$biwako){$biwako="誰もいません";}
   if(!$nara){$nara="誰もいません";}
   if(!$wakayama){$wakayama="誰もいません";}

   #=====移動中表示=====#
   &header(syokudou_style);
   print <<"EOM";
<script language="JavaScript"><!--
var TimeID;
var counts=$matiidou_time2;
window.setTimeout("run()",1000);
function run(){
counts--;
document.getElementById("time").innerHTML = counts;
if(counts>0){timeID = setTimeout("run()",1000);}
}

//--></script>

<br><br><br><br><table  border=0  cellspacing="5" cellpadding="0" width=200 align=center bgcolor=#ffffcc><tr><td><div align=center style=\"font-size:11px\">電車で移動中...<br><span id=\"time\">$matiidou_time2</span>秒ほどお待ちください。<br>$nedan円支払いました。</div></td></tr></table>

<center>
<table width="400" cellpadding="0" cellspacing="0" border="1" style="z-index:1;"><tr>
<td background="img/keihansin-s.gif" width="200" height="150" title="京阪神ストリート" align="left" valign="top"><center><font color="red"><b>京阪神ストリート</b></font></center><br><font color="#ffffff"><b>$keihan</b></font></td>
<td background="img/biwako-s.gif" width="200" height="150" title="近江レイク" align="left" valign="top"><center><font color="red"><b>近江レイク</b></font></center><br><font color="#ffffff"><b>$biwako</b></font></td>
</tr><tr>
<td background="img/wakayama-s.gif" width="200" height="150" title="和歌山アイランド" align="left" valign="top"><center><font color="red"><b>和歌山アイランド</b></font></center><br><font color="#ffffff"><b>$wakayama</b></font></td>
<td background="img/nara-s.gif" width="200" height="150" title="奈良シティ" align="left" valign="top"><center><font color="red"><b>奈良シティ</b></font></center><br><font color="#ffffff"><b>$nara</b></font></td>
</tr></table>
</center>

<form method=POST name=f_idou action="$script">
<input type=hidden name=mode value="login_view">
<input type=hidden name=town_no value="$in{'mokuteki'}">
<input type=hidden name=idou value="$idou_time">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=ziko_flag value="off">
<input type=hidden name=maigo value="">
</form>
EOM

exit;
}