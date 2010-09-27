#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
######################### koko
# データーファィル名
$kyushitu_dat = "./dat_dir/kyushitu.cgi";
######################## kokoend

$this_script = 'kyushitu.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐

# 使用時間の保持
# $kyushitu_time = "./member/$in{'k_id'}/kyushitu_time.cgi"; # $next_tra を別に保存
	if($in{'mode'} eq "kyushitu"){&kyushitu;}
	elsif($in{'mode'} eq "kyushitu_go"){&kyushitu_go;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
	
#############以下サブルーチン
sub kyushitu{
	open(SP,"$kyushitu_dat") || &error("Open Error : $kyushitu_dat");
	$top_koumoku_kyo = <SP>;
	@koushitu_hairetu = <SP>;
	close(SP);
	($kyo_name,$kyo_koku,$kyo_suu,$kyo_ri,$kyo_sya,$kyo_ei,$kyo_on,$kyo_bi,$kyo_lu,$kyo_tai,$kyo_ken,$kyo_sup,$kyo_paw,$kyo_wan,$kyo_kya,$kyo_love,$kyo_omo,$kyo_h,$kyo_mane,$kyo_kou,$kyo_kankaku,$kyo_shintai,$kyo_zunou,$kyo_yobi1,$kyo_yobi2,$kyo_yobi3) = split(/<>/, $top_koumoku_kyo);
	&header(gym_style);
	&gym_sprit($top_koumoku);

	($next_tra0,$next_tra1,$next_tra2) = split(/=/, $next_tra);#koko2006/08/24

	$toremadeatonanbyou = $next_tra1 - time;
	if($toremadeatonanbyou > 0){$tore_messe = "$nameさんがトレーニングできるまであと$toremadeatonanbyou秒です。";}else{$tore_messe = "今日も張り切って鍛えましょう。";}
	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10"><tr><td width="554" >
	<form method="POST" action="$this_script" NAME="foMes5">		<!--ver.1.2-->
	<INPUT TYPE="hidden" NAME="TeMes5">		<!--ver.1.2-->
	<input type=hidden name=mode value="kyushitu_go">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td colspan=18 bgcolor=#ffffff>$tore_messe<br></td>
	<td colspan=4 bgcolor=#333333 align=center><font color=#ffffff>教　室</font></td>
	</tr>
	<tr><td colspan=22><font color=#336699>凡例：(ル)＝ルックスup値、(体)＝体力up値、(健)＝健康up値、(ス)＝スピードup値、(パ)＝パワーup値、(腕)＝腕力up値、(脚)＝脚力up値、(H)＝エッチup値、(間)＝次にトレーニング出来る間隔、(消)＝消費する身体パワー</font></td></tr>
	<tr bgcolor=#ffff66><td align=center>$kyo_name</td><td>$kyo_koku</td><td>$kyo_suu</td><td>$kyo_ri</td><td>$kyo_sya</td><td>$kyo_ei</td><td>$kyo_on</td><td>$kyo_bi</td><td>$kyo_lu</td><td>$kyo_tai</td><td>$kyo_ken</td><td>$kyo_sup</td><td>$kyo_paw</td><td>$kyo_wan</td><td>$kyo_kya</td><td>$kyo_love</td><td>$kyo_omo</td><td>$kyo_h</td><td>$kyo_mane</td><td>$kyo_kankaku 分</td><td>$kyo_shintai</td><td>$kyo_zunou</td></tr>
EOM
	foreach (@koushitu_hairetu) {
		($kyo_name,$kyo_koku,$kyo_suu,$kyo_ri,$kyo_sya,$kyo_ei,$kyo_on,$kyo_bi,$kyo_lu,$kyo_tai,$kyo_ken,$kyo_sup,$kyo_paw,$kyo_wan,$kyo_kya,$kyo_love,$kyo_omo,$kyo_h,$kyo_mane,$kyo_kou,$kyo_kankaku,$kyo_shintai,$kyo_zunou,$kyo_yobi1,$kyo_yobi2,$kyo_yobi3) = split(/<>/);

		print <<"EOM";
	<tr><td nowrap><input type=radio value="$kyo_name" name="kyo_menu">$kyo_name</td><td>$kyo_koku</td><td>$kyo_suu</td><td>$kyo_ri</td><td>$kyo_sya</td><td>$kyo_ei</td><td>$kyo_on</td><td>$kyo_bi</td><td>$kyo_lu</td><td>$kyo_tai</td><td>$kyo_ken</td><td>$kyo_sup</td><td>$kyo_paw</td><td>$kyo_wan</td><td>$kyo_kya</td><td>$kyo_love</td><td>$kyo_omo</td><td>$kyo_h</td><td>$kyo_mane</td><td>$kyo_kankaku</td><td>$kyo_shintai</td><td>$kyo_zunou</td></tr>
EOM
	}
#koko2006/12/08
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	@my_kounyuu_list =<OUT>;
	close(OUT);
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}
	}

	print <<"EOM";
	<tr><td colspan=22><div align=center>支払い方法 <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select><input type=submit value=" O K "></div></td>
	</table></form></td><td valign=top>
EOM
#kokoend
#	&loged_gamen;
	print "</td></tr></table>";
	&hooter("login_view","戻る");
	exit;
}
############################
sub kyushitu_go{
	($next_tra0,$next_tra1,$next_tra2) = split(/=/, $next_tra);#koko2006/08/24
	open(SP,"$kyushitu_dat") || &error("Open Error : $kyushitu_dat");
	$top_koumoku_kyo = <SP>;
	@koushitu_hairetu = <SP>;
	close(SP);

	foreach (@koushitu_hairetu) {
		($kyo_name,$kyo_koku,$kyo_suu,$kyo_ri,$kyo_sya,$kyo_ei,$kyo_on,$kyo_bi,$kyo_lu,$kyo_tai,$kyo_ken,$kyo_sup,$kyo_paw,$kyo_wan,$kyo_kya,$kyo_love,$kyo_omo,$kyo_h,$kyo_mane,$kyo_kou,$kyo_kankaku,$kyo_shintai,$kyo_zunou,$kyo_yobi1,$kyo_yobi2,$kyo_yobi3) = split(/<>/);
		if($in{'kyo_menu'} eq "$kyo_name"){
			$now_time = time;
			if($energy < $kyo_shintai){&error("身体パワーが足りません。");}
			if($nou_energy < $kyo_zunou){&error("頭脳パワーが足りません。");}

			if($next_tra1 > $now_time){&error("まだトレーニングできません。");}
#koko2006/12/08
			if ($in{'siharaihouhou'} eq "現金"){
				if($money < $kyo_mane){&error("お金が足りません。");}
			}
			if ($in{'siharaihouhou'} ne "現金"){
				$bank -= $kyo_mane;
				&kityou_syori("クレジット支払い（受講料）","$kyo_mane","",$bank,"普");
			}else{
				$money -= $kyo_mane;
			}
#			if($money < $kyo_mane){&error("お金が足りません。");}
#kokoend
				
			if($kyo_koku){$kokugo += $kyo_koku; $print_messe .= "・国語が$kyo_kokuアップしました。<br>";}
			if($kyo_suu){$suugaku += $kyo_suu; $print_messe .= "・数学が$kyo_suuアップしました。<br>";}
			if($kyo_ri){$rika += $kyo_ri; $print_messe .= "・理科が$kyo_riアップしました。<br>";}
			if($kyo_sya){$syakai += $kyo_sya; $print_messe .= "・社会が$kyo_syaアップしました。<br>";}
			if($kyo_ei){$eigo += $kyo_ei; $print_messe .= "・英語が$kyo_eiアップしました。<br>";}
			if($kyo_on){$ongaku += $kyo_on; $print_messe .= "・音楽が$kyo_onアップしました。<br>";}
			if($kyo_bi){$bijutu += $kyo_bi; $print_messe .= "・美術が$kyo_biアップしました。<br>";}
			if($kyo_lu){$looks += $kyo_lu; $print_messe .= "・ルックス値が$kyo_luアップしました。<br>";}
			if($kyo_tai){$tairyoku += $kyo_tai; $print_messe .= "・体力が$kyo_taiアップしました。<br>";}
			if($kyo_ken){$kenkou += $kyo_ken; $print_messe .= "・健康値が$kyo_kenアップしました。<br>";}
			if($kyo_sup){$speed += $kyo_sup; $print_messe .= "・スピードが$kyo_supアップしました。<br>";}
			if($kyo_paw){$power += $kyo_paw; $print_messe .= "・パワーが$kyo_pawアップしました。<br>";}
			if($kyo_wan){$wanryoku += $kyo_wan; $print_messe .= "・腕力が$kyo_wanアップしました。<br>";}
			if($kyo_kya){$kyakuryoku += $kyo_kya; $print_messe .= "・脚力が$kyo_kyaアップしました。<br>";}
			if($kyo_love){$love += $kyo_love; $print_messe .= "・love度が$kyo_loveアップしました。<br>";}
			if($kyo_omo){$unique += $kyo_omo; $print_messe .= "・面白度が$kyo_omoアップしました。<br>";}
			if($kyo_h){$etti += $kyo_h; $print_messe .= "・エッチ度が$kyo_hアップしました。<br>";}

			$next_tra1 = $now_time + ($kyo_kankaku*60);
			$energy -= $kyo_shintai;$print_messe .= "・$kyo_shintaiの身体エネルギーを使いました。<br>";
			$nou_energy -= $kyo_zunou;$print_messe .= "・$kyo_zunouの頭脳エネルギーを使いました。<br>";
			$taijuu_heri = $kyo_shintai / 100 + $kyo_zunou / 100;
			$taijuu -= $taijuu_heri; $print_messe .= "・$taijuu_heri kg体重が減りました。<br>";
		#	$money -= $kyo_mane; # 先に支払い済み
			last;
		}
	}
#ログ更新
			$next_tra2 = "";#2006/11/26
			$next_tra = "$next_tra0=$next_tra1=$next_tra2=";#koko2006/08/24
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);

	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$in{'kyo_menu'}で体を鍛えました。<br>
$print_messe
</span>
</td></tr></table>
<br>

	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
exit;
}

