#!/usr/bin/perl

####################
$max_dat=50;
$max=10;
####################

$this_script = 'event.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;

$filename='log_dir/eventlog.cgi';
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}

if($in{'mode'} eq "form"){&form;}
elsif($in{'mode'} eq "save"){&save;}
else{&error("エラー");}

exit;

###########################################
sub save{
	if ($in{'msg'}){
		$in{'msg'} =~ s/</&lt;/g;
		$in{'msg'} =~ s/>/&gt;/g;
	}else{&error("メッセ－ジがありません。");}
	
	open(OI,"< $filename") || &error("Open Error : $ori_ie_list");
	eval{ flock (OI, 2); };
	@event_data = <OI>;
	close(OI);
	
	if ($#event_data + 1 >= $max_dat){
		$#event_data = $max_dat - 1;
	}
	$num = split(/<>/,$load_dat[0]);
	$num++;
	
	if($in{'syo_looks'} == 0){$in{'syo_looks'} = "";}
	if($in{'syo_tairyoku'} == 0){$in{'syo_tairyoku'} = "";}
	if($in{'syo_kenkou'} == 0){$in{'syo_kenkou'} = "";}
	if($in{'syo_speed'} == 0){$in{'syo_speed'} = "";}
	if($in{'syo_power'} == 0){$in{'syo_power'} = "";}
	if($in{'syo_wanryoku'} == 0){$in{'syo_wanryoku'} = "";}
	if($in{'syo_kyakuryoku'} == 0){$in{'syo_kyakuryoku'} = "";}
	
	if($in{'syo_kokugo'} == 0){$in{'syo_kokugo'} = "";}
	if($in{'syo_suugaku'} == 0){$in{'syo_suugaku'} = "";}
	if($in{'syo_rika'} == 0){$in{'syo_rika'} = "";}
	if($in{'syo_syakai'} == 0){$in{'syo_syakai'} = "";}
	if($in{'syo_eigo'} == 0){$in{'syo_eigo'} = "";}
	if($in{'syo_ongaku'} == 0){$in{'syo_ongaku'} = "";}
	if($in{'syo_bijutu'} == 0){$in{'syo_bijutu'} = "";}
	
	if($in{'syo_love'} == 0){$in{'syo_love'} = "";}
	if($in{'syo_unique'} == 0){$in{'syo_unique'} = "";}
	if($in{'syo_etti'} == 0){$in{'syo_etti'} = "";}
	if($in{'syo_sintai_kaihuku'} == 0){$in{'syo_sintai_kaihuku'} = "";}
	if($in{'syo_zunou_kaihuku'} == 0){$in{'syo_zunou_kaihuku'} = "";}
	if($in{'syo_sintyou'} == 0){$in{'syo_sintyou'} = "";}
	if($in{'syo_cal'} == 0){$in{'syo_cal'} = "";}
	
	if($in{'syo_money'} == 0){$in{'syo_money'} = "";}
	if($in{'syo_byouki'}){
		$in{'syo_byouki'} =~ s/</&lt;/g;
		$in{'syo_byouki'} =~ s/>/&gt;/g;
	}
	if($in{'setumei'}){
		$in{'setumei'} =~ s/</&lt;/g;
		$in{'setumei'} =~ s/>/&gt;/g;
	}
	
	unshift (@event_data,"$num<>$name<>$in{'msg'}<>$in{'syo_kokugo'}<>$in{'syo_suugaku'}<>$in{'syo_rika'}<>$in{'syo_syakai'}<>$in{'syo_eigo'}<>$in{'syo_ongaku'}<>$in{'syo_bijutu'}<>$in{'syo_looks'}<>$in{'syo_tairyoku'}<>$in{'syo_kenkou'}<>$in{'syo_speed'}<>$in{'syo_power'}<>$in{'syo_wanryoku'}<>$in{'syo_kyakuryoku'}<>$in{'syo_love'}<>$in{'syo_unique'}<>$in{'syo_etti'}<>$in{'syo_sintai_kaihuku'}<>$in{'syo_zunou_kaihuku'}<>$in{'syo_sintyou'}<>$in{'syo_cal'}<>$in{'syo_money'}<>$in{'syo_byouki'}<>$in{'setumei'}<>\n");
	
	open(OUT,">$filename") || &error("Write Error : $filename");
	eval{ flock (OUT, 2); };
	print OUT @event_data;
	close(OUT);
	
	&header(item_style);
	print <<"EOM";
	<div align=center><br>
	<table border=0 cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
		<span class="job_messe">投稿しました。</span>
	</td></tr></table>
	<br>
	<form method=POST action="event.cgi">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>form<>">
	<input type=submit value="戻る">
	</form>
	
	</div>
EOM
exit;
}

sub form {
	open(STD,"<$filename") || &error("not open");
	@event_all=<STD>;
	close(STD);
	
	if($in{'start'} < 0){$in{'start'} = 0;}
	if($in{'start'} > $#event_all){$in{'start'}= $#event_all;}
	if($in{'start'} > 0){
		$back_flag=1;
		$back=$in{'start'}-$max;
		if($back < 0){$back=0;}
	}
	$next_flag=1;
	$next=$in{'start'} + $max;
	if($next > $#event_all){$next_flag=0;}
			
	for($i=$in{'start'};$i<$next;$i++){
		if($i > $#event_all){last;}
		
		($num,$name,$msg,$kokugo,$suugaku,$rika,$syakai,$eigo,$ongaku,$bijutu,$looks,$tairyoku,$kenkou,$speed,$power,$wanryoku,$kyakuryoku,$love,$unique,$etti,$syo_sintai_kaihuku,$syo_zunou_kaihuku,$syo_sintyou,$syo_cal,$syo_money,$syo_byouki,$setumei) = split(/<>/,$event_all[$i]);
		
		if($looks > 0){$looks = "<font color=\"red\">ルックス↑$looks　　</font>";}
		elsif($looks < 0){$looks = "<font color=\"blue\">ルックス↓$looks　　";}
		
		if($tairyoku > 0){$tairyoku = "<font color=\"red\">体力↑$tairyoku　　</font>";}
		elsif($tairyoku < 0){$tairyoku = "<font color=\"blue\">体力↓$tairyoku　　</font>";}
		
		if($kenkou > 0){$kenkou = "<font color=\"red\">健康↑$kenkou　　</font>";}
		elsif($kenkou < 0){$kenkou = "<font color=\"blue\">健康↓$kenkou　　</font>";}
		
		if($speed > 0){$speed = "<font color=\"red\">スピード↑$speed　　</font>";}
		elsif($speed < 0){$speed = "<font color=\"blue\">スピード↓$speed　　</font>";}
		
		if($power > 0){$power = "<font color=\"red\">パワー↑$power　　</font>";}
		elsif($power < 0){$power = "<font color=\"blue\">パワー↓$power　　</font>";}
		
		if($wanryoku > 0){$wanryoku = "<font color=\"red\">腕力↑$wanryoku　　</font>";}
		elsif($wanryoku < 0){$wanryoku = "<font color=\"blue\">腕力↓$wanryoku　　</font>";}
		
		if($kyakuryoku > 0){$kyakuryoku = "<font color=\"red\">脚力↑$kyakuryoku　　</font>";}
		elsif($kyakuryoku < 0){$kyakuryoku = "<font color=\"blue\">脚力↓$kyakuryoku　　</font>";}
		
		if($kokugo > 0){$kokugo = "<font color=\"red\">国語↑$kokugo　　</font>";}
		elsif($kokugo < 0){$kokugo = "<font color=\"blue\">国語↓$kokugo　　</font>";}
		
		if($suugaku > 0){$suugaku = "<font color=\"red\">数学↑$suugaku　　</font>";}
		elsif($suugaku < 0){$suugaku = "<font color=\"blue\">数学↓$suugaku　　</font>";}
		
		if($rika > 0){$rika = "<font color=\"red\">理科↑$rika　　</font>";}
		elsif($rika < 0){$rika = "<font color=\"blue\">理科↓$rika　　</font>";}
		
		if($syakai > 0){$syakai = "<font color=\"red\">社会↑$syakai　　</font>";}
		elsif($syakai < 0){$syakai = "<font color=\"blue\">社会↓$syakai　　</font>";}
		
		if($eigo > 0){$eigo = "<font color=\"red\">英語↑$eigo　　</font>";}
		elsif($eigo < 0){$eigo = "<font color=\"blue\">英語↓$eigo　　</font>";}
		
		if($ongaku > 0){$ongaku = "<font color=\"red\">音楽↑$ongaku　　</font>";}
		elsif($ongaku < 0){$ongaku = "<font color=\"blue\">音楽↓$ongaku　　</font>";}
		
		if($bijutu > 0){$bijutu = "<font color=\"red\">美術↑$bijutu　　</font>";}
		elsif($bijutu < 0){$bijutu = "<font color=\"blue\">美術↓$bijutu　　</font>";}
		
		if($love > 0){$love = "<font color=\"red\">ＬＯＶＥ↑$love　　</font>";}
		elsif($love < 0){$love = "<font color=\"blue\">ＬＯＶＥ↓$love　　</font>";}
		
		if($unique > 0){$unique = "<font color=\"red\">面白さ↑$unique　　</font>";}
		elsif($unique < 0){$unique = "<font color=\"blue\">面白さ↓$unique　　</font>";}
		
		if($etti > 0){$etti = "<font color=\"red\">エッチ↑$etti　　</font>";}
		elsif($etti < 0){$etti = "<font color=\"blue\">エッチ↓$etti　　</font>";}
		
		if($syo_sintai_kaihuku > 0){$syo_sintai_kaihuku = "<font color=\"red\">身体ＰＯＷＥＲ↑$syo_sintai_kaihuku　　</font>";}
		elsif($syo_sintai_kaihuku < 0){$syo_sintai_kaihuku = "<font color=\"blue\">身体ＰＯＷＥＲ↓$syo_sintai_kaihuku　　</font>";}
		
		if($syo_zunou_kaihuku > 0){$syo_zunou_kaihuku = "<font color=\"red\">頭脳ＰＯＷＥＲ↑$syo_zunou_kaihuku　　</font>";}
		elsif($syo_zunou_kaihuku < 0){$syo_zunou_kaihuku = "<font color=\"blue\">頭脳ＰＯＷＥＲ↓$syo_zunou_kaihuku　　</font>";}
		
		if($syo_sintyou > 0){$syo_sintyou = "<font color=\"red\">身長↑$syo_sintyou cm　　</font>";}
		elsif($syo_sintyou < 0){$syo_sintyou = "<font color=\"blue\">身長↓$syo_sintyou cm　　</font>";}
		
		if($syo_cal > 0){$syo_cal = "<font color=\"red\">体重↑$syo_cal kg　　</font>";}
		elsif($syo_cal < 0){$syo_cal = "<font color=\"blue\">体重↓$syo_cal kg　　</font>";}
		
		if($syo_money > 0){$syo_money = "<font color=\"red\">金↑$syo_money円　　</font>";}
		elsif($syo_money < 0){$syo_money = "<font color=\"blue\">金↓$syo_money円　　</font>";}
		
		if($syo_byouki){$syo_byouki = "病気について：$syo_byouki";}
		
		if($setumei){$setumei = "<br>補足説明：$setumei";}
		
		$message .= <<"EOM";
		<font color="red"><b>$name</b></font><br>
		<b><font color="green">$msg</font></b><br>
		<br>
		$kokugo$suugaku$rika$syakai$eigo$ongaku$bijutu<br>
		$looks$tairyoku$kenkou$speed$power$wanryoku$kyakuryoku<br>
		$love$unique$etti$syo_sintai_kaihuku$syo_zunou_kaihuku$syo_sintyou$syo_cal<br>
		$syo_money$syo_byouki$setumei<br>
		<hr>
EOM
	}

	&header(item_style);
print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td>	
		ここではあなたの思いついたイベント（イベント発生！の）を投稿することができます。<br>
		例えば、数学の欄に-10、国語の欄に10と打てば、「数学が10↓、国語が10↑」となります。<br>
		数字以外のものがあれば表\示されません。<br>
		また、身長up（down）値、体重up（down）値の単位はそれぞれcm（センチメートル）、kg（キログラム）です。<br>
		採用されると、評価ポイントがもらえるかもしれません。<br>
		<font color="red">ふざけた投稿はおやめください。</font>
	</td>
	<td bgcolor="#333333" align=center width="300"><font color="#ffffff" size="5"><b>イベント製作所</b></font></td>
	</tr></table>
	
	<form action="$this_script" method="POST">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value=$in{'town_no'}>
	<input type="hidden" name="mode" value="save">
	
	<table bordercolor="#999999" bgcolor="#ffffff" width="100%" border="2" cellspacing="0" cellpadding="5" align="center">
	<tr><td colspan="7">起こったこと<input type="text" name="msg" size="100"></td></tr>
	<tr><td align="center" colspan="7" bgcolor="#00ff00"><font color="#006699">頭脳up（down）値</font></td></tr>
	<tr><td>国語up値</td><td>数学up値</td><td>理科up値</td><td>社会up値</td><td>英語up値</td><td>音楽up値</td><td>美術up値</td></tr>
	<tr><td><input type="text" size="10" value="±0" name="syo_kokugo"></td>
	<td><input type="text" size="10" value="±0" name="syo_suugaku"></td>
	<td><input type="text" size="10" value="±0" name="syo_rika"></td>
	<td><input type="text" size="10" value="±0" name="syo_syakai"></td>
	<td><input type="text" size="10" value="±0" name="syo_eigo"></td>
	<td><input type="text" size="10" value="±0" name="syo_ongaku"></td>
	<td><input type="text" size="10" value="±0" name="syo_bijutu"></td></tr>
	<tr><td align="center" colspan="7" bgcolor="#00ff00"><font color="#006699">身体up（down）値</font></td></tr>
	<tr><td>ルックスup値</td><td>体力up値</td><td>健康up値</td><td>スピードup値</td><td>パワーup値</td><td>腕力up値</td><td>脚力up値</td></tr>
	<tr><td><input type="text" size="10" value="±0" name="syo_looks"></td>
	<td><input type="text" size="10" value="±0" name="syo_tairyoku"></td>
	<td><input type="text" size="10" value="±0" name="syo_kenkou"></td>
	<td><input type="text" size="10" value="±0" name="syo_speed"></td>
	<td><input type="text" size="10" value="±0" name="syo_power"></td>
	<td><input type="text" size="10" value="±0" name="syo_wanryoku"></td>
	<td><input type="text" size="10" value="±0" name="syo_kyakuryoku"></td></tr>
	<tr><td align="center" colspan="7" bgcolor="#00ff00"><font color="#006699">その他up（down）値</font></td></tr>
	<tr><td>LOVEup値</td><td>面白さup値</td><td>エッチup値</td><td>身体回復</td><td>頭脳回復</td><td>身長up値</td><td>体重up値</td></tr>
	<tr><td><input type=text size="10" value="±0" name=syo_love></td>
	<td><input type="text" size="10" value="±0" name="syo_unique"></td>
	<td><input type="text" size="10" value="±0" name="syo_etti"></td>
	<td><input type="text" size="10" value="±0" name="syo_sintai_kaihuku"></td>
	<td><input type="text" size="10" value="±0" name="syo_zunou_kaihuku"></td>
	<td><input type="text" size="10" value="±0" name="syo_sintyou"></td>
	<td><input type="text" size="10" value="±0" name="syo_cal"></td></tr>
	<tr><td align="center" colspan="7" bgcolor="#00ff00"><font color="#006699">その他説明など</font></td></tr>
	<tr><td>金up値</td><td colspan="2">病気（風邪になる、治る等）</td><td colspan="4">補足説明（アイテムゲット、ほかの人から奪う等）</td></tr>
	<td><input type="text" size="10" value="±0" name="syo_money"></td>
	<td colspan="2"><input type="text" size="30" name="syo_byouki"></td>
	<td colspan="4"><input type="text" size="50" name="setumei"></td></tr>
	<tr><td colspan="7" align="center"><input type=submit name="sousin" value="新規投稿">
	</tr></table>
	
	</form>
	
	<table bgcolor="#ffffff" width="100%" border="1" cellspacing="0" cellpadding="5" align="center"><tr><td>
	$message
	</td></tr></table>
	
	<center>
	<table><tr>
EOM
	
	if($back_flag){	
		print <<"EOM";
		<form action="$this_script" method="POST"><td>
		<input type=hidden name=name value="$in{'name'}">
		<input type=hidden name=pass value="$in{'pass'}">
		<input type=hidden name=town_no value=$in{'town_no'}>
		<input type=hidden name=mode value=form>
		<input type=hidden name=start value=$back>
		<td width="45%" align="right"><input type="submit" value="前のページ">
		</td></form>
EOM
	}
	if($next_flag){	
		print <<"EOM";
		<form action="$this_script" method="POST"><td>
		<input type=hidden name=name value="$in{'name'}">
		<input type=hidden name=pass value="$in{'pass'}">
		<input type=hidden name=town_no value=$in{'town_no'}>
		<input type=hidden name=mode value=form>
		<input type=hidden name=start value=$next>
		<td width="45%" align="left"><input type="submit" value="次のページ">
		</td></form>
EOM
	}
	
	print "</tr></table></center>";

	&hooter("login_view","町に戻る");
	exit;
}
