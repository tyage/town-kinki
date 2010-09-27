#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
# 
#　 Edit:たっちゃん　2007/11/11
#################################
# unit.pl
#"ゲムラ" => "<form method=POST action=\"gamerand.cgi\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/kentiku_yotei.gif'  onMouseOver='onMes5(\"ゲームランド\")' onMouseOut='onMes5(\"\")'></td></form>\n",
#################################

# $this_script = "gamerand.cgi";
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
#制限時間チェック
#2008/01/06
	if(!$k_id && $in{'name'}){
		open(IN,"< $logfile") || &error("Open Error : $logfile");
		eval{ flock (IN, 1); }; 
		@all_member = <IN>;
		close(IN);
		foreach (@all_member){
			(@kojin_dat) = split(/<>/);
			if ($in{'name'} eq $kojin_dat[1]){
				$k_id = $kojin_dat[0];
				$in{'k_id'} = $k_id;
				last;
			}
		}
	}
#end01/16
	if($in{'name'} eq""){&error("ログインしてください。")}
#main
	&header(ginkou_style);

	print <<"EOM";
<center>
<h1>ゲームランド</h1>

<table border="0" cellspacing="0" cellpadding="0" background="img/road/bg.gif">
<tr>

<td width="32" height="32"><img width="32" height="32" src="img/road/1.gif"></td>

<form method=POST action="donut.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>donus<>">
<input type="image" src="$img_dir/donuts_tate.gif" width="32" height="32" onMouseOver="Navi('$img_dir/donuts_tate.gif','カードゲーム','前の人が引いたカードと同じ数字を出さないようにするカードゲームです。<br>掛け金１万円です。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/2.gif"></td>

<form method=POST action="donut.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>donus2<>">
<input type=image src="$img_dir/donuts_tate.gif" width="32" height="32" onMouseOver="Navi('$img_dir/donuts_tate.gif','カードゲーム２','前の人が引いたカードと同じ数字を出さないようにするカードゲームです。<br>掛け金２万円です。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/2.gif"></td>

<form method=POST action="donut.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>donus3<>">
<input type=image src="$img_dir/donuts_tate.gif"width="32" height="32" onMouseOver="Navi('$img_dir/donuts_tate.gif','カードゲーム３','前の人が引いたカードと同じ数字を出すようにするカードゲームです。<br>掛け金１０万円です。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/2.gif"></td>

<form method=POST action="donut.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>donus4<>">
<input type=image src="$img_dir/hi&lo.gif" width="32" height="32" onMouseOver="Navi('$img_dir/donuts_tate.gif','High＆Lowを当てるゲームです。','前のカードより高いか低いかを当てます。<br>掛け金１万です。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/3.gif"></td>

</tr>

<tr>
<td width="32" height="32"><img width="32" height="32" src="img/road/4.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/6.gif"></td>
</tr>

<tr>

<td width="32" height="32"><img width="32" height="32" src="img/road/4.gif"></td>

<form method=POST action="slot.php"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>l1_slot<>">
<input type=image src="$img_dir/slot.gif" width="32" height="32" onMouseOver="Navi('$img_dir/slot.gif','スロットで遊ぼう。','スロットで一攫千金！<br>ついでにステータスもちょびっとあがります。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<form method=POST action="loto.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>loto_game<>">
<input type=image src="$img_dir/loto.gif" width="32" height="32" onMouseOver="Navi('$img_dir/loto.gif','ロトくじだよ。','ロトくじです。<br>その場で当たります。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<form method=POST action="loto6.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>loto_game<>">
<input type=image src="$img_dir/loto6.gif" onMouseOver="Navi('$img_dir/loto6','ロト６だよ。','一口2500円のロト６です。<br>当選金は銀行の普通口座に振り込まれます。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<form method=POST action="fukubiki.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>fukubiki<>">
<input type=image src="$img_dir/fukubiki.gif" width="32" height="32" onMouseOver="Navi('$img_dir/fukubiki.gif','ふくびきです。','福引券がないとできません。<br>いろんな賞品が当たります', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/6.gif"></td>

</tr>

<tr>
<td width="32" height="32"><img width="32" height="32" src="img/road/4.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/6.gif"></td>
</tr>

<tr>

<td width="32" height="32"><img width="32" height="32" src="img/road/4.gif"></td>

<form method=POST action="saikoro.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>saikoro<>">
<input type=image src="$img_dir/saikoro.gif" width="32" height="32" onMouseOver="Navi('$img_dir/saikoro.gif','サイコロで遊ぼう。','偶数か奇数かを当てます。<br>当たれば掛け金がもらえます。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<form method=POST action="cardw2.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>cardw<>">
<input type=image src="$img_dir/malti.gif" width="32" height="32" onMouseOver="Navi('$img_dir/malti.gif','マルチカードで遊ぼう。','掛け金を選んでカードを引きます。<br>当たれば、掛け金×レート分のお金がもらえます。', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<!-- <form method=POST action="kuzi.cgi"> --><td width="32" height="32">
<!-- 
<input type=hidden name=gamerand value="gamerand">
<input type=hidden name=mode value="kuzi_game">
<input type=hidden name=name value="$in{"name"}">
<input type=hidden name=pass value="$in{"pass"}">
<input type=hidden name=k_id value="$in{"k_id"}">
<input type=hidden name=town_no value="$in{"town_no"}">
 -->
<input type=image src="$img_dir/kuji.gif" width="32" height="32" onclick="{alert("今は入れません。")}">
<!-- </form> -->
</td>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<form method=POST action="otakara.cgi"><td width="32" height="32">
<input type=hidden name=gamerand value="gamerand">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>otakara<>">
<input type=image src="$img_dir/otakara.gif" width="32" height="32" onMouseOver="Navi('$img_dir/otakara.gif','お宝ゲーム！','お金を払って宝箱を開けていきます。<br>なにが当たるかはお楽しみ！', 0, event);" onMouseOut="NaviClose();">
</td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/6.gif"></td></tr>

<tr>
<td width="32" height="32"><img width="32" height="32" src="img/road/4.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/6.gif"></td>
</tr>

<tr>

<td width="32" height="32"><img width="32" height="32" src="img/road/4.gif"></td>

<form method=POST action="obatyan.cgi">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>week<>">
<td height=32 width=32>
<input type=image src="$img_dir/obatyan.gif" width=32 height=32 onMouseOver="Navi('$img_dir/obatyan.gif','弱いおばちゃんに挑戦状を突きつけます。','おばちゃんパワーに負けるな！<br>アイテムやお金を落とします。', 0, event);" onMouseOut="NaviClose();"></td></form>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<form method=POST action="obatyan.cgi">
<input type=hidden name=mode value="strong">
<input type=hidden name=name value="$in{"name"}">
<input type=hidden name=pass value="$in{"pass"}">
<input type=hidden name=k_id value="$k_id">
<input type=hidden name=town_no value="$in{"town_no"}">
<td height=32 width=32>
<input type=image src="$img_dir/obatyan2.gif" width=32 height=32 onMouseOver="Navi('$img_dir/obatyan2.gif','強いおばちゃんに挑戦状を突きつけます。','おばちゃんパワーに負けるな！<br>アイテムやお金を落とします。', 0, event);" onMouseOut="NaviClose();">
</td>
</form>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<td>
<a href="http://w6.oroti.com/~nikuman/town/" target="_blank"><img src="$img_dir/nikuman.gif" width=32 height=32 border=0 onMouseOver="Navi('$img_dir/nikuman.gif','肉まん（豚マン）☆TOWNです。','管理人は肉まんさんです。<br>面白いＴＯＷＮです。', 0, event);" onMouseOut="NaviClose();"></a>
</td>

<td width="32" height="32"><img width="32" height="32" src="img/road/5.gif"></td>

<td>
<a href="http://w2.oroti.com/~tyage/chin/login.cgi" target="_blank" onMouseOver="Navi('http://w2.oroti.com/~tyage/chin/img/car11.gif','珍走記です。','珍走記です。<br>日本中を駆け回れ！', 0, event);" onMouseOut="NaviClose();"><img src=http://w2.oroti.com/~tyage/chin/img/car11.gif width=32 height=32 border=0></a>
</td>

<td width="32" height="32"><img width="32" height="32" src="img/road/6.gif"></td></tr>

<tr>
<td width="32" height="32"><img width="32" height="32" src="img/road/4.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/kousa.gif"></td>
<td width="32" height="32"><img width="32" height="32" src="img/road/6.gif"></td>
</tr>

<tr>

<td width="32" height="32"><img width="32" height="32" src="img/road/7.gif"></td>

<td width="32" height="32">
<a href="../wolf/" target=_blank><img src=$img_dir/wlf.gif width=32 height=32 border=0 onMouseOver="Navi('$img_dir/wlf.gif','人狼です。','人狼です。<br>頭脳を駆使して戦います！', 0, event);" onMouseOut="NaviClose();"></a>
</td>

<td width="32" height="32"><img width="32" height="32" src="img/road/8.gif"></td>

<td width="32" height="32">
<a href="../aki/" target="_blank"><img src=../aki/akimono/image/job/job.gif width=32 height=32 border=0 onMouseOver="Navi('../aki/akimono/image/job/job.gif','商人物語（７種類）です。','商人物語です。<br>現在停止中です。', 0, event);" onMouseOut="NaviClose();"></a>
</td>

<td width="32" height="32"><img width="32" height="32" src="img/road/8.gif"></td>

<td width="32" height="32"><a href="../ffaicu/" target="_blank"><img src=../ffaicu/images/link.gif width=32 height=32 border=0 onMouseOver="Navi('../ffaicu/images/link.gif','ＦＦＡいく改です。','ＦＦＡいく改です。<br>ＦＦっぽいゲームです。', 0, event);" onMouseOut="NaviClose();"></a>
</td>

<td width="32" height="32"><img width="32" height="32" src="img/road/8.gif"></td>

<form method=POST name=ct action="$script"><td>
<input type=hidden name=std value="$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis">
<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>login_view<>">
<input type=image src="$img_dir/game.gif" width=32 height=32>
</td>
</form>

<td width="32" height="32"><img width="32" height="32" src="img/road/9.gif"></td>

</tr>

</table>

EOM

exit;


